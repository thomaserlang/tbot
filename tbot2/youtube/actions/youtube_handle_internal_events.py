from loguru import logger

from tbot2.channel_provider import (
    ChannelProvider,
    EventBanUser,
    EventUnbanUser,
    SendChannelMessage,
    get_channel_providers,
    on_event_ban_user,
    on_event_send_message,
    on_event_unban_user,
    on_event_update_stream_title,
)
from tbot2.channel_provider.event_types import on_event_run_commercial
from tbot2.channel_timer import Timer, is_timer_active, on_handle_timer
from tbot2.common import ErrorMessage
from tbot2.youtube.actions.youtube_live_broadcast_cuepoint_action import (
    insert_live_broadcast_cuepoint,
)

from ..actions.youtube_live_broadcast_actions import update_live_broadcast
from ..actions.youtube_live_chat_ban_actions import live_chat_ban
from ..actions.youtube_live_chat_message_actions import (
    send_live_chat_message,
)


@on_event_send_message('youtube')
async def send_channel_message(data: SendChannelMessage) -> None:
    if data.channel_provider.stream_chat_id:
        await send_live_chat_message(
            channel_id=data.channel_provider.channel_id,
            message=data.message,
            live_chat_id=data.channel_provider.stream_chat_id,
        )
    else:
        logger.error(
            f'Channel {data.channel_provider.channel_id} '
            'has no stream chat id, skipping message send'
        )


@on_event_update_stream_title('youtube')
async def update_stream_title(
    channel_provider: ChannelProvider,
    stream_title: str,
) -> bool:
    if not channel_provider.live_stream_id:
        raise ErrorMessage(
            'No youtube broadcast was found. '
            'Create one first before updating the title',
            type='no_youtube_broadcast',
        )
    await update_live_broadcast(
        channel_id=channel_provider.channel_id,
        live_broadcast_id=channel_provider.live_stream_id,
        snippet_title=stream_title[:100],
    )
    return True


@on_handle_timer(provider='youtube')
async def handle_timer(
    timer: Timer,
    message: str,
) -> None:
    for channel_provider in await get_channel_providers(
        channel_id=timer.channel_id,
        provider='youtube',
    ):
        if channel_provider.stream_chat_id:
            if not await is_timer_active(
                timer=timer,
                channel_provider=channel_provider,
            ):
                continue
            await send_live_chat_message(
                channel_id=channel_provider.channel_id,
                message=message,
                live_chat_id=channel_provider.stream_chat_id,
            )


@on_event_ban_user('youtube')
async def ban_user(
    data: EventBanUser,
) -> bool:
    return await live_chat_ban(
        channel_id=data.channel_provider.channel_id,
        live_chat_id=data.channel_provider.stream_chat_id or '',
        type='permanent' if not data.ban_duration else 'temporary',
        banned_youtube_user_channel_id=data.provider_viewer_id,
        ban_duration_seconds=data.ban_duration,
    )


@on_event_unban_user('youtube')
async def unban_user(
    data: EventUnbanUser,
) -> bool:
    raise ErrorMessage(
        'Unban of user on YouTube is currently not supported',
        type='not_supported',
    )


@on_event_run_commercial('youtube')
async def run_commercial(
    channel_provider: ChannelProvider,
    length: int,
) -> bool:
    await insert_live_broadcast_cuepoint(
        channel_id=channel_provider.channel_id,
        live_broadcast_id=channel_provider.live_stream_id or '',
        duration_secs=length,
    )
    return True
