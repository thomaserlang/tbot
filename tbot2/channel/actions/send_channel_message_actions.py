from collections.abc import Awaitable, Callable

from tbot2.common.utils.event import add_event_handler, fire_event_async

from ..schemas.channel_send_message_schema import SendChannelMessage


async def send_channel_message(
    data: SendChannelMessage,
) -> None:
    await fire_event_async(
        'channel_send_message',
        data=data,
    )


def on_send_channel_message(
    priority: int = 128,
) -> Callable[
    [Callable[[SendChannelMessage], Awaitable[None]]],
    Callable[[SendChannelMessage], Awaitable[None]],
]:
    def decorator(
        func: Callable[[SendChannelMessage], Awaitable[None]],
    ) -> Callable[[SendChannelMessage], Awaitable[None]]:
        add_event_handler('channel_send_message', func, priority)
        return func

    return decorator
