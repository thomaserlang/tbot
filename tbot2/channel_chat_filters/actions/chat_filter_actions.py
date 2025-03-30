from typing import TypeVar
from uuid import UUID

import sqlalchemy as sa
from pydantic import TypeAdapter
from uuid6 import uuid7

from tbot2.channel_chat_filters.filters import FilterTypesUnion
from tbot2.contexts import AsyncSession, get_session

from ..models.chat_filter_model import MChatFilter
from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseUpdate,
)

T = TypeVar('T', bound=ChatFilterBase)


async def get_chat_filter(
    filter_id: UUID,
    session: AsyncSession | None = None,
    model: type[T] = ChatFilterBase,
) -> T | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatFilter).where(MChatFilter.id == filter_id)
        )
        if result:
            return TypeAdapter[T](FilterTypesUnion).validate_python(result)


async def get_chat_filters(
    channel_id: UUID,
    session: AsyncSession | None = None,
) -> list[ChatFilterBase]:
    async with get_session(session) as session:
        filters = await session.scalars(
            sa.select(MChatFilter).where(MChatFilter.channel_id == channel_id)
        )
        return [
            TypeAdapter(FilterTypesUnion).validate_python(filter_)
            for filter_ in filters
        ]


async def create_chat_filter(
    channel_id: UUID,
    data: ChatFilterBaseCreate,
    session: AsyncSession | None = None,
) -> ChatFilterBase:
    async with get_session(session) as session:
        id = uuid7()
        await session.execute(
            sa.insert(
                MChatFilter.__table__,  # type: ignore
            ).values(
                id=id,
                channel_id=channel_id,
                **data.model_dump(),
            )
        )

        result = await get_chat_filter(
            filter_id=id,
            session=session,
        )
        if result is None:
            raise Exception('Filter not found after creation')
        return result


async def update_chat_filter(
    filter_id: UUID,
    data: ChatFilterBaseUpdate,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        data_.pop('type', None)
        if 'settings' in data_:
            settings = await session.scalar(
                sa.select(MChatFilter.__table__.c.settings).where(
                    MChatFilter.id == filter_id
                )
            )
            settings.update(data_['settings'])  # type: ignore
            data_['settings'] = settings

        await session.execute(
            sa.update(MChatFilter.__table__)  # type: ignore
            .where(MChatFilter.id == filter_id)
            .values(**data_)
        )
        result = await get_chat_filter(
            filter_id=filter_id,
            session=session,
        )
        if result is None:
            raise Exception('Filter not found after update')
        return result


async def delete_chat_filter(
    filter_id: UUID,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        await session.execute(
            sa.delete(
                MChatFilter.__table__,  # type: ignore
            ).where(
                MChatFilter.id == filter_id,
            )
        )
        return True
