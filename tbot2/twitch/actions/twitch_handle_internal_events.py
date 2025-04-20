from tbot2.channel import (
    ChannelProvider,
    SendChannelMessage,
    on_event_send_message,
    on_event_update_stream_title,
)

from .twitch_channel_actions import (
    ModifyChannelInformationRequest,
    update_twitch_channel,
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
    await update_twitch_channel(
        channel_provider=channel_provider,
        data=ModifyChannelInformationRequest(
            title=stream_title,
        ),
    )
    return True
