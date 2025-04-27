from collections.abc import Awaitable, Callable
from uuid import UUID

import sqlalchemy as sa

from tbot2.bot_providers import BotProvider, MBotProvider, delete_bot_provider
from tbot2.common import Provider
from tbot2.common.utils.event import add_event_handler, fire_event_async
from tbot2.contexts import AsyncSession, get_session

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
        if not channel_provider or not channel_provider.channel_id != channel_id:
            raise ValueError(
                f'Failed to disconnect channel bot provider {channel_provider_id}: '
                'no provider found'
            )
        if not channel_provider.bot_provider:
            raise ValueError(
                f'Failed to disconnect channel bot provider {channel_provider_id}: '
                'no bot provider found'
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


def on_disconnect_channel_bot_provider(
    priority: int = 128,
) -> Callable[
    [Callable[[UUID, BotProvider], Awaitable[None]]],
    Callable[[UUID, BotProvider], Awaitable[None]],
]:
    def decorator(
        func: Callable[[UUID, BotProvider], Awaitable[None]],
    ) -> Callable[[UUID, BotProvider], Awaitable[None]]:
        add_event_handler('disconnect_channel_bot_provider', func, priority)
        return func

    return decorator


async def fire_disconnect_channel_bot_provider(
    *,
    channel_id: UUID,
    bot_provider: BotProvider,
) -> None:
    await fire_event_async(
        'disconnect_channel_bot_provider',
        channel_id=channel_id,
        bot_provider=bot_provider,
    )
