from collections.abc import Awaitable, Callable
from uuid import UUID

from tbot2.common.utils.event import add_event_handler, fire_event_async
from tbot2.contexts import AsyncSession


def on_deleting_channel(
    priority: int = 128,
) -> Callable[
    [Callable[[UUID, AsyncSession], Awaitable[None]]],
    Callable[[UUID, AsyncSession], Awaitable[None]],
]:
    def decorator(
        func: Callable[[UUID, AsyncSession], Awaitable[None]],
    ) -> Callable[[UUID, AsyncSession], Awaitable[None]]:
        add_event_handler('deleting_channel', func, priority)
        return func

    return decorator


async def fire_deleting_channel(
    *,
    channel_id: UUID,
    session: AsyncSession,
) -> None:
    await fire_event_async(
        'deleting_channel',
        channel_id=channel_id,
        session=session,
    )
