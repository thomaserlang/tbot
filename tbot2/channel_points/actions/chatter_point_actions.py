from uuid import UUID

import sqlalchemy as sa

from tbot2.common import TProvider
from tbot2.contexts import AsyncSession, get_session

from ..models.chatter_points_model import MChatterPoints
from ..schemas.chatter_points_schema import ChatterPoints


async def get_points(
    *,
    channel_id: UUID,
    provider: TProvider,
    chatter_id: str,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatterPoints).where(
                MChatterPoints.channel_id == channel_id,
                MChatterPoints.provider == provider,
                MChatterPoints.chatter_id == chatter_id,
            )
        )
        if not result:
            return ChatterPoints(
                channel_id=channel_id,
                chatter_id=chatter_id,
                provider=provider,
                points=0,
            )
        return ChatterPoints.model_validate(result)


async def inc_points(
    *,
    channel_id: UUID,
    provider: TProvider,
    chatter_id: str,
    points: int,
    session: AsyncSession | None = None,
):
    async with get_session(session) as session:
        result = await session.execute(
            sa.update(MChatterPoints)
            .where(
                MChatterPoints.channel_id == channel_id,
                MChatterPoints.provider == provider,
                MChatterPoints.chatter_id == chatter_id,
            )
            .values(
                points=sa.func.if_(
                    MChatterPoints.points + points > 0,
                    MChatterPoints.points + points,
                    0,
                )
            )
        )

        if result.rowcount == 0:
            await session.execute(
                sa.insert(MChatterPoints).values(
                    channel_id=channel_id,
                    provider=provider,
                    chatter_id=chatter_id,
                    points=points if points > 0 else 0,
                )
            )

        return await get_points(
            channel_id=channel_id,
            provider=provider,
            chatter_id=chatter_id,
            session=session,
        )
