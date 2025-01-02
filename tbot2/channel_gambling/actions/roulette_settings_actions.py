from uuid import UUID

import sqlalchemy as sa

from tbot2.contexts import AsyncSession, get_session

from ..models.roulette_settings_model import MRouletteSettings
from ..schemas.roulette_settings_schema import RouletteSettings, RouletteSettingsUpdate


async def get_roulette_settings(
    *,
    channel_id: UUID,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MRouletteSettings).where(
                MRouletteSettings.channel_id == channel_id,
            )
        )
        if not result:
            return RouletteSettings(
                channel_id=channel_id,
                win_chance=45,
                win_message='@{user}, You won {bet} {points_name} and now have {points} {points_name}',
                lose_message='@{user}, You lost {bet} {points_name} and now have {points} {points_name}',
                allin_win_message='@{user}, You won {bet} {points_name} and now have {points} {points_name}',
                allin_lose_message='@{user}, You lost {bet} {points_name} and now have {points} {points_name}',
                min_bet=5,
                max_bet=0,
            )
        return RouletteSettings.model_validate(result)


async def update_roulette_settings(
    *,
    channel_id: UUID,
    data: RouletteSettingsUpdate,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        result = await session.execute(
            sa.update(MRouletteSettings)
            .where(MRouletteSettings.channel_id == channel_id)
            .values(**data_)
        )

        if result.rowcount == 0:
            await session.execute(
                sa.insert(MRouletteSettings).values(
                    channel_id=channel_id, **data.model_dump()
                )
            )

        roulette_settings = await get_roulette_settings(
            channel_id=channel_id, session=session
        )
        if not roulette_settings:
            raise Exception('Failed to update roulette settings')
        return roulette_settings
