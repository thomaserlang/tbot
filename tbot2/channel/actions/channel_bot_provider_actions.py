from uuid import UUID

import sqlalchemy as sa

from tbot2.bot_providers import BotProvider, MBotProvider, delete_bot_provider
from tbot2.channel.models.channel_oauth_provider_model import MChannelOAuthProvider
from tbot2.common import TProvider
from tbot2.contexts import AsyncSession, get_session

from ..actions.channel_oauth_provider_actions import (
    get_channel_oauth_provider_by_id,
    save_channel_oauth_provider,
)
from ..schemas.channel_oauth_provider_schema import ChannelOAuthProviderRequest


async def get_channel_bot_provider(
    *,
    provider: TProvider,
    channel_id: UUID,
    session: AsyncSession | None = None,
) -> BotProvider | None:
    from tbot2.channel import MChannelOAuthProvider

    async with get_session(session) as session:
        query = (
            sa.select(MBotProvider)
            .join(
                MChannelOAuthProvider,
                MChannelOAuthProvider.bot_provider_id == MBotProvider.id,
                isouter=True,
            )
            .where(
                MBotProvider.provider == provider,
                sa.or_(
                    MChannelOAuthProvider.channel_id == channel_id,
                    MBotProvider.system_default.is_(True),
                ),
            )
            .order_by(
                sa.case(
                    (MChannelOAuthProvider.channel_id == channel_id, 1),
                    else_=2,
                )
            )
        )
        bot_provider = await session.scalar(query)
        if bot_provider:
            return BotProvider.model_validate(bot_provider)


async def disconnect_channel_bot_provider(
    *,
    channel_provider_id: UUID,
    channel_id: UUID,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        provider = await get_channel_oauth_provider_by_id(
            channel_id=channel_id,
            provider_id=channel_provider_id,
            session=session,
        )
        if not provider:
            raise ValueError(
                f'Failed to disconnect channel bot provider {channel_provider_id}: '
                'no provider found'
            )
        if not provider.bot_provider:
            raise ValueError(
                f'Failed to disconnect channel bot provider {channel_provider_id}: '
                'no bot provider found'
            )

        await save_channel_oauth_provider(
            channel_id=channel_id,
            provider=provider.provider,
            data=ChannelOAuthProviderRequest(
                bot_provider_id=None,
            ),
            session=session,
        )

        providers_left = await session.scalar(
            sa.select(sa.func.count('*')).where(
                MChannelOAuthProvider.bot_provider_id == provider.bot_provider.id
            )
        )
        if not providers_left:
            await delete_bot_provider(
                bot_provider_id=provider.bot_provider.id,
                session=session,
            )
