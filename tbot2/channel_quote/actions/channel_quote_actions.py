from datetime import UTC, datetime
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import ErrorMessage, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_quote_model import MChannelQuote
from ..schemas.channel_quote_request_schemas import (
    ChannelQuoteCreate,
    ChannelQuoteUpdate,
)
from ..schemas.channel_quote_schema import ChannelQuote


async def get_random_channel_quote(
    *,
    channel_id: UUID,
    session: AsyncSession | None = None,
) -> ChannelQuote | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelQuote)
            .where(MChannelQuote.channel_id == channel_id)
            .order_by(sa.func.random())
            .limit(1)
        )
        if result:
            return ChannelQuote.model_validate(result)
        return None


async def get_channel_quote_by_number(
    *,
    channel_id: UUID,
    number: int,
    session: AsyncSession | None = None,
) -> ChannelQuote | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelQuote).where(
                MChannelQuote.channel_id == channel_id,
                MChannelQuote.number == number,
            )
        )
        if result:
            return ChannelQuote.model_validate(result)
        return None


async def get_channel_quote(
    *,
    quote_id: UUID,
    session: AsyncSession | None = None,
) -> ChannelQuote | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelQuote).where(MChannelQuote.id == quote_id)
        )
        if result:
            return ChannelQuote.model_validate(result)
        return None


async def create_channel_quote(
    *,
    channel_id: UUID,
    data: ChannelQuoteCreate,
    session: AsyncSession | None = None,
) -> ChannelQuote:
    async with get_session(session) as session:
        number = await session.scalar(
            sa.select(sa.func.count(MChannelQuote.id)).where(
                MChannelQuote.channel_id == channel_id
            )
        )
        if number is None:
            raise ErrorMessage(
                'Failed to get channel quote number',
                code=500,
                type='channel_quote_number_error',
            )

        uuid = uuid7()
        await session.execute(
            sa.insert(MChannelQuote.__table__).values(  # type: ignore
                id=uuid,
                channel_id=channel_id,
                created_at=datetime.now(tz=UTC),
                number=number + 1,
                **data.model_dump(),
            )
        )

        quote = await get_channel_quote(quote_id=uuid, session=session)
        if not quote:
            raise Exception('Failed to create channel quote')

        return quote


async def update_channel_quote(
    *,
    quote_id: UUID,
    data: ChannelQuoteUpdate,
    session: AsyncSession | None = None,
) -> ChannelQuote:
    async with get_session(session) as session:
        result = await session.execute(
            sa.update(MChannelQuote.__table__)  # type: ignore
            .where(MChannelQuote.id == quote_id)
            .values(
                updated_at=datetime_now(),
                **data.model_dump(exclude_unset=True),
            )
        )

        if result.rowcount == 0:
            raise ErrorMessage(
                'Failed to update channel quote',
                code=400,
                type='channel_quote_not_found',
            )

        quote = await get_channel_quote(quote_id=quote_id, session=session)
        if not quote:
            raise Exception('Failed to update channel quote')
        return quote


async def delete_channel_quote(
    *,
    quote_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        quote = await get_channel_quote(quote_id=quote_id, session=session)
        if not quote:
            raise ErrorMessage(
                'Failed to delete channel quote',
                code=400,
                type='channel_quote_not_found',
            )

        r = await session.execute(
            sa.delete(MChannelQuote).where(MChannelQuote.id == quote_id)
        )

        if r.rowcount == 1:
            r = await session.execute(
                sa.update(MChannelQuote.__table__)  # type: ignore
                .where(
                    MChannelQuote.channel_id == quote.channel_id,
                    MChannelQuote.number > quote.number,
                )
                .values(
                    number=MChannelQuote.number - 1,
                )
            )

        return r.rowcount == 1
