from tbot2.channel import SendChannelMessage
from tbot2.channel_timer import Timer, is_timer_active, on_handle_timer

from ..actions.twitch_send_message_actions import (
    channel_send_message,
)


@on_handle_timer()
async def handle_timer(
    timer: Timer,
    message: str,
) -> None:
    if timer.provider != 'twitch' and timer.provider != 'all':
        return

    if not await is_timer_active(
        timer=timer,
        provider='twitch',
    ):
        return

    await channel_send_message(
        SendChannelMessage(
            channel_id=timer.channel_id,
            provider='twitch',
            message=message,
        )
    )
