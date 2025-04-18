from tbot2.channel import get_channel_oauth_providers
from tbot2.channel_timer import Timer, is_timer_active, on_handle_timer

from .twitch_send_message_actions import (
    twitch_bot_send_message,
)


@on_handle_timer(provider='twitch')
async def handle_timer(
    timer: Timer,
    message: str,
) -> None:
    for channel_provider in await get_channel_oauth_providers(
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
