import asyncio
import random
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta

from loguru import logger

from tbot2.channel import ChannelProvider
from tbot2.channel_stream import get_current_channel_provider_stream
from tbot2.common import Provider, datetime_now
from tbot2.common.utils.event import add_event_handler, fire_event_async
from tbot2.contexts import AsyncSession, get_session

from ..actions.timer_actions import (
    Timer,
    get_timers,
    update_timer_next_run_at,
)

CHECK_EVERY = 60


async def task_handle_timers() -> None:
    last_check: datetime | None = None
    logger.info('Starting task_handle_timers')
    while True:
        if last_check:
            elapsed = (datetime_now() - last_check).total_seconds()
            sleep_time = max(0, CHECK_EVERY - elapsed)
        else:
            sleep_time = CHECK_EVERY

        await asyncio.sleep(sleep_time)

        timers = await get_timers(
            enabled=True,
            lte_next_run_at=datetime_now(),
        )
        if not timers:
            logger.debug('No timers to handle')
            break
        await asyncio.gather(*[handle_timer(timer) for timer in timers])


async def handle_timer(timer: Timer) -> None:
    try:
        last_message_index = timer.last_message_index

        if timer.pick_mode == 'random':
            messages = timer.messages
            if last_message_index:
                if last_message_index >= len(messages):
                    messages.pop(last_message_index)
            message = random.choice(timer.messages)
            last_message_index = messages.index(message)

        else:
            if last_message_index is None:
                last_message_index = 0
            if last_message_index >= len(timer.messages):
                last_message_index = 0
            message = timer.messages[last_message_index]
            last_message_index += 1
            if last_message_index >= len(timer.messages):
                last_message_index = 0

        await update_timer_next_run_at(
            timer_id=timer.id,
            next_run_at=datetime_now()
            + timedelta(
                minutes=timer.interval,
            ),
            last_message_index=last_message_index,
        )

        await fire_event_handle_timer(
            timer=timer,
            message=message,
        )

    except Exception as e:
        logger.exception(e)


async def is_timer_active(
    timer: Timer,
    channel_provider: ChannelProvider,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        if timer.active_mode == 'always':
            return True
        stream = await get_current_channel_provider_stream(
            channel_id=timer.channel_id,
            provider=channel_provider.provider,
            provider_id=channel_provider.provider_user_id,
            session=session,
        )
        if timer.active_mode == 'online' and stream:
            return True
        if timer.active_mode == 'offline' and not stream:
            return True
        return False


async def fire_event_handle_timer(
    timer: Timer,
    message: str,
) -> None:
    await fire_event_async(
        f'handle_timer.{timer.provider}',
        timer=timer,
        message=message,
    )


def on_handle_timer(
    provider: Provider,
    priority: int = 128,
) -> Callable[
    [Callable[[Timer, str], Awaitable[None]]],
    Callable[[Timer, str], Awaitable[None]],
]:
    def decorator(
        func: Callable[[Timer, str], Awaitable[None]],
    ) -> Callable[[Timer, str], Awaitable[None]]:
        add_event_handler(f'handle_timer.{provider}', func, priority)
        add_event_handler('handle_timer.all', func, priority)
        return func

    return decorator
