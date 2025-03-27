from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.contexts import AsyncSession, get_session

from ..models.chat_filter_banned_terms_model import MChatFilterBannedTerm
from ..schemas.banned_term_schema import BannedTerm, BannedTermCreate, BannedTermUpdate


async def get_banned_term(
    term_id: UUID,
    session: AsyncSession | None = None,
) -> BannedTerm | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatFilterBannedTerm).where(
                MChatFilterBannedTerm.id == term_id,
            )
        )
        if result:
            return BannedTerm.model_validate(result)


async def get_banned_terms(
    filter_id: UUID,
    session: AsyncSession | None = None,
) -> list[BannedTerm]:
    async with get_session(session) as session:
        terms = await session.scalars(
            sa.select(MChatFilterBannedTerm).where(
                MChatFilterBannedTerm.chat_filter_id == filter_id,
            )
        )
        return [BannedTerm.model_validate(term) for term in terms]


async def create_banned_term(
    filter_id: UUID,
    data: BannedTermCreate,
    session: AsyncSession | None = None,
) -> BannedTerm:
    async with get_session(session) as session:
        id = uuid7()
        await session.execute(
            sa.insert(
                MChatFilterBannedTerm.__table__,  # type: ignore
            ).values(
                id=id,
                chat_filter_id=filter_id,
                **data.model_dump(),
            )
        )
        return BannedTerm(
            id=id,
            chat_filter_id=filter_id,
            type=data.type,
            text=data.text,
        )


async def update_banned_term(
    term_id: UUID,
    data: BannedTermUpdate,
    session: AsyncSession | None = None,
) -> BannedTerm:
    async with get_session(session) as session:
        await session.execute(
            sa.update(MChatFilterBannedTerm)
            .where(MChatFilterBannedTerm.id == term_id)
            .values(**data.model_dump(exclude_unset=True))
        )
        result = await get_banned_term(term_id=term_id, session=session)
        if result is None:
            raise Exception('Banned term not found after update')
        return result


async def delete_banned_term(
    term_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        r = await session.execute(
            sa.delete(MChatFilterBannedTerm).where(
                MChatFilterBannedTerm.id == term_id,
            )
        )
        if r.rowcount == 0:
            raise ValueError('Banned term not found')
        return True
