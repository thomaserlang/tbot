from uuid import UUID

import sqlalchemy as sa

from tbot2.contexts import AsyncSession, get_session

from ..models.channel_point_settings_model import (
    MChannelPointSettings,
)
from ..schemas.channel_point_settings_schema import (
    ChannelPointSettings,
    ChannelPointSettingsUpdate,
)


async def get_channel_point_settings(
    *,
    channel_id: UUID,
    session: AsyncSession | None = None,
) -> ChannelPointSettings:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelPointSettings).where(
                MChannelPointSettings.channel_id == channel_id
            )
        )
        if not result:
            return ChannelPointSettings(
                channel_id=channel_id,
            )
        return ChannelPointSettings.model_validate(result)


async def update_channel_point_settings(
    *,
    channel_id: UUID,
    data: ChannelPointSettingsUpdate,
    session: AsyncSession | None = None,
) -> ChannelPointSettings:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        result = await session.execute(
            sa.update(MChannelPointSettings)
            .where(MChannelPointSettings.channel_id == channel_id)
            .values(**data_)
        )

        if result.rowcount == 0:
            await session.execute(
                sa.insert(MChannelPointSettings).values(
                    channel_id=channel_id, **data.model_dump()
                )
            )

        channel_point_settings = await get_channel_point_settings(
            channel_id=channel_id, session=session
        )
        if not channel_point_settings:
            raise Exception('Failed to update channel point settings')
        return channel_point_settings
