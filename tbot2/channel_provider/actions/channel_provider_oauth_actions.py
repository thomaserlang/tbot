from datetime import timedelta
from uuid import UUID

import sqlalchemy as sa

from tbot2.common import Provider, datetime_now
from tbot2.contexts import AsyncSession, get_session
from tbot2.database import conn

from ..models.channel_provider_model import MChannelProvider
from ..models.channel_provider_oauth_model import MChannelProviderOAuth
from ..schemas.channel_provider_oauth_schemas import (
    ChannelProviderOAuth,
    ChannelProviderOAuthRequest,
)


async def get_channel_provider_oauth(
    *,
    channel_provider_id: UUID | None = None,
    channel_id: UUID | None = None,
    provider: Provider | None = None,
    session: AsyncSession | None = None,
) -> ChannelProviderOAuth | None:
    async with get_session(session) as session:
        stmt = sa.select(MChannelProviderOAuth)
        if not channel_provider_id and not (channel_id and provider):
            raise ValueError(
                'channel_provider_id or channel_id and provider is required'
            )
        if channel_provider_id:
            stmt = stmt.where(
                MChannelProviderOAuth.channel_provider_id == channel_provider_id,
            )
        if channel_id and provider:
            stmt = stmt.where(
                MChannelProviderOAuth.channel_provider_id == MChannelProvider.id,
                MChannelProvider.channel_id == channel_id,
                MChannelProvider.provider == provider,
            )
        channel_provider = await session.scalar(stmt)
        if channel_provider:
            return ChannelProviderOAuth.model_validate(channel_provider)
        return None


async def save_channel_provider_oauth(
    *,
    channel_provider_id: UUID,
    data: ChannelProviderOAuthRequest,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        data_ = data.model_dump()

        data_['expires_at'] = datetime_now() + timedelta(
            seconds=data_.pop('expires_in'),
        )

        r = await session.execute(
            sa.update(MChannelProviderOAuth)
            .where(
                MChannelProviderOAuth.channel_provider_id == channel_provider_id,
            )
            .values(**data_)
        )

        if r.rowcount == 0:
            await session.execute(
                sa.insert(MChannelProviderOAuth).values(
                    channel_provider_id=channel_provider_id,
                    **data_,
                ),
            )
        else:
            from .channel_provider_actions import get_channel_provider_by_id

            channel_provider = await get_channel_provider_by_id(
                channel_provider_id=channel_provider_id,
                session=session,
            )
            if channel_provider:
                await conn.redis.delete(
                    f'channel_provider_oauth:{channel_provider.provider}:{channel_provider.channel_id}',
                )
        return True
