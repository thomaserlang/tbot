from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert

from tbot2.common import Provider
from tbot2.contexts import AsyncSession, get_session

from ..models.chatter_points_model import MChatterPoints
from ..schemas.chatter_points_schema import ChatterPoints, ChatterPointsRank


async def get_points(
    *,
    channel_id: UUID,
    provider: Provider,
    chatter_id: str,
    session: AsyncSession | None = None,
) -> ChatterPoints:
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


async def get_points_rank(
    *,
    channel_id: UUID,
    provider: Provider,
    chatter_id: str,
    session: AsyncSession | None = None,
) -> ChatterPointsRank | None:
    async with get_session(session) as session:
        sub_rank = (
            sa.select(
                sa.func.rank()
                .over(
                    order_by=MChatterPoints.points.desc(),
                    partition_by=MChatterPoints.channel_id,
                )
                .label('rank'),
                MChatterPoints.chatter_id,
            )
            .where(
                MChatterPoints.channel_id == channel_id,
            )
            .subquery()
        )
        result = (
            await session.execute(
                sa.select(
                    MChatterPoints,
                    sub_rank.c.rank,
                ).where(
                    MChatterPoints.channel_id == channel_id,
                    MChatterPoints.provider == provider,
                    MChatterPoints.chatter_id == chatter_id,
                    sub_rank.c.chatter_id == MChatterPoints.chatter_id,
                )
            )
        ).first()

        if result:
            cpr = ChatterPointsRank.model_validate(result[0])
            cpr.rank = result.rank
            return cpr


async def inc_points(
    *,
    channel_id: UUID,
    provider: Provider,
    chatter_id: str,
    points: int,
    session: AsyncSession | None = None,
) -> ChatterPoints:
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


async def inc_bulk_points(
    *,
    channel_id: UUID,
    provider: Provider,
    chatter_ids: list[str],
    points: int,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        await session.execute(
            insert(MChatterPoints)
            .values(
                [
                    {
                        'channel_id': channel_id,
                        'provider': provider,
                        'chatter_id': chatter_id,
                        'points': points if points > 0 else 0,
                    }
                    for chatter_id in chatter_ids
                ]
            )
            .on_duplicate_key_update(
                points=sa.func.if_(
                    MChatterPoints.points + points > 0,
                    MChatterPoints.points + points,
                    0,
                )
            )
        )
