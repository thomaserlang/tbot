import asyncio
from uuid import UUID

from loguru import logger

from tbot2.channel import ChannelOAuthProvider, get_channels_providers
from tbot2.database import database
from tbot2.exceptions import InternalHttpError
from tbot2.youtube.actions.youtube_handle_message import handle_message

from ..actions.youtube_live_broadcast_actions import get_live_broadcasts
from ..actions.youtube_live_chat_message_actions import (
    LiveChatMessages,
    get_live_chat_messages,
)
from ..schemas.youtube_live_broadcast_schema import LiveBroadcast

live_broadcast_tasks: dict[UUID, list[asyncio.Task[None]]] = {}


async def task_youtube_live() -> None:
    logger.info('Checking for live youtube channels')
    while True:
        channel_provider_ids: dict[UUID, asyncio.Task[None]] = {}

        async for channel_provider in get_channels_providers(provider='youtube'):
            channel_provider_ids[channel_provider.id] = asyncio.create_task(
                handle_channel_provider(channel_provider)
            )

        # Cancel tasks for channels that are no longer active
        for channel_provider_id, tasks in live_broadcast_tasks.items():
            if channel_provider_id not in channel_provider_ids:
                for task in tasks:
                    task.cancel()
                del live_broadcast_tasks[channel_provider_id]
        await asyncio.sleep(60)


@logger.catch
async def handle_channel_provider(channel_provider: ChannelOAuthProvider) -> None:
    with logger.contextualize(
        channel_provider_id=channel_provider.id,
    ):
        logger.debug('Handling channel provider')

        if channel_provider.id in live_broadcast_tasks:
            logger.debug('Is already being handled')
            return

        live_broadcasts = await get_live_broadcasts(
            channel_provider=channel_provider,
        )
        if not live_broadcasts:
            logger.debug('No live broadcasts')
            return

        logger.debug(f'Found {len(live_broadcasts)} live broadcasts')

        for live_broadcast in live_broadcasts:
            task = asyncio.create_task(
                handle_live_broadcast(
                    channel_provider=channel_provider,
                    live_broadcast=live_broadcast,
                )
            )
            live_broadcast_tasks.setdefault(channel_provider.id, []).append(task)


@logger.catch
async def handle_live_broadcast(
    channel_provider: ChannelOAuthProvider,
    live_broadcast: LiveBroadcast,
) -> None:
    live_chat_id = live_broadcast.snippet.live_chat_id

    with logger.contextualize(
        live_chat_id=live_chat_id,
    ):
        logger.info('Monitoring for events')
        try:
            page_token = await database.redis.get(
                f'youtube:live_broadcast:{live_chat_id}:page_token'
            )
            while True:
                try:
                    messages = await get_live_chat_messages(
                        channel_provider=channel_provider,
                        live_chat_id=live_chat_id,
                        page_token=page_token or '',
                    )
                    await database.redis.set(
                        f'youtube:live_broadcast:{live_chat_id}:page_token',
                        messages.next_page_token,
                        ex=60,
                    )
                    page_token = messages.next_page_token
                    logger.trace(
                        f'Got {len(messages.items)} messages, next page token: '
                        f'{page_token}, waiting for '
                        f'{messages.polling_interval_millis}ms'
                    )
                    await asyncio.gather(
                        handle_messages(
                            channel_provider=channel_provider,
                            messages=messages,
                        ),
                        asyncio.sleep(messages.polling_interval_millis / 1000),
                    )
                except InternalHttpError as e:
                    if e.status_code == 403:
                        logger.info(e.body)
                        break
                    else:
                        logger.error(f'Error getting live chat messages: {e.body}')

        finally:
            task = asyncio.current_task()
            if task:
                live_broadcast_tasks[channel_provider.id].remove(task)
                if not live_broadcast_tasks[channel_provider.id]:
                    del live_broadcast_tasks[channel_provider.id]


async def handle_messages(
    channel_provider: ChannelOAuthProvider,
    messages: LiveChatMessages,
) -> None:
    for message in messages.items:
        try:
            await handle_message(
                channel_provider=channel_provider,
                message=message,
            )
        except Exception as e:
            logger.exception(e)
