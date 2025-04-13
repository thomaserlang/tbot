from datetime import timedelta
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import Provider, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.bot_provider_model import MBotProvider
from ..schemas.bot_provider_schemas import (
    BotProvider,
    BotProviderRequest,
)


async def get_bot_provider_by_provider_user_id(
    *,
    provider: Provider,
    provider_user_id: str,
    session: AsyncSession | None = None,
) -> BotProvider | None:
    async with get_session(session) as session:
        bot_provider = await session.scalar(
            sa.select(MBotProvider).where(
                MBotProvider.provider == provider,
                MBotProvider.provider_user_id == provider_user_id,
            )
        )
        if bot_provider:
            return BotProvider.model_validate(bot_provider)


async def get_system_bot_provider(
    *,
    provider: Provider,
    session: AsyncSession | None = None,
) -> BotProvider | None:
    async with get_session(session) as session:
        bot_provider = await session.scalar(
            sa.select(MBotProvider).where(
                MBotProvider.provider == provider,
                MBotProvider.system_default.is_(True),
            )
        )
        if bot_provider:
            return BotProvider.model_validate(bot_provider)


async def save_bot_provider(
    *,
    data: BotProviderRequest,
    session: AsyncSession | None = None,
) -> BotProvider:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        if 'expires_in' in data_:
            data_.pop('expires_in')
            if not data.expires_at and data.expires_in:
                data_['expires_at'] = datetime_now() + timedelta(
                    seconds=data.expires_in
                )

        if data.system_default:
            await session.execute(
                sa.update(MBotProvider)
                .where(
                    MBotProvider.provider == data.provider,
                    MBotProvider.provider_user_id != data.provider_user_id,
                    MBotProvider.system_default.is_(True),
                )
                .values(system_default=None)
            )

        r = await session.execute(
            sa.update(MBotProvider)
            .where(
                MBotProvider.provider == data.provider,
                MBotProvider.provider_user_id == data.provider_user_id,
            )
            .values(**data_)
        )

        if r.rowcount == 0:
            id = uuid7()
            await session.execute(
                sa.insert(MBotProvider).values(
                    id=id,
                    **data_,
                )
            )

        bot_provider = await get_bot_provider_by_provider_user_id(
            provider=data.provider,
            provider_user_id=data.provider_user_id,
            session=session,
        )
        if not bot_provider:
            raise Exception('Failed to create bot provider')
        return bot_provider


async def delete_bot_provider(
    *,
    bot_provider_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        result = await session.execute(
            sa.delete(MBotProvider).where(MBotProvider.id == bot_provider_id)
        )
        return result.rowcount > 0
