from tbot2.channel_provider import (
    ChannelProvider,
    SendChannelMessage,
    get_channel_providers,
    on_event_send_message,
    on_event_update_stream_title,
)
from tbot2.channel_timer import Timer, is_timer_active, on_handle_timer

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
        channel_id=channel_provider.id,
        broadcaster_id=channel_provider.provider_user_id or '',
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
