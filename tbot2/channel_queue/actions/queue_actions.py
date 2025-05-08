from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from tbot2.common import ErrorMessage, datetime_now
from tbot2.contexts import get_session

from ..models.channel_queue_model import MChannelQueue
from ..schemas.queue_schema import (
    Queue,
    QueueCreate,
    QueueUpdate,
)


async def get_queue(
    channel_queue_id: UUID, session: AsyncSession | None = None
) -> Queue | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelQueue).where(MChannelQueue.id == channel_queue_id)
        )
        if result:
            return Queue.model_validate(result)
        return None


async def get_queues(
    channel_id: UUID,
    name: str | None = None,
    session: AsyncSession | None = None,
) -> list[Queue]:
    async with get_session(session) as session:
        stmt = (
            sa.select(MChannelQueue)
            .where(MChannelQueue.channel_id == channel_id)
            .order_by(MChannelQueue.id)
        )
        if name:
            stmt = stmt.where(MChannelQueue.name == name)
        result = await session.scalars(stmt)
        return [Queue.model_validate(r) for r in result]


async def create_queue(
    channel_id: UUID,
    data: QueueCreate,
    session: AsyncSession | None = None,
) -> Queue:
    async with get_session(session) as session:
        id = uuid7()
        data_ = data.model_dump()
        try:
            await session.execute(
                sa.insert(MChannelQueue.__table__).values(  # type: ignore
                    id=id,
                    channel_id=channel_id,
                    created_at=datetime_now(),
                    **data_,
                )
            )
        except IntegrityError as e:
            raise ErrorMessage(
                'Queue with this name already exists',
                type='queue_already_exists',
                code=400,
            ) from e
        queue = await get_queue(channel_queue_id=id, session=session)
        if not queue:
            raise ValueError('Queue not found after creation')
        return queue


async def update_queue(
    channel_queue_id: UUID,
    data: QueueUpdate,
    session: AsyncSession | None = None,
) -> Queue:
    async with get_session(session) as session:
        data_ = data.model_dump()
        await session.execute(
            sa.update(MChannelQueue.__table__)  # type: ignore
            .where(MChannelQueue.id == channel_queue_id)
            .values(**data_)
        )
        queue = await get_queue(channel_queue_id=channel_queue_id, session=session)
        if queue is None:
            raise ValueError('Queue not found after creation')
        return queue


async def delete_queue(
    channel_queue_id: UUID, session: AsyncSession | None = None
) -> bool:
    async with get_session(session) as session:
        r = await session.execute(
            sa.delete(MChannelQueue.__table__).where(  # type: ignore
                MChannelQueue.id == channel_queue_id
            )
        )
        return r.rowcount > 0
