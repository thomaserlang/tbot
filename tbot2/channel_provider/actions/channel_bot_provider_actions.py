from uuid import UUID

import sqlalchemy as sa

from tbot2.bot_providers import BotProvider, MBotProvider, delete_bot_provider
from tbot2.common import ErrorMessage, Provider
from tbot2.contexts import AsyncSession, get_session

from ..event_types import fire_disconnect_channel_bot_provider
from ..models.channel_provider_model import MChannelProvider
from ..schemas.channel_provider_schema import ChannelProviderRequest
from .channel_provider_actions import (
    get_channel_provider_by_id,
    save_channel_provider,
)


async def get_channel_bot_provider(
    *,
    provider: Provider,
    channel_id: UUID,
    session: AsyncSession | None = None,
) -> BotProvider | None:
    async with get_session(session) as session:
        query = (
            sa.select(MBotProvider)
            .join(
                MChannelProvider,
                MChannelProvider.bot_provider_id == MBotProvider.id,
                isouter=True,
            )
            .where(
                MBotProvider.provider == provider,
                sa.or_(
                    MChannelProvider.channel_id == channel_id,
                    MBotProvider.system_default.is_(True),
                ),
            )
            .order_by(
                sa.case(
                    (MChannelProvider.channel_id == channel_id, 1),
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
        channel_provider = await get_channel_provider_by_id(
            channel_provider_id=channel_provider_id,
            session=session,
        )
        if not channel_provider or channel_provider.channel_id != channel_id:
            raise ErrorMessage(
                f'Failed to disconnect channel bot provider {channel_provider_id}: '
                'no provider found',
                code=400,
                type='channel_provider_not_found',
            )
        if not channel_provider.bot_provider:
            raise ErrorMessage(
                f'Failed to disconnect channel bot provider {channel_provider_id}: '
                'no bot provider found',
                code=400,
                type='bot_provider_not_found',
            )

        await save_channel_provider(
            channel_id=channel_id,
            provider=channel_provider.provider,
            data=ChannelProviderRequest(
                bot_provider_id=None,
            ),
            session=session,
        )

        providers_left = await session.scalar(
            sa.select(sa.func.count('*')).where(
                MChannelProvider.bot_provider_id == channel_provider.bot_provider.id
            )
        )
        if not providers_left:
            await delete_bot_provider(
                bot_provider_id=channel_provider.bot_provider.id,
                session=session,
            )
        await fire_disconnect_channel_bot_provider(
            channel_id=channel_id,
            bot_provider=channel_provider.bot_provider,
        )
