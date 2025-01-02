from uuid import UUID

import sqlalchemy as sa

from tbot2.contexts import AsyncSession, get_session

from ..models.slots_settings_model import MSlotsSettings
from ..schemas.slots_settings_schema import SlotsSettings, SlotsSettingsUpdate


async def get_slots_settings(
    *,
    channel_id: UUID,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MSlotsSettings).where(MSlotsSettings.channel_id == channel_id)
        )
        if not result:
            return SlotsSettings(
                channel_id=channel_id,
                emotes=['MrDestructoid', 'SeriousSloth', 'OSFrog', 'OhMyDog'],
                emote_pool_size=3,
                payout_percent=95,
                min_bet=5,
                max_bet=0,
                win_message='@{user} {emotes} you won {bet} {points_name} and now have {points} {points_name}',
                lose_message='@{user} {emotes} you lost {bet} {points_name}',
                allin_win_message='@{user} {emotes} you WON {bet} {points_name} and now have {points} {points_name} EZ',
                allin_lose_message='@{user} {emotes} you lost {bet} {points_name} PepeLaugh',
            )
        return SlotsSettings.model_validate(result)


async def update_slots_settings(
    *,
    channel_id: UUID,
    data: SlotsSettingsUpdate,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        result = await session.execute(
            sa.update(MSlotsSettings)
            .where(MSlotsSettings.channel_id == channel_id)
            .values(**data_)
        )

        if result.rowcount == 0:
            await session.execute(
                sa.insert(MSlotsSettings).values(
                    channel_id=channel_id, **data.model_dump()
                )
            )

        slots_settings = await get_slots_settings(
            channel_id=channel_id, session=session
        )
        if not slots_settings:
            raise Exception('Failed to update slots settings')
        return slots_settings
