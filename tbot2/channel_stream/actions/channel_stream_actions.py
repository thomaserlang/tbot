from datetime import timedelta
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import ErrorMessage, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_stream_model import MChannelStream
from ..schemas.channel_stream_schema import ChannelStream


async def get_channel_stream(
    *, channel_stream_id: UUID, session: AsyncSession | None = None
) -> ChannelStream | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelStream).where(MChannelStream.id == channel_stream_id)
        )
        if result:
            return ChannelStream.model_validate(result)


async def get_existing_channel_stream(
    *, channel_id: UUID, within_hours: int = 6, session: AsyncSession | None = None
) -> ChannelStream | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelStream).where(
                MChannelStream.channel_id == channel_id,
                MChannelStream.started_at
                >= datetime_now() - timedelta(hours=within_hours),
            )
        )
        if result:
            return ChannelStream.model_validate(result)


async def get_or_create_channel_stream(
    *, channel_id: UUID, session: AsyncSession | None = None
) -> ChannelStream:
    async with get_session(session) as session:
        existing = await get_existing_channel_stream(
            channel_id=channel_id, session=session
        )
        if existing:
            return existing

        id = uuid7()
        try:
            await session.execute(
                sa.insert(MChannelStream.__table__).values(  # type: ignore
                    id=id, channel_id=channel_id, started_at=datetime_now()
                )
            )
        except sa.exc.IntegrityError as e:
            raise ErrorMessage(
                'Channel not found',
                code=400,
                type='channel_not_found',
            ) from e
        stream = await get_channel_stream(channel_stream_id=id, session=session)
        if not stream:
            raise Exception(
                'Channel stream could not be created',
            )
        return stream
