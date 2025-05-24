import asyncio
from datetime import datetime
from uuid import UUID

from loguru import logger

from tbot2.channel_provider import (
    ChannelProvider,
    ChannelProviderRequest,
    create_or_update_channel_provider,
    get_channels_providers,
)
from tbot2.channel_stream import (
    add_viewer_count,
    end_channel_provider_stream,
    get_or_create_channel_provider_stream,
)
from tbot2.common import datetime_now
from tbot2.common.utils.chunk_list import chunk_list
from tbot2.database import conn

from ..actions.youtube_handle_message import handle_message
from ..actions.youtube_live_broadcast_actions import (
    get_live_broadcasts,
)
from ..actions.youtube_live_chat_message_actions import (
    LiveChatMessages,
    get_live_chat_messages,
)
from ..actions.youtube_video_actions import get_youtube_videos
from ..exceptions import YouTubeException
from ..schemas.youtube_live_broadcast_schema import LiveBroadcast

broadcast_chat_monitor_tasks: dict[str, asyncio.Task[None]] = {}
CHECK_EVERY = 60.0


async def youtube_tasks() -> None:
    last_check: datetime | None = None
    logger.info('Starting youtube_tasks')
    while True:
        try:
            fns = [
                check_for_live(),
                update_viewer_count(),
            ]
            await asyncio.wait(
                [asyncio.create_task(fn) for fn in fns],
                return_when=asyncio.FIRST_EXCEPTION,
            )
        finally:
            if last_check:
                elapsed = (datetime_now() - last_check).total_seconds()
                sleep_time = max(0.0, CHECK_EVERY - elapsed)
            else:
                sleep_time = CHECK_EVERY
            await asyncio.sleep(sleep_time)
            last_check = datetime_now()


async def update_viewer_count() -> None:
    logger.debug('Updating viewer count')
    channel_providers: list[ChannelProvider] = []
    async for channel_provider in get_channels_providers(
        provider='youtube', stream_live=True
    ):
        channel_providers.append(channel_provider)

    for chunk in chunk_list(channel_providers, 50):
        video_ids = [
            channel_provider.live_stream_id
            for channel_provider in chunk
            if channel_provider.live_stream_id
        ]
        videos = await get_youtube_videos(video_ids=video_ids)
        videos_by_id = {video.id: video for video in videos}
        for channel_provider in chunk:
            video = videos_by_id.get(channel_provider.live_stream_id or '')
            if (
                not video
                or not video.live_streaming_details
                or not channel_provider.channel_provider_stream_id
            ):
                continue
            if (
                channel_provider.stream_viewer_count
                == video.live_streaming_details.concurrent_viewers
            ):
                continue
            await add_viewer_count(
                channel_provider_id=channel_provider.id,
                channel_provider_stream_id=channel_provider.channel_provider_stream_id,
                viewer_count=video.live_streaming_details.concurrent_viewers or 0,
            )


@logger.catch()
async def check_for_live() -> None:
    channel_provider_ids: dict[UUID, asyncio.Task[None]] = {}
    current_chat_ids: set[str] = set()

    async for channel_provider in get_channels_providers(provider='youtube'):
        if channel_provider.scope_needed:
            logger.debug(
                'Channel provider needs scope, skipping',
                extra={'channel_provider_id': channel_provider.id},
            )
            continue
        channel_provider_ids[channel_provider.id] = asyncio.create_task(
            check_for_broadcast(channel_provider)
        )

        if channel_provider.stream_chat_id:
            if channel_provider.stream_chat_id not in broadcast_chat_monitor_tasks:
                task = asyncio.create_task(
                    handle_broadcast_live_chat(
                        channel_provider=channel_provider,
                        live_chat_id=channel_provider.stream_chat_id,
                    )
                )
                broadcast_chat_monitor_tasks[channel_provider.stream_chat_id] = task
            current_chat_ids.add(channel_provider.stream_chat_id)

    # Remove no longer monitored live chats
    for chat_id in list(broadcast_chat_monitor_tasks.keys()):
        if chat_id not in current_chat_ids:
            logger.debug(
                'Cancelling chat live monitor',
                extra={'stream_chat_id': chat_id},
            )
            broadcast_chat_monitor_tasks[chat_id].cancel()
            del broadcast_chat_monitor_tasks[chat_id]

    for id in broadcast_chat_monitor_tasks:
        if broadcast_chat_monitor_tasks[id].done():
            del broadcast_chat_monitor_tasks[id]


