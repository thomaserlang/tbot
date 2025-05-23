import asyncio
from uuid import UUID

from loguru import logger
from TikTokLive import TikTokLiveClient  # type: ignore
from TikTokLive.client.errors import UserNotFoundError  # type: ignore
from TikTokLive.events import (  # type: ignore
    CommentEvent,
    ConnectEvent,
    GiftEvent,
    LiveEndEvent,
    RoomUserSeqEvent,
)

from tbot2.channel_provider import (
    ChannelProvider,
    get_channels_providers,
)
from tbot2.channel_stream import (
    add_viewer_count,
    end_channel_provider_stream,
    get_current_channel_provider_stream,
    get_or_create_channel_provider_stream,
)
from tbot2.common import datetime_now
from tbot2.database import conn

from .tiktok_handle_events import (
    handle_comment_event,
    handle_gift_event,
)

channel_monitor_tasks: dict[UUID, asyncio.Task[None]] = {}

CHECK_EVERY = 60.0


async def tiktok_tasks() -> None:
    logger.info('Starting tiktok_tasks')
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

                current_channels.add(channel_provider.id)
                if channel_provider.channel_id in channel_monitor_tasks:
                    continue
                channel_monitor_tasks[channel_provider.id] = asyncio.create_task(
                    handle_channel(channel_provider)
                )

            # Remove no longer channels
            for channel_provider_id in list(channel_monitor_tasks.keys()):
                if channel_provider_id not in current_channels:
                    logger.debug(
                        'Cancelling channel monitor',
                        extra={'channel_id': channel_provider_id},
                    )
                    channel_monitor_tasks[channel_provider_id].cancel()
                    del channel_monitor_tasks[channel_provider_id]
            for channel_provider_id in channel_monitor_tasks:
                if channel_monitor_tasks[channel_provider_id].done():
                    del channel_monitor_tasks[channel_provider_id]
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
                        provider_user_id=channel_provider.provider_user_id,
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
                        provider_user_id=channel_provider.provider_user_id or '',
                        provider_stream_id=str(event.room_id),
                        started_at=datetime_now(),
                    )

            async def on_comment(event: CommentEvent) -> None:
                asyncio.create_task(
                    conn.elasticsearch.index(
                        index='tiktok_comment_events',
                        document={
                            'channel_id': channel_provider.channel_id,
                            'channel_provider_id': channel_provider.id,
                            **event.to_dict(),
                        },
                    )
                )
                await handle_comment_event(
                    client=client, channel_provider=channel_provider, event=event
                )

            async def on_gift(event: GiftEvent) -> None:
                asyncio.create_task(
                    conn.elasticsearch.index(
                        index='tiktok_gift_events',
                        document={
                            'channel_id': channel_provider.channel_id,
                            'channel_provider_id': channel_provider.id,
                            **event.to_dict(),
                        },
                    )
                )
                await handle_gift_event(
                    client=client, channel_provider=channel_provider, event=event
                )

            async def on_live_end(event: LiveEndEvent) -> None:
                await end_channel_provider_stream(
                    channel_id=channel_provider.channel_id,
                    provider='tiktok',
                    provider_user_id=channel_provider.provider_user_id,
                    ended_at=datetime_now(),
                )
                await client.disconnect()

            async def on_viewer_count(event: RoomUserSeqEvent) -> None:
                channel_provider_stream = await get_current_channel_provider_stream(
                    channel_id=channel_provider.channel_id,
                    provider='tiktok',
                    provider_user_id=channel_provider.provider_user_id or '',
                )
                if channel_provider_stream:
                    await add_viewer_count(
                        channel_provider_id=channel_provider.id,
                        channel_provider_stream_id=channel_provider_stream.id,
                        viewer_count=event.m_total,
                    )

            client.add_listener(ConnectEvent, on_connect)  # type: ignore
            client.add_listener(CommentEvent, on_comment)  # type: ignore
            client.add_listener(GiftEvent, on_gift)  # type: ignore
            client.add_listener(LiveEndEvent, on_live_end)  # type: ignore
            client.add_listener(RoomUserSeqEvent, on_viewer_count)  # type: ignore
            await client.connect()  # type: ignore
        except UserNotFoundError as e:
            logger.debug(str(e))
            return
        except Exception as e:
            logger.error(
                'Failed to create tiktok client',
                extra={'error': str(e)},
            )
            return
        finally:
            if channel_provider.id in channel_monitor_tasks:
                del channel_monitor_tasks[channel_provider.id]
