from tbot2.channel import SendChannelMessage
from tbot2.channel_timer import Timer, is_timer_active, on_handle_timer
from tbot2.common import TProvider

from ..actions.twitch_send_message_actions import (
    channel_send_message,
)


@on_handle_timer()
async def handle_timer(
    timer: Timer,
    message: str,
) -> None:
    if timer.provider != TProvider.twitch and timer.provider != 'all':
        return

    if not await is_timer_active(
        timer=timer,
        provider=TProvider.twitch,
    ):
        return

    await channel_send_message(
        SendChannelMessage(
            channel_id=timer.channel_id,
            provider=TProvider.twitch,
            message=message,
        )
    )