@logger.catch
async def check_for_broadcast(channel_provider: ChannelProvider) -> None:
    with logger.contextualize(
        channel_provider_id=channel_provider.id,
    ):
        upcoming_live_broadcasts: list[LiveBroadcast] = []
        try:
            active_live_broadcasts = await get_live_broadcasts(
                channel_id=channel_provider.channel_id,
                broadcast_status='active',
            )
            if not active_live_broadcasts:
                upcoming_live_broadcasts = await get_live_broadcasts(
                    channel_id=channel_provider.channel_id,
                    broadcast_status='upcoming',
                )

        except YouTubeException as e:
            if e.error.errors:
                if e.error.errors[0].reason == 'liveStreamingNotEnabled':
                    logger.debug(
                        'Live streaming is not enabled for this channel, '
                        'skipping live broadcast check',
                    )
                    return
            raise e

        if not active_live_broadcasts and channel_provider.stream_live:
            await end_stream(channel_provider=channel_provider)
            return

        for live_broadcast in active_live_broadcasts or upcoming_live_broadcasts:
            if channel_provider.live_stream_id != live_broadcast.id:
                await create_or_update_channel_provider(
                    channel_id=channel_provider.channel_id,
                    provider='youtube',
                    data=ChannelProviderRequest(
                        live_stream_id=live_broadcast.id,
                        stream_chat_id=live_broadcast.snippet.live_chat_id,
                    ),
                )

            if live_broadcast.snippet.actual_start_time and (
                not channel_provider.stream_live
                or channel_provider.live_stream_id != live_broadcast.id
            ):
                logger.debug('Channel is live')
                await get_or_create_channel_provider_stream(
                    channel_id=channel_provider.channel_id,
                    provider='youtube',
                    provider_channel_id=live_broadcast.snippet.channel_id,
                    provider_stream_id=live_broadcast.id,
                    started_at=live_broadcast.snippet.actual_start_time,
                )

            if channel_provider.stream_title != live_broadcast.snippet.title:
                await create_or_update_channel_provider(
                    channel_id=channel_provider.channel_id,
                    provider='youtube',
                    data=ChannelProviderRequest(
                        stream_title=live_broadcast.snippet.title,
                    ),
                )

            if live_broadcast.snippet.live_chat_id not in broadcast_chat_monitor_tasks:
                task = asyncio.create_task(
                    handle_broadcast_live_chat(
                        channel_provider=channel_provider,
                        live_chat_id=live_broadcast.snippet.live_chat_id,
                    )
                )
                broadcast_chat_monitor_tasks[live_broadcast.snippet.live_chat_id] = task

            # Is having multiple streams live at the same time
            # for a channel actually a thing?
            # For now just track the latest ready or live one.
            break


@logger.catch
async def handle_broadcast_live_chat(
    channel_provider: ChannelProvider,
    live_chat_id: str,
) -> None:
    with logger.contextualize(
        channel_provider_id=channel_provider.id,
        live_chat_id=live_chat_id,
    ):
        logger.debug('Monitoring for events')
        try:
            page_token = await conn.redis.get(
                f'youtube:live_broadcast:{live_chat_id}:page_token'
            )
            while True:
                messages: LiveChatMessages | None = None
                try:
                    messages = await get_live_chat_messages(
                        channel_id=channel_provider.channel_id,
                        live_chat_id=live_chat_id,
                        page_token=page_token or '',
                    )
                except YouTubeException as e:
                    for error in e.error.errors:
                        if error.reason == 'liveChatEnded':
                            await end_stream(
                                channel_provider=channel_provider,
                            )
                            return
                        if error.reason == 'liveChatNotFound':
                            await end_stream(
                                channel_provider=channel_provider,
                            )
                            return

                    logger.error(
                        'Error getting live chat messages',
                        extra={
                            'error': e.error,
                        },
                    )
                    if e.error.code in (403, 404):
                        return
                    await asyncio.sleep(60)
                    continue

                await conn.redis.set(
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

                if messages.offline_at:
                    logger.info(
                        f'Live chat is offline, stopping monitoring {live_chat_id}'
                    )
                    await end_stream(channel_provider=channel_provider)
                    break

                await asyncio.gather(
                    handle_messages(
                        channel_provider=channel_provider,
                        messages=messages,
                    ),
                    asyncio.sleep(messages.polling_interval_millis / 1000),
                )

        finally:
            if live_chat_id in broadcast_chat_monitor_tasks:
                del broadcast_chat_monitor_tasks[live_chat_id]


async def handle_messages(
    channel_provider: ChannelProvider,
    messages: LiveChatMessages,
) -> None:
    for message in messages.items:
        try:
            await handle_message(
                channel_provider=channel_provider,
                live_message=message,
            )
        except Exception as e:
            logger.exception(e)


async def end_stream(
    channel_provider: ChannelProvider,
    live_broadcast: LiveBroadcast | None = None,
) -> None:
    logger.debug('Ending stream')
    if not live_broadcast:
        live_broadcasts = await get_live_broadcasts(
            channel_id=channel_provider.channel_id,
            broadcast_status='completed',
        )
        if not live_broadcasts:
            await end_channel_provider_stream(
                channel_id=channel_provider.channel_id,
                provider='youtube',
                provider_channel_id=channel_provider.provider_channel_id,
                ended_at=datetime_now(),
                reset_live_stream_id=True,
            )
            return
        live_broadcast = live_broadcasts[0]
    await end_channel_provider_stream(
        channel_id=channel_provider.channel_id,
        provider='youtube',
        provider_channel_id=live_broadcast.snippet.channel_id,
        provider_stream_id=live_broadcast.id,
        ended_at=live_broadcast.snippet.actual_end_time,
        reset_live_stream_id=True,
    )
