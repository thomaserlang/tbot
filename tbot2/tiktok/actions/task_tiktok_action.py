import asyncio
import datetime
from uuid import UUID

from loguru import logger
from TikTokLive import TikTokLiveClient  # type: ignore
from TikTokLive.client.errors import UserNotFoundError  # type: ignore
from TikTokLive.events import (  # type: ignore
    CommentEvent,
    ConnectEvent,
    GiftEvent,
    LiveEndEvent,
)
from uuid6 import uuid7

from tbot2.channel_chatlog import create_chatlog
from tbot2.channel_provider import (
    ChannelProvider,
    get_channels_providers,
)
from tbot2.channel_stream import (
    end_channel_provider_stream,
    get_or_create_channel_provider_stream,
)
from tbot2.common import ChatMessage, datetime_now

channel_monitor_tasks: dict[UUID, asyncio.Task[None]] = {}

CHECK_EVERY = 60.0


async def task_tiktok() -> None:
    logger.info('Checking for live tiktok streams')
    while True:
        try:
            current_channels: set[UUID] = set()
            async for channel_provider in get_channels_providers(provider='tiktok'):
                if channel_provider.scope_needed:
                    logger.debug(
                        'Channel provider needs scope, skipping',
                        extra={'channel_provider_id': channel_provider.id},
                    )
                    continue

                current_channels.add(channel_provider.channel_id)
                if channel_provider.channel_id in channel_monitor_tasks:
                    logger.debug(
                        'Channel already being handled',
                        extra={'channel_provider_id': channel_provider.id},
                    )
                    continue
                channel_monitor_tasks[channel_provider.channel_id] = (
                    asyncio.create_task(handle_channel(channel_provider))
                )

            # Remove no longer channels
            for channel_id in list(channel_monitor_tasks.keys()):
                if channel_id not in current_channels:
                    logger.debug(
                        'Cancelling channel monitor', extra={'channel_id': channel_id}
                    )
                    channel_monitor_tasks[channel_id].cancel()
                    del channel_monitor_tasks[channel_id]
        finally:
            await asyncio.sleep(CHECK_EVERY)


@logger.catch
async def handle_channel(
    channel_provider: ChannelProvider,
) -> None:
    with logger.contextualize(channel_provider_id=channel_provider.id):
        logger.debug('Handling tiktok channel')
        try:
            client = TikTokLiveClient(unique_id=f'@{channel_provider.provider_user_id}')

            if not await client.is_live():
                if channel_provider.stream_live:
                    await end_channel_provider_stream(
                        channel_id=channel_provider.channel_id,
                        provider='tiktok',
                        provider_id=channel_provider.provider_user_id,
                        ended_at=datetime_now(),
                    )
                return

            async def on_connect(event: ConnectEvent) -> None:  # type: ignore
                logger.debug(
                    'Connected to tiktok stream',
                    extra={'room_id': event.room_id, 'unique_id': event.unique_id},
                )
                if not channel_provider.stream_live:
                    logger.debug('channel is live')
                    await get_or_create_channel_provider_stream(
                        channel_id=channel_provider.channel_id,
                        provider='tiktok',
                        provider_id=channel_provider.provider_user_id or '',
                        provider_stream_id=str(event.room_id),
                        started_at=datetime.datetime.now(),
                    )

            async def on_comment(event: CommentEvent) -> None:
                await create_chatlog(
                    data=ChatMessage(
                        id=uuid7(),
                        type='message',
                        created_at=datetime_now(),
                        channel_id=channel_provider.channel_id,
                        provider='tiktok',
                        provider_id=client.unique_id,
                        provider_viewer_id=event.user.unique_id,
                        viewer_display_name=event.user.nickname,
                        viewer_name=event.user.unique_id,
                        message=event.comment,
                        msg_id=str(event.base_message.message_id),
                    )
                )

            async def on_gift(event: GiftEvent) -> None:
                message: str | None = None
                if event.gift.streakable and not event.streaking:  # type: ignore
                    message = f'{event.user.nickname} sent {event.repeat_count} '
                    f'{event.gift.name}'
                elif not event.gift.streakable:  # type: ignore
                    message = f'{event.user.nickname} sent {event.gift.name}'
                if message:
                    await create_chatlog(
                        data=ChatMessage(
                            id=uuid7(),
                            type='notice',
                            created_at=datetime_now(),
                            channel_id=channel_provider.channel_id,
                            provider='tiktok',
                            provider_id=client.unique_id,
                            provider_viewer_id=event.user.unique_id,
                            viewer_display_name=event.user.nickname,
                            viewer_name=event.user.unique_id,
                            message=message,
                            msg_id=str(event.base_message.message_id),
                        )
                    )

            async def on_live_end(event: LiveEndEvent) -> None:
                await end_channel_provider_stream(
                    channel_id=channel_provider.channel_id,
                    provider='tiktok',
                    provider_id=channel_provider.provider_user_id,
                    ended_at=datetime_now(),
                )
                await client.disconnect()

            client.add_listener(ConnectEvent, on_connect)  # type: ignore
            client.add_listener(CommentEvent, on_comment)  # type: ignore
            client.add_listener(GiftEvent, on_gift)  # type: ignore
            client.add_listener(LiveEndEvent, on_live_end)  # type: ignore
            await client.connect()  # type: ignore
        except UserNotFoundError as e:
            logger.debug(str(e))
        except Exception as e:
            logger.error(
                'Failed to create tiktok client',
                extra={'error': str(e)},
            )
            return
        finally:
            if channel_provider.id in channel_monitor_tasks:
                del channel_monitor_tasks[channel_provider.id]
