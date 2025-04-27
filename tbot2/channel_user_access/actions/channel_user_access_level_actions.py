from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import TAccessLevel
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_user_access_levels_model import MChannelUserAccessLevel
from ..schemas.channel_user_access_level_schemas import ChannelUserAccessLevel


async def get_channel_user_access_level(
    *,
    channel_id: UUID,
    user_id: UUID,
    session: AsyncSession | None = None,
) -> ChannelUserAccessLevel | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelUserAccessLevel).where(
                MChannelUserAccessLevel.channel_id == channel_id,
                MChannelUserAccessLevel.user_id == user_id,
            )
        )
        if result:
            return ChannelUserAccessLevel.model_validate(result)
        return None


async def get_channel_user_access_level_by_id(
    *,
    channel_user_access_id: UUID,
    session: AsyncSession | None = None,
) -> ChannelUserAccessLevel | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelUserAccessLevel).where(
                MChannelUserAccessLevel.id == channel_user_access_id,
            )
        )
        if result:
            return ChannelUserAccessLevel.model_validate(result)


async def set_channel_user_access_level(
    *,
    channel_id: UUID,
    user_id: UUID,
    access_level: TAccessLevel,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        result = await session.execute(
            sa.insert(MChannelUserAccessLevel)
            .values(
                id=uuid7(),
                channel_id=channel_id,
                user_id=user_id,
                access_level=access_level.value,
            )
            .prefix_with('IGNORE')
        )

        if result.rowcount == 0:
            await session.execute(
                sa.update(MChannelUserAccessLevel)
                .where(
                    MChannelUserAccessLevel.channel_id == channel_id,
                    MChannelUserAccessLevel.user_id == user_id,
                )
                .values(access_level=access_level.value)
            )


async def delete_channel_user_access_level(
    *,
    channel_user_access_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        result = await session.execute(
            sa.delete(MChannelUserAccessLevel).where(
                MChannelUserAccessLevel.id == channel_user_access_id
            )
        )
        return result.rowcount > 0
