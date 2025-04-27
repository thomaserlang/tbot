from uuid import UUID

import sqlalchemy as sa

from tbot2.common import Provider
from tbot2.contexts import AsyncSession, get_session

from ..models.chatter_gambling_stats_model import MChatterGamblingStats
from ..schemas.chatter_gambling_stats_schema import (
    ChatterGamblingStats,
    ChatterGamblingStatsUpdate,
)


async def get_chatter_gambling_stats(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    session: AsyncSession | None = None,
) -> ChatterGamblingStats:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChatterGamblingStats).where(
                MChatterGamblingStats.channel_id == channel_id,
                MChatterGamblingStats.provider == provider,
                MChatterGamblingStats.provider_viewer_id == provider_viewer_id,
            )
        )
        if not result:
            return ChatterGamblingStats(
                channel_id=channel_id,
                provider_viewer_id=provider_viewer_id,
                provider=provider,
            )
        return ChatterGamblingStats.model_validate(result)


async def inc_chatter_gambling_stats(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    data: ChatterGamblingStatsUpdate,
) -> ChatterGamblingStats:
    async with get_session() as session:
        data_ = data.model_dump(exclude_unset=True)
        result = await session.execute(
            sa.update(MChatterGamblingStats)
            .where(
                MChatterGamblingStats.channel_id == channel_id,
                MChatterGamblingStats.provider == provider,
                MChatterGamblingStats.provider_viewer_id == provider_viewer_id,
            )
            .values(
                {k: getattr(MChatterGamblingStats, k) + v for k, v in data_.items()}
            )
        )

        if result.rowcount == 0:
            await session.execute(
                sa.insert(MChatterGamblingStats).values(
                    channel_id=channel_id,
                    provider=provider,
                    provider_viewer_id=provider_viewer_id,
                    **{k: v if v > 0 else 0 for k, v in data_.items()},
                )
            )

        chatter_gambling_stats = await get_chatter_gambling_stats(
            channel_id=channel_id,
            provider=provider,
            provider_viewer_id=provider_viewer_id,
            session=session,
        )
        if not chatter_gambling_stats:
            raise Exception('Failed to update gambling stats')
        return chatter_gambling_stats
