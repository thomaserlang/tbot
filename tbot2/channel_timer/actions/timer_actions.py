from datetime import datetime, timedelta
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.channel_timer.models.timer_model import MChannelTimer
from tbot2.common import datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..schemas.timer_schemas import Timer, TimerCreate, TimerUpdate


async def get_timer(
    *,
    timer_id: UUID,
    session: AsyncSession | None = None,
) -> Timer | None:
    async with get_session(session) as session:
        timer = await session.scalar(
            sa.select(MChannelTimer).where(MChannelTimer.id == timer_id)
        )
        if timer:
            return Timer.model_validate(timer)


async def get_timers(
    *,
    channel_id: UUID | None = None,
    enabled: bool | None = None,
    lte_next_run_at: datetime | None = None,
    session: AsyncSession | None = None,
) -> list[Timer]:
    async with get_session(session) as session:
        query = sa.select(MChannelTimer).order_by(MChannelTimer.id)
        if channel_id:
            query = query.where(MChannelTimer.channel_id == channel_id)
        if enabled is not None:
            query = query.where(MChannelTimer.enabled.is_(enabled))
        if lte_next_run_at:
            query = query.where(MChannelTimer.next_run_at <= lte_next_run_at)
        timers = await session.scalars(query)
        return [Timer.model_validate(timer) for timer in timers]


async def create_timer(
    *,
    channel_id: UUID,
    data: TimerCreate,
    session: AsyncSession | None = None,
) -> Timer:
    async with get_session(session) as session:
        id = uuid7()
        await session.execute(
            sa.insert(MChannelTimer.__table__).values(  # type: ignore
                {
                    'id': id,
                    'channel_id': channel_id,
                    'next_run_at': datetime_now() + timedelta(minutes=data.interval),
                    'created_at': datetime_now(),
                    'updated_at': datetime_now(),
                    **data.model_dump(),
                }
            )
        )
        timer = await get_timer(
            timer_id=id,
            session=session,
        )
        if not timer:
            raise Exception('Timer could not be created')
        return timer


async def update_timer(
    *,
    timer_id: UUID,
    data: TimerUpdate,
    session: AsyncSession | None = None,
) -> Timer:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)

        timer = await get_timer(
            timer_id=timer_id,
            session=session,
        )
        if not timer:
            raise ValueError('Timer not found')

        if (data.interval and timer.interval != data.interval) or (
            data.enabled and not timer.enabled
        ):
            data_['next_run_at'] = datetime_now() + timedelta(
                minutes=data.interval or timer.interval
            )
        await session.execute(
            sa.update(MChannelTimer.__table__)  # type: ignore
            .where(MChannelTimer.id == timer_id)
            .values(
                {
                    'updated_at': datetime_now(),
                    **data_,
                }
            )
        )
        timer = await get_timer(
            timer_id=timer_id,
            session=session,
        )
        if not timer:
            raise Exception('Timer could not be updated')
        return timer


async def delete_timer(
    *,
    timer_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        timer = await get_timer(
            timer_id=timer_id,
            session=session,
        )
        if not timer:
            raise ValueError('Timer not found')
        await session.execute(
            sa.delete(MChannelTimer.__table__).where(MChannelTimer.id == timer_id)  # type: ignore
        )
        return True


async def update_timer_next_run_at(
    *,
    timer_id: UUID,
    next_run_at: datetime,
    last_message_index: int,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        await session.execute(
            sa.update(MChannelTimer.__table__)  # type: ignore
            .where(MChannelTimer.id == timer_id)
            .values(
                next_run_at=next_run_at,
                last_message_index=last_message_index,
            )
        )
