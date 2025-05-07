from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from tbot2.common import ErrorMessage, datetime_now
from tbot2.contexts import get_session

from ..models.queue_model import MQueue
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
            sa.select(MQueue).where(MQueue.id == channel_queue_id)
        )
        if result:
            return Queue.model_validate(result)


async def get_queue_by_name(
    channel_id: UUID, name: str, session: AsyncSession | None = None
) -> Queue | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MQueue).where(
                MQueue.channel_id == channel_id,
                MQueue.name == name,
            )
        )
        if result:
            return Queue.model_validate(result)


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
                sa.insert(MQueue.__table__).values(  # type: ignore
                    id=id,
                    channel_id=channel_id,
                    created_at=datetime_now(),
                    **data_,
                )
            )
        except sa.exc.IntegrityError as e:
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
            sa.update(MQueue.__table__)  # type: ignore
            .where(MQueue.id == channel_queue_id)
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
            sa.delete(MQueue.__table__).where(  # type: ignore
                MQueue.id == channel_queue_id
            )
        )
        return r.rowcount > 0
