from collections.abc import Awaitable, Callable

from tbot2.common import Provider
from tbot2.common.utils.event import add_event_handler, fire_event_async

from .schemas.event_ban_user_schema import EventBanUser, EventUnbanUser
from .schemas.event_send_message_schema import ChannelProvider, SendChannelMessage


async def fire_event_send_message(
    data: SendChannelMessage,
) -> None:
    await fire_event_async(
        f'channel_send_message.{data.channel_provider.provider}',
        data=data,
    )


def on_event_send_message(
    provider: Provider,
    priority: int = 128,
) -> Callable[
    [Callable[[SendChannelMessage], Awaitable[None]]],
    Callable[[SendChannelMessage], Awaitable[None]],
]:
    def decorator(
        func: Callable[[SendChannelMessage], Awaitable[None]],
    ) -> Callable[[SendChannelMessage], Awaitable[None]]:
        add_event_handler(f'channel_send_message.{provider}', func, priority)
        return func

    return decorator


async def fire_event_update_stream_title(
    channel_provider: ChannelProvider,
    stream_title: str,
) -> bool:
    result = await fire_event_async(
        f'channel_update_stream_title.{channel_provider.provider}',
        channel_provider=channel_provider,
        stream_title=stream_title,
    )
    return all([bool(r) for r in result])


def on_event_update_stream_title(
    provider: Provider,
    priority: int = 128,
) -> Callable[
    [Callable[[ChannelProvider, str], Awaitable[bool]]],
    Callable[[ChannelProvider, str], Awaitable[bool]],
]:
    def decorator(
        func: Callable[[ChannelProvider, str], Awaitable[bool]],
    ) -> Callable[[ChannelProvider, str], Awaitable[bool]]:
        add_event_handler(
            f'channel_update_stream_title.{provider}',
            func,
            priority,
        )
        return func

    return decorator


async def fire_event_ban_user(
    data: EventBanUser,
) -> list[bool]:
    return await fire_event_async(
        f'channel_ban_user.{data.channel_provider.provider}',
        data=data,
    )


def on_event_ban_user(
    provider: Provider,
    priority: int = 128,
) -> Callable[
    [Callable[[EventBanUser], Awaitable[bool]]],
    Callable[[EventBanUser], Awaitable[bool]],
]:
    def decorator(
        func: Callable[[EventBanUser], Awaitable[bool]],
    ) -> Callable[[EventBanUser], Awaitable[bool]]:
        add_event_handler(f'channel_ban_user.{provider}', func, priority)
        return func

    return decorator


async def fire_event_unban_user(
    data: EventUnbanUser,
) -> list[bool]:
    return await fire_event_async(
        f'channel_unban_user.{data.channel_provider.provider}',
        data=data,
    )


def on_event_unban_user(
    provider: Provider,
    priority: int = 128,
) -> Callable[
    [Callable[[EventUnbanUser], Awaitable[bool]]],
    Callable[[EventUnbanUser], Awaitable[bool]],
]:
    def decorator(
        func: Callable[[EventUnbanUser], Awaitable[bool]],
    ) -> Callable[[EventUnbanUser], Awaitable[bool]]:
        add_event_handler(f'channel_unban_user.{provider}', func, priority)
        return func

    return decorator
