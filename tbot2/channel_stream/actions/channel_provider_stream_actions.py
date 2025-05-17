from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.channel_provider import (
    ChannelProviderUpdate,
    get_channel_provider,
    reset_channel_provider_live_state,
    update_channel_provider,
)
from tbot2.common import Provider, datetime_now
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
        return None


async def get_current_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_user_id: str | None = None,
    provider_stream_id: str | None = None,
    session: AsyncSession | None = None,
) -> ChannelProviderStream | None:
    async with get_session(session) as session:
        stmt = sa.select(MChannelProviderStream).where(
            MChannelProviderStream.channel_id == channel_id,
            MChannelProviderStream.provider == provider,
            MChannelProviderStream.ended_at.is_(None),
        )
        if provider_user_id:
            stmt = stmt.where(
                MChannelProviderStream.provider_user_id == provider_user_id
            )
        if provider_stream_id:
            stmt = stmt.where(
                MChannelProviderStream.provider_stream_id == provider_stream_id
            )
        result = await session.scalar(stmt)
        if result:
            return ChannelProviderStream.model_validate(result)
        return None


async def create_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_user_id: str,
    provider_stream_id: str,
    started_at: datetime,
    live_stream_id: str | None = None,
    ended_at: datetime | None = None,
    session: AsyncSession | None = None,
) -> ChannelProviderStream:
    """
    Args:
        provider_stream_id: The id of the stream from the provider.
        live_stream_id: This is the id to watch the stream live. For Twitch it would be the username and for YouTube the live broadcast id.
    """  # noqa: E501
    async with get_session(session) as session:
        # Check if there is an existing not ended
        # stream for the channel and provider
        stream = await get_current_channel_provider_stream(
            channel_id=channel_id,
            provider=provider,
            provider_user_id=provider_user_id,
            session=session,
        )
        if stream:
            await end_channel_provider_stream(
                channel_id=channel_id,
                provider=provider,
                provider_user_id=provider_user_id,
                ended_at=datetime_now(),
                session=session,
            )

        id = uuid7()
        stream = await get_or_create_channel_stream(
            channel_id=channel_id, session=session
        )
        try:
            await session.execute(
                sa.insert(MChannelProviderStream.__table__).values(  # type: ignore
                    id=id,
                    channel_id=channel_id,
                    channel_stream_id=stream.id,
                    provider=provider,
                    provider_user_id=provider_user_id,
                    provider_stream_id=provider_stream_id,
                    started_at=started_at,
                    ended_at=ended_at,
                )
            )
        except sa.exc.IntegrityError as e:
            if 'provider_streams_uq' not in str(e.orig):
                raise e

        stream = await get_channel_provider_stream(
            channel_provider_stream_id=id, session=session
        )
        if not stream:
            raise Exception('Failed to create channel provider stream')

        data = ChannelProviderUpdate(
            stream_live=True,
            stream_live_at=started_at,
            channel_provider_stream_id=id,
            stream_viewer_count=1,            
        )
        if live_stream_id:
            data.live_stream_id = live_stream_id
        channel_provider = await get_channel_provider(
            channel_id=channel_id, provider=provider, session=session
        )
        if channel_provider:
            await update_channel_provider(
                channel_provider_id=channel_provider.id, data=data, session=session
            )

        return stream


async def get_or_create_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_user_id: str,
    provider_stream_id: str,
    started_at: datetime,
    live_stream_id: str | None = None,
    session: AsyncSession | None = None,
) -> ChannelProviderStream:
    """
    Args:
        provider_stream_id: The id of the stream from the provider.
        live_stream_id: This is the id to watch the stream live. For Twitch it would be the username and for YouTube the live broadcast id.
    """  # noqa: E501
    stream = await get_current_channel_provider_stream(
        channel_id=channel_id,
        provider=provider,
        provider_user_id=provider_user_id,
        provider_stream_id=provider_stream_id,
        session=session,
    )
    if stream:
        return stream
    return await create_channel_provider_stream(
        channel_id=channel_id,
        provider=provider,
        provider_user_id=provider_user_id,
        provider_stream_id=provider_stream_id,
        started_at=started_at,
        live_stream_id=live_stream_id,
    )


async def end_channel_provider_stream(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_user_id: str | None = None,
    provider_stream_id: str | None = None,
    ended_at: datetime | None = None,
    reset_live_stream_id: bool = False,
    session: AsyncSession | None = None,
) -> ChannelProviderStream | None:
    """
    Args:
        reset_live_stream_id: This is only meant to be true for providers where the stream_id changes per stream, e.g. YouTube.
    """  # noqa: E501
    if ended_at is None:
        ended_at = datetime_now()
    async with get_session(session) as session:
        stream = await get_current_channel_provider_stream(
            channel_id=channel_id,
            provider=provider,
            provider_user_id=provider_user_id,
            session=session,
        )
        if stream and not stream.ended_at:
            stmt = (
                sa.update(MChannelProviderStream.__table__)  # type: ignore
                .where(
                    MChannelProviderStream.id == stream.id,
                )
                .values(ended_at=ended_at)
            )
            if provider_stream_id:
                stmt = stmt.where(
                    MChannelProviderStream.provider_stream_id == provider_stream_id
                )
            await session.execute(stmt)
            stream.ended_at = ended_at

        await reset_channel_provider_live_state(
            channel_id=channel_id,
            provider=provider,
            reset_live_stream_id=reset_live_stream_id,
            session=session,
        )
        return stream
