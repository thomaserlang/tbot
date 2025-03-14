from datetime import datetime, timezone
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from uuid6 import uuid7

from tbot2.contexts import AsyncSession, get_session

from ..models.oauth_provider_model import MOAuthProvider
from ..schemas.oauth_provider_schema import (
    OAuthProvider,
    OAuthProviderCreate,
    OAuthProviderUpdate,
)


async def create_oauth_provider(
    *, data: OAuthProviderCreate, session: AsyncSession | None = None
) -> OAuthProvider:
    async with get_session(session) as session:
        try:
            provider_id = uuid7()
            await session.execute(
                sa.insert(MOAuthProvider.__table__).values(  # type: ignore
                    id=provider_id,
                    created_at=datetime.now(tz=timezone.utc),
                    **data.model_dump(),
                )
            )
            provider = await get_oauth_provider(
                provider_id=provider_id, session=session
            )
            if not provider:
                raise Exception('OAuth provider could not be created')
            return OAuthProvider.model_validate(provider)

        except IntegrityError:
            provider = await get_oauth_provider_by_user_and_provider(
                user_id=data.user_id, provider=data.provider, session=session
            )
            if provider:
                raise ValueError(
                    f"OAuth provider '{data.provider}' already connected for this user"
                )

            provider = await get_oauth_provider_by_provider_user_id(
                provider=data.provider,
                provider_user_id=data.provider_user_id,
                session=session,
            )
            if provider:
                raise ValueError(
                    f'This {data.provider} account is already connected to a different user'
                )

            raise


async def get_oauth_provider(
    *, provider_id: UUID, session: AsyncSession | None = None
) -> OAuthProvider | None:
    async with get_session(session) as session:
        provider = await session.scalar(
            sa.select(MOAuthProvider).where(MOAuthProvider.id == provider_id)
        )
        if not provider:
            return None
        return OAuthProvider.model_validate(provider)


async def get_oauth_provider_by_user_and_provider(
    *, user_id: UUID, provider: str, session: AsyncSession | None = None
) -> OAuthProvider | None:
    async with get_session(session) as session:
        p = await session.scalar(
            sa.select(MOAuthProvider).where(
                MOAuthProvider.user_id == user_id,
                MOAuthProvider.provider == provider,
            )
        )
        if not p:
            return None
        return OAuthProvider.model_validate(p)


async def get_oauth_provider_by_provider_user_id(
    *, provider: str, provider_user_id: str, session: AsyncSession | None = None
) -> OAuthProvider | None:
    async with get_session(session) as session:
        p = await session.scalar(
            sa.select(MOAuthProvider).where(
                MOAuthProvider.provider == provider,
                MOAuthProvider.provider_user_id == provider_user_id,
            )
        )
        if not p:
            return None
        return OAuthProvider.model_validate(p)


async def get_oauth_providers_by_user(
    *, user_id: UUID, session: AsyncSession | None = None
) -> list[OAuthProvider]:
    async with get_session(session) as session:
        providers = await session.scalars(
            sa.select(MOAuthProvider).where(MOAuthProvider.user_id == user_id)
        )
        return [OAuthProvider.model_validate(provider) for provider in providers]


async def update_oauth_provider(
    *, provider_id: UUID, data: OAuthProviderUpdate, session: AsyncSession | None = None
) -> OAuthProvider:
    async with get_session(session) as session:
        await session.execute(
            sa.update(MOAuthProvider.__table__)  # type: ignore
            .where(MOAuthProvider.id == provider_id)
            .values(
                updated_at=datetime.now(tz=timezone.utc),
                **data.model_dump(exclude_unset=True, exclude_defaults=True),
            )
        )
        provider = await get_oauth_provider(provider_id=provider_id, session=session)
        if not provider:
            raise ValueError('OAuth provider could not be updated')
        return OAuthProvider.model_validate(provider)


async def delete_oauth_provider(
    *, provider_id: UUID, session: AsyncSession | None = None
) -> bool:
    async with get_session(session) as session:
        result = await session.execute(
            sa.delete(MOAuthProvider.__table__).where(MOAuthProvider.id == provider_id)  # type: ignore
        )
        return result.rowcount > 0
