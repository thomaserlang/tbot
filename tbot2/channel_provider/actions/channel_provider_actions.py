from collections.abc import AsyncGenerator, Awaitable, Callable
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import Provider
from tbot2.common.utils.event import add_event_handler, fire_event_async
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_provider_model import (
    MChannelProvider,
)
from ..schemas.channel_provider_schema import (
    ChannelProvider,
    ChannelProviderRequest,
)


async def get_channel_provider(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_id: str | None = None,
    session: AsyncSession | None = None,
) -> ChannelProvider | None:
    async with get_session(session) as session:
        stmt = sa.select(MChannelProvider).where(
            MChannelProvider.channel_id == channel_id,
            MChannelProvider.provider == provider,
        )
        if provider_id:
            stmt = stmt.where(MChannelProvider.provider_user_id == provider_id)
        channel_provider = await session.scalar(stmt)
        if channel_provider:
            return ChannelProvider.model_validate(channel_provider)


async def get_channel_provider_by_id(
    *, channel_provider_id: UUID, session: AsyncSession | None = None
) -> ChannelProvider | None:
    async with get_session(session) as session:
        channel_provider = await session.scalar(
            sa.select(MChannelProvider).where(
                MChannelProvider.id == channel_provider_id,
            )
        )
        if channel_provider:
            return ChannelProvider.model_validate(channel_provider)


async def get_channel_providers(
    *,
    channel_id: UUID,
    provider: Provider | None = None,
    session: AsyncSession | None = None,
) -> list[ChannelProvider]:
    async with get_session(session) as session:
        stmt = sa.select(MChannelProvider).where(
            MChannelProvider.channel_id == channel_id,
        )
        if provider:
            stmt = stmt.where(MChannelProvider.provider == provider)
        channel_providers = await session.scalars(stmt)
        return [
            ChannelProvider.model_validate(provider) for provider in channel_providers
        ]


async def get_channels_providers(
    *,
    provider: Provider,
    stream_live: bool | None = None,
    session: AsyncSession | None = None,
) -> AsyncGenerator[ChannelProvider]:
    async with get_session(session) as session:
        stmt = sa.select(MChannelProvider).where(
            MChannelProvider.provider == provider,
        )
        if stream_live is not None:
            stmt = stmt.where(MChannelProvider.stream_live.is_(stream_live))

        providers = await session.stream_scalars(stmt)
        async for p in providers:
            yield ChannelProvider.model_validate(p)


async def save_channel_provider(
    *,
    channel_id: UUID,
    provider: Provider,
    data: ChannelProviderRequest,
    session: AsyncSession | None = None,
) -> ChannelProvider:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)

        r = await session.execute(
            sa.update(MChannelProvider)
            .where(
                MChannelProvider.channel_id == channel_id,
                MChannelProvider.provider == provider,
            )
            .values(**data_)
        )

        if r.rowcount == 0:
            id = uuid7()
            await session.execute(
                sa.insert(MChannelProvider).values(
                    id=id,
                    channel_id=channel_id,
                    provider=provider,
                    **data_,
                )
            )

        channel_provider = await get_channel_provider(
            channel_id=channel_id,
            provider=provider,
            session=session,
        )
        if not channel_provider:
            raise Exception('Channel provider not found')

        return ChannelProvider.model_validate(channel_provider)


async def reset_channel_provider_live_state(
    channel_id: UUID,
    provider: Provider,
    reset_channel_stream_id: bool = False,
    session: AsyncSession | None = None,
) -> ChannelProvider:
    async with get_session(session) as session:
        data = ChannelProviderRequest(
            stream_live=False,
            stream_live_at=None,
        )
        if reset_channel_stream_id:
            data.stream_id = None
            data.stream_chat_id = None

        return await save_channel_provider(
            channel_id=channel_id,
            provider=provider,
            data=data,
        )


async def delete_channel_provider(
    *, channel_provider_id: UUID, session: AsyncSession | None = None
) -> bool:
    async with get_session(session) as session:
        channel_provider = await get_channel_provider_by_id(
            channel_provider_id=channel_provider_id,
            session=session,
        )
        if not channel_provider:
            return False
        result = await session.execute(
            sa.delete(MChannelProvider).where(
                MChannelProvider.id == channel_provider_id,
            )
        )
        if result.rowcount > 0:
            await fire_event_delete_channel_provider(
                channel_provider=channel_provider,
            )
            return True
        return False


def on_delete_channel_provider(
    priority: int = 128,
) -> Callable[
    [Callable[[ChannelProvider], Awaitable[None]]],
    Callable[[ChannelProvider], Awaitable[None]],
]:
    def decorator(
        func: Callable[[ChannelProvider], Awaitable[None]],
    ) -> Callable[[ChannelProvider], Awaitable[None]]:
        add_event_handler('delete_channel_provider', func, priority)
        return func

    return decorator


async def fire_event_delete_channel_provider(
    *,
    channel_provider: ChannelProvider,
) -> None:
    await fire_event_async(
        'delete_channel_provider',
        channel_provider=channel_provider,
    )
