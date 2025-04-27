from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.contexts import AsyncSession, get_session

from ..models.chat_filter_link_whitelist_model import (
    MChatFilterLinkAllowlist,
)
from ..schemas.link_allow_schema import (
    LinkAllow,
    LinkAllowCreate,
    LinkAllowUpdate,
)


async def get_link_allow(
    link_id: UUID,
    session: AsyncSession | None = None,
) -> LinkAllow | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatFilterLinkAllowlist).where(
                MChatFilterLinkAllowlist.id == link_id,
            )
        )
        if result:
            return LinkAllow.model_validate(result)


async def get_link_allowlist(
    filter_id: UUID,
    session: AsyncSession | None = None,
) -> list[LinkAllow]:
    async with get_session(session) as session:
        links = await session.scalars(
            sa.select(MChatFilterLinkAllowlist).where(
                MChatFilterLinkAllowlist.chat_filter_id == filter_id,
            )
        )
        return [LinkAllow.model_validate(link) for link in links]


async def create_link_allow(
    filter_id: UUID,
    data: LinkAllowCreate,
    session: AsyncSession | None = None,
) -> LinkAllow:
    async with get_session(session) as session:
        id = uuid7()
        await session.execute(
            sa.insert(
                MChatFilterLinkAllowlist.__table__,  # type: ignore
            ).values(
                id=id,
                chat_filter_id=filter_id,
                **data.model_dump(exclude_unset=True),
            )
        )
        return LinkAllow(
            id=id,
            chat_filter_id=filter_id,
            url=data.url,
        )


async def update_link_allow(
    link_id: UUID,
    data: LinkAllowUpdate,
    session: AsyncSession | None = None,
) -> LinkAllow:
    async with get_session(session) as session:
        await session.execute(
            sa.update(MChatFilterLinkAllowlist.__table__)  # type: ignore
            .where(
                MChatFilterLinkAllowlist.id == link_id,
            )
            .values(**data.model_dump())
        )
        result = await get_link_allow(
            link_id=link_id,
            session=session,
        )
        if result is None:
            raise Exception('Link not found after update')
        return result


async def delete_link_allow(
    link_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        await session.execute(
            sa.delete(MChatFilterLinkAllowlist.__table__).where(  # type: ignore
                MChatFilterLinkAllowlist.id == link_id,
            )
        )
        result = await get_link_allow(link_id=link_id, session=session)
        if result is not None:
            raise Exception('Link not deleted')
        return True
