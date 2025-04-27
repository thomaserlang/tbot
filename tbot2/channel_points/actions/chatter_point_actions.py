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
    provider_viewer_id: str,
    session: AsyncSession | None = None,
) -> ChatterPoints:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatterPoints).where(
                MChatterPoints.channel_id == channel_id,
                MChatterPoints.provider == provider,
                MChatterPoints.provider_viewer_id == provider_viewer_id,
            )
        )
        if not result:
            return ChatterPoints(
                channel_id=channel_id,
                provider_viewer_id=provider_viewer_id,
                provider=provider,
                points=0,
            )
        return ChatterPoints.model_validate(result)


async def get_points_rank(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
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
                MChatterPoints.provider_viewer_id,
            )
            .where(
                MChatterPoints.channel_id == channel_id,
                MChatterPoints.provider == provider,
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
                    MChatterPoints.provider_viewer_id == provider_viewer_id,
                    sub_rank.c.provider_viewer_id == MChatterPoints.provider_viewer_id,
                )
            )
        ).first()

        if result:
            cpr = ChatterPointsRank.model_validate(result[0])
            cpr.rank = result.rank
            return cpr


async def get_total_point_users(
    *,
    channel_id: UUID,
    provider: Provider,
    session: AsyncSession | None = None,
) -> int:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(sa.func.count('*')).where(
                MChatterPoints.channel_id == channel_id,
                MChatterPoints.provider == provider,
            )
        )
        return result if result else 0


async def inc_points(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    points: int,
    session: AsyncSession | None = None,
) -> ChatterPoints:
    async with get_session(session) as session:
        result = await session.execute(
            sa.update(MChatterPoints)
            .where(
                MChatterPoints.channel_id == channel_id,
                MChatterPoints.provider == provider,
                MChatterPoints.provider_viewer_id == provider_viewer_id,
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
                    provider_viewer_id=provider_viewer_id,
                    points=points if points > 0 else 0,
                )
            )

        return await get_points(
            channel_id=channel_id,
            provider=provider,
            provider_viewer_id=provider_viewer_id,
            session=session,
        )


async def inc_bulk_points(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_ids: list[str],
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
                        'provider_viewer_id': provider_viewer_id,
                        'points': points if points > 0 else 0,
                    }
                    for provider_viewer_id in provider_viewer_ids
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
