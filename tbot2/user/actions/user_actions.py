from datetime import datetime, timezone
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from uuid6 import uuid7

from tbot2.contexts import AsyncSession, get_session

from ..models.user_model import MUser
from ..schemas.user_schema import User, UserCreate, UserUpdate


async def get_user(
    *, user_id: UUID, session: AsyncSession | None = None
) -> User | None:
    async with get_session(session) as session:
        user = await session.scalar(sa.select(MUser).where(MUser.id == user_id))
        if not user:
            return None
        return User.model_validate(user)


async def get_user_by_email(
    *, email: str, session: AsyncSession | None = None
) -> User | None:
    async with get_session(session) as session:
        user = await session.scalar(sa.select(MUser).where(MUser.email == email))
        if not user:
            return None
        return User.model_validate(user)


async def get_user_by_username(
    *, username: str, session: AsyncSession | None = None
) -> User | None:
    async with get_session(session) as session:
        user = await session.scalar(sa.select(MUser).where(MUser.username == username))
        if not user:
            return None
        return User.model_validate(user)


async def create_user(
    *,
    data: UserCreate,
    session: AsyncSession | None = None,
) -> User:
    async with get_session(session) as session:
        try:
            user_id = uuid7()
            result = await session.execute(
                sa.insert(MUser).values(
                    id=user_id,
                    created_at=datetime.now(tz=timezone.utc),
                    **data.model_dump(),
                )
            )
            user = await get_user(user_id=user_id, session=session)
            if not user:
                raise ValueError('User could not be created')

            return user
        except IntegrityError:
            result = await session.scalar(
                sa.select(MUser.id).where(MUser.username == data.username)
            )
            if result:
                raise ValueError(f"Username '{data.username}' already exists")

            result = await session.scalar(
                sa.select(MUser.id).where(MUser.email == data.email)
            )
            if result:
                raise ValueError(f"Email '{data.email}' already exists")

            raise


async def update_user(
    *, user_id: UUID, data: UserUpdate, session: AsyncSession | None = None
) -> User:
    async with get_session(session) as session:
        try:
            await session.execute(
                sa.update(MUser)
                .where(MUser.id == user_id)
                .values(
                    updated_at=datetime.now(tz=timezone.utc),
                    **data.model_dump(exclude_defaults=True),
                )
            )
            user = await get_user(user_id=user_id, session=session)
            if not user:
                raise ValueError('User could not be updated')
            return user
        except IntegrityError:
            if data.username:
                user = await get_user_by_username(
                    username=data.username, session=session
                )
                if user:
                    raise ValueError(f"Username '{data.username}' already exists")

            if data.email:
                user = await get_user_by_email(email=data.email, session=session)
                if user:
                    raise ValueError(f"Email '{data.email}' already exists")

            user = await get_user(user_id=user_id, session=session)
            if not user:
                raise ValueError('User could not be updated')

            raise
