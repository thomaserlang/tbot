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
from tbot2.twitch.actions.twitch_ban_user_actions import (
    twitch_ban_user,
    twitch_unban_user,
)
from tbot2.twitch.actions.twitch_start_commercial_actions import twitch_run_commercial

from .twitch_channel_information_actions import (
    ModifyChannelInformationRequest,
    update_twitch_channel_information,
)
from .twitch_send_message_actions import twitch_bot_send_message


@on_event_send_message('twitch')
async def send_channel_message(data: SendChannelMessage) -> None:
    await twitch_bot_send_message(
        channel_provider=data.channel_provider,
        message=data.message,
    )


@on_event_update_stream_title('twitch')
async def update_stream_title(
    channel_provider: ChannelProvider,
    stream_title: str,
) -> bool:
    await update_twitch_channel_information(
        channel_id=channel_provider.channel_id,
        broadcaster_id=channel_provider.provider_channel_id or '',
        data=ModifyChannelInformationRequest(
            title=stream_title,
        ),
    )
    return True


@on_handle_timer(provider='twitch')
async def handle_timer(
    timer: Timer,
    message: str,
) -> None:
    for channel_provider in await get_channel_providers(
        channel_id=timer.channel_id,
        provider='twitch',
    ):
        if not await is_timer_active(
            timer=timer,
            channel_provider=channel_provider,
        ):
            continue
        await twitch_bot_send_message(
            channel_provider=channel_provider,
            message=message,
        )


@on_event_ban_user('twitch')
async def ban_user(
    data: EventBanUser,
) -> bool:
    return await twitch_ban_user(
        channel_id=data.channel_provider.channel_id,
        broadcaster_id=data.channel_provider.provider_channel_id or '',
        twitch_user_id=data.provider_viewer_id,
        duration=data.ban_duration,
    )


@on_event_unban_user('twitch')
async def unban_user(
    data: EventUnbanUser,
) -> bool:
    return await twitch_unban_user(
        channel_id=data.channel_provider.channel_id,
        broadcaster_id=data.channel_provider.provider_channel_id or '',
        twitch_user_id=data.provider_viewer_id,
    )


@on_event_run_commercial(provider='twitch')
async def run_commercial(
    channel_provider: ChannelProvider,
    length: int,
) -> bool:
    await twitch_run_commercial(
        channel_id=channel_provider.channel_id,
        broadcaster_id=channel_provider.provider_channel_id or '',
        length=length,
    )
    return True
