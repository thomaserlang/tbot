from uuid import UUID

import sqlalchemy as sa
from pydantic import TypeAdapter
from uuid6 import uuid7

from tbot2.channel_chat_filters.filters import FilterTypesUnion
from tbot2.contexts import AsyncSession, get_session

from ..models.chat_filter_model import MChatFilter
from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterCreate,
    ChatFilterUpdate,
)


async def get_chat_filter(
    filter_id: UUID,
    session: AsyncSession | None = None,
) -> ChatFilterBase | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatFilter).where(MChatFilter.id == filter_id)
        )
        if result:
            return TypeAdapter(FilterTypesUnion).validate_python(result)  # type: ignore


async def create_chat_filter(
    channel_id: UUID,
    data: ChatFilterCreate,
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
    data: ChatFilterUpdate,
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
