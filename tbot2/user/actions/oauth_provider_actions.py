from dataclasses import dataclass
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from uuid6 import uuid7

from tbot2.channel import (
    Channel,
    ChannelCreate,
    create_channel,
)
from tbot2.common import (
    ErrorMessage,
    Provider,
    Scope,
    TAccessLevel,
    TokenData,
    datetime_now,
)
from tbot2.contexts import AsyncSession, get_session

from ..models.oauth_provider_model import MUserOAuthProvider
from ..schemas.oauth_provider_schema import (
    UserOAuthProvider,
)
from ..schemas.user_schema import User, UserCreate, UserUpdate
from .user_actions import create_user, get_user, update_user


@dataclass(slots=True)
class GetOrCreateUserResult:
    user: User
    channel: Channel | None
    created: bool
    token_data: TokenData


async def get_or_create_user(
    *,
    provider: Provider,
    provider_user_id: str,
    data: UserCreate,
    session: AsyncSession | None = None,
) -> GetOrCreateUserResult:
    """
    Returns a tuple of TokenData and a boolean indicating if the user was created.
    """
    from tbot2.channel_user_access import set_channel_user_access_level

    async with get_session(session) as session:
        p = await get_oauth_provider_by_provider_user_id(
            provider=provider,
            provider_user_id=provider_user_id,
            session=session,
        )
        if not p:
            user = await create_user(
                data=data,
                session=session,
            )
            await create_user_oauth_provider(
                user_id=user.id,
                provider=provider,
                provider_user_id=provider_user_id,
                session=session,
            )

            channel = await create_channel(
                data=ChannelCreate(
                    display_name=data.display_name,
                ),
                session=session,
            )
            await set_channel_user_access_level(
                channel_id=channel.id,
                user_id=user.id,
                access_level=TAccessLevel.OWNER,
                session=session,
            )
            await update_user(
                user_id=user.id,
                data=UserUpdate(
                    default_channel_id=channel.id,
                ),
                session=session,
            )
            return GetOrCreateUserResult(
                user=user,
                channel=channel,
                created=True,
                token_data=TokenData(
                    user_id=user.id,
                    scopes=Scope.get_all_scopes(),
                ),
            )
        user = await get_user(user_id=p.user_id, session=session)
        if not user:
            raise Exception('User not found')
        return GetOrCreateUserResult(
            user=user,
            channel=None,
            created=False,
            token_data=TokenData(
                user_id=user.id,
                scopes=Scope.get_all_scopes(),
            ),
        )


async def create_user_oauth_provider(
    *,
    user_id: UUID,
    provider: Provider,
    provider_user_id: str,
    session: AsyncSession | None = None,
) -> UserOAuthProvider:
    async with get_session(session) as session:
        try:
            user_oauth_provider_id = uuid7()
            await session.execute(
                sa.insert(MUserOAuthProvider.__table__).values(  # type: ignore
                    id=user_oauth_provider_id,
                    created_at=datetime_now(),
                    user_id=user_id,
                    provider=provider,
                    provider_user_id=provider_user_id,
                )
            )
            p = await get_user_oauth_provider(
                user_oauth_provider_id=user_oauth_provider_id,
                session=session,
            )
            if not p:
                raise Exception('OAuth provider could not be created')
            return UserOAuthProvider.model_validate(p)

        except IntegrityError:
            p = await get_oauth_provider_by_user_and_provider(
                user_id=user_id, provider=provider, session=session
            )
            if p:
                raise ErrorMessage(
                    f'{provider} already connected for this user',
                    code=400,
                    type='oauth_provider_already_connected',
                ) from None

            p = await get_oauth_provider_by_provider_user_id(
                provider=provider,
                provider_user_id=provider_user_id,
                session=session,
            )
            if p:
                raise ErrorMessage(
                    f'{provider} already connected to a different user',
                    code=400,
                    type='oauth_provider_already_connected',
                ) from None

            raise


async def get_user_oauth_provider(
    *,
    user_oauth_provider_id: UUID,
    session: AsyncSession | None = None,
) -> UserOAuthProvider | None:
    async with get_session(session) as session:
        provider = await session.scalar(
            sa.select(MUserOAuthProvider).where(
                MUserOAuthProvider.id == user_oauth_provider_id
            )
        )
        if not provider:
            return None
        return UserOAuthProvider.model_validate(provider)


async def get_oauth_provider_by_user_and_provider(
    *, user_id: UUID, provider: Provider, session: AsyncSession | None = None
) -> UserOAuthProvider | None:
    async with get_session(session) as session:
        p = await session.scalar(
            sa.select(MUserOAuthProvider).where(
                MUserOAuthProvider.user_id == user_id,
                MUserOAuthProvider.provider == provider,
            )
        )
        if not p:
            return None
        return UserOAuthProvider.model_validate(p)


async def get_oauth_provider_by_provider_user_id(
    *,
    provider: Provider,
    provider_user_id: str,
    session: AsyncSession | None = None,
) -> UserOAuthProvider | None:
    async with get_session(session) as session:
        p = await session.scalar(
            sa.select(MUserOAuthProvider).where(
                MUserOAuthProvider.provider == provider,
                MUserOAuthProvider.provider_user_id == provider_user_id,
            )
        )
        if not p:
            return None
        return UserOAuthProvider.model_validate(p)


async def get_oauth_providers_by_user(
    *,
    user_id: UUID,
    session: AsyncSession | None = None,
) -> list[UserOAuthProvider]:
    async with get_session(session) as session:
        providers = await session.scalars(
            sa.select(MUserOAuthProvider).where(MUserOAuthProvider.user_id == user_id)
        )
        return [UserOAuthProvider.model_validate(provider) for provider in providers]


async def delete_oauth_provider(
    *,
    provider_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        result = await session.execute(
            sa.delete(MUserOAuthProvider.__table__).where(  # type: ignore
                MUserOAuthProvider.id == provider_id,
            )
        )
        return result.rowcount > 0
