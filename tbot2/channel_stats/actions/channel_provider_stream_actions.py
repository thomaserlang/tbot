from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import TProvider, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..actions.channel_stream_actions import (
    get_or_create_channel_stream,
)
from ..models.channel_provider_stream_model import MChannelProviderStream
from ..schemas.channel_provider_stream_schema import ChannelProviderStream


async def get_channel_provider_stream(
    *, channel_provider_stream_id: UUID, session: AsyncSession | None = None
) -> ChannelProviderStream | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelProviderStream).where(
                MChannelProviderStream.id == channel_provider_stream_id
            )
        )
        if result:
            return ChannelProviderStream.model_validate(result)


async def get_current_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: TProvider,
    session: AsyncSession | None = None,
) -> ChannelProviderStream | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelProviderStream).where(
                MChannelProviderStream.channel_id == channel_id,
                MChannelProviderStream.provider == provider,
                MChannelProviderStream.ended_at.is_(None),
            )
        )
        if result:
            return ChannelProviderStream.model_validate(result)


async def create_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: TProvider,
    provider_stream_id: str,
    started_at: datetime,
    ended_at: datetime | None = None,
    session: AsyncSession | None = None,
) -> ChannelProviderStream:
    async with get_session(session) as session:
        # Check if there is an existing not ended
        # stream for the channel and provider
        stream = await get_current_channel_provider_stream(
            channel_id=channel_id,
            provider=provider,
            session=session,
        )
        if stream:
            await end_channel_provider_stream(
                channel_id=channel_id,
                provider=provider,
                ended_at=datetime_now(),
                session=session,
            )

        id = uuid7()
        stream = await get_or_create_channel_stream(
            channel_id=channel_id, session=session
        )
        await session.execute(
            sa.insert(MChannelProviderStream.__table__).values(  # type: ignore
                id=id,
                channel_id=channel_id,
                channel_stream_id=stream.id,
                provider=provider,
                provider_stream_id=provider_stream_id,
                started_at=started_at,
                ended_at=ended_at,
            )
        )
        stream = await get_channel_provider_stream(
            channel_provider_stream_id=id, session=session
        )
        if not stream:
            raise ValueError('Failed to create channel provider stream')
        return stream


async def end_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: TProvider,
    ended_at: datetime | None = None,
    session: AsyncSession | None = None,
) -> ChannelProviderStream | None:
    if ended_at is None:
        ended_at = datetime_now()
    async with get_session(session) as session:
        stream = await get_current_channel_provider_stream(
            channel_id=channel_id,
            provider=provider,
            session=session,
        )
        if not stream:
            return None
        await session.execute(
            sa.update(MChannelProviderStream.__table__)  # type: ignore
            .where(
                MChannelProviderStream.id == stream.id,
            )
            .values(ended_at=ended_at)
        )
        stream.ended_at = ended_at
        return stream
