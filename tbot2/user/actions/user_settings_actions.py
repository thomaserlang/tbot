from typing import Any, cast
from uuid import UUID

import sqlalchemy as sa

from tbot2.contexts import AsyncSession, get_session

from ..models.user_settings_model import MUserSettings
from ..schemas.user_settings_schema import UserSettings


async def get_user_settings(
    *,
    user_id: UUID,
    session: AsyncSession | None = None,
) -> UserSettings | None:
    async with get_session(session) as session:
        settings = await session.scalar(
            sa.select(MUserSettings.settings).where(MUserSettings.user_id == user_id)
        )
        if not settings:
            return UserSettings()
        return UserSettings.model_validate(settings)


async def create_user_settings(
    *,
    user_id: UUID,
    data: UserSettings,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        await session.execute(
            sa.insert(MUserSettings).values(
                user_id=user_id,
                settings=data.model_dump(),
            )
        )


async def update_user_settings(
    *,
    user_id: UUID,
    data: UserSettings,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True, mode='json')
        if not data_:
            return

        json_set_args: list[Any] = []
        for key, value in data_.items():
            json_set_args.append(f'$.{key}')
            if isinstance(value, list):
                json_set_args.append(sa.func.json_array(*value))
            elif isinstance(value, dict):
                args: list[Any] = []
                for k, v in cast(dict[str, str | int], value.items()):
                    args += [k, v]
                json_set_args.append(sa.func.json_object(*args))
            else:
                json_set_args.append(value)
        await session.execute(
            sa.update(MUserSettings)
            .where(MUserSettings.user_id == user_id)
            .values(settings=sa.func.json_set(MUserSettings.settings, *json_set_args))
        )
