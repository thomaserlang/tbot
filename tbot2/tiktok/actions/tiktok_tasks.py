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

from tbot2.channel_chatlog import create_chatlog
from tbot2.channel_provider import (
    ChannelProvider,
    get_channels_providers,
)
from tbot2.channel_stream import (
    ChannelProviderStream,
    add_viewer_count,
    end_channel_provider_stream,
    get_or_create_channel_provider_stream,
)
from tbot2.common import (
    ChatMessagePartRequest,
    ChatMessageRequest,
    GiftPartRequest,
    datetime_now,
)
from tbot2.message_parse import message_to_parts

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

            channel_provider_stream: ChannelProviderStream | None = None

            async def on_connect(event: ConnectEvent) -> None:  # type: ignore
                logger.debug(
                    'Connected to tiktok stream',
                    extra={'room_id': event.room_id, 'unique_id': event.unique_id},
                )
                if not channel_provider.stream_live:
                    logger.debug('channel is live')
                    channel_provider_stream = (
                        await get_or_create_channel_provider_stream(
                            channel_id=channel_provider.channel_id,
                            provider='tiktok',
                            provider_user_id=channel_provider.provider_user_id or '',
                            provider_stream_id=str(event.room_id),
                            started_at=datetime_now(),
                        )
                    )

            async def on_comment(event: CommentEvent) -> None:
                await create_chatlog(
                    data=ChatMessageRequest(
                        type='message',
                        channel_id=channel_provider.channel_id,
                        provider='tiktok',
                        provider_id=client.unique_id,
                        provider_viewer_id=event.user.unique_id,
                        viewer_display_name=event.user.nickname,
                        viewer_name=event.user.unique_id,
                        message=event.comment,
                        parts=await message_to_parts(
                            message=event.comment,
                            provider='tiktok',
                            provider_user_id=channel_provider.provider_user_id or '',
                        ),
                        msg_id=str(event.base_message.message_id),
                    )
                )

            async def on_gift(event: GiftEvent) -> None:
                if event.gift.streakable and event.streaking:  # type: ignore
                    return  # wait til streak ends
                diamonds = event.gift.diamond_count * event.repeat_count
                name = 'diamonds' if diamonds > 1 else 'diamond'
                message = (
                    f'{event.user.nickname} sent {event.gift.name} '
                    f'x{event.repeat_count} ({diamonds} {name})'
                )
                parts: list[ChatMessagePartRequest] = [
                    ChatMessagePartRequest(
                        type='text',
                        text=f'{event.user.nickname} sent ',
                    ),
                    ChatMessagePartRequest(
                        type='gift',
                        text=event.gift.name,
                        gift=GiftPartRequest(
                            id=str(event.gift.id),
                            type='gift',
                            name=event.gift.name,
                            count=event.gift.diamond_count,
                        ),
                    ),
                    ChatMessagePartRequest(
                        type='text',
                        text=f' x{event.repeat_count} ({diamonds} {name})',
                    ),
                ]
                await create_chatlog(
                    data=ChatMessageRequest(
                        type='notice',
                        sub_type='gift',
                        channel_id=channel_provider.channel_id,
                        provider='tiktok',
                        provider_id=client.unique_id,
                        provider_viewer_id=event.user.unique_id,
                        viewer_display_name=event.user.nickname,
                        viewer_name=event.user.unique_id,
                        message=message,
                        parts=parts,
                        msg_id=str(event.base_message.message_id),
                    )
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
                if channel_provider_stream:
                    logger.info(event)
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
