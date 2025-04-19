from tbot2.channel import get_channel_providers
from tbot2.channel_stream import get_current_channel_provider_stream
from tbot2.channel_timer import Timer, on_handle_timer
from tbot2.youtube.actions.youtube_live_chat_message_actions import (
    send_live_chat_message,
)


@on_handle_timer(provider='youtube')
async def handle_timer(
    timer: Timer,
    message: str,
) -> None:
    for channel_provider in await get_channel_providers(
        channel_id=timer.channel_id,
        provider='twitch',
    ):
        stream = await get_current_channel_provider_stream(
            channel_id=timer.channel_id,
            provider=channel_provider.provider,
            provider_id=channel_provider.provider_user_id,
        )
        if stream:
            await send_live_chat_message(
                channel_provider=channel_provider,
                message=message,
                live_chat_id=stream.provider_stream_id,
            )
