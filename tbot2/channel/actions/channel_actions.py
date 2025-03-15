from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_model import MChannel
from ..schemas.channel_schemas import Channel, ChannelCreate, ChannelUpdate


async def get_channel(
    *, id: UUID, session: AsyncSession | None = None
) -> Channel | None:
    async with get_session(session) as session:
        result = await session.scalar(sa.select(MChannel).where(MChannel.id == id))
        if result:
            return Channel.model_validate(result)


async def create_channel(*, data: ChannelCreate, session: AsyncSession | None = None):
    async with get_session(session) as session:
        data_ = data.model_dump()
        id = uuid7()
        await session.execute(
            sa.insert(MChannel).values(id=id, created_at=datetime_now(), **data_)
        )

        channel = await get_channel(id=id, session=session)
        if not channel:
            raise Exception('Failed to create channel')
        return channel


async def update_channel(
    *,
    id: UUID,
    data: ChannelUpdate,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        await session.execute(
            sa.update(MChannel).where(MChannel.id == id).values(**data_)
        )

        channel = await get_channel(id=id, session=session)
        if not channel:
            raise Exception('Failed to update channel')
        return channel


async def delete_channel(*, id: UUID, session: AsyncSession | None = None):
    async with get_session(session) as session:
        channel = await get_channel(id=id, session=session)
        if not channel:
            return False
        await session.execute(sa.delete(MChannel).where(MChannel.id == id))
        return True
