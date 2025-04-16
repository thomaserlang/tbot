from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import Provider, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_viewer_stats_model import (
    MChannelViewerStats,
)
from ..schemas.channel_viewer_schema import (
    ChannelViewerStats,
    ChannelViewerStatsUpdate,
)


async def set_channel_viewer_watched_stream(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    channel_provider_stream_id: UUID,
    session: AsyncSession | None = None,
) -> None:
    """
    Used when a viewer is detected as watching a stream.
    Updates the amount of streams they have watched and increments their in a row count.
    """
    async with get_session(session) as session:
        stats = await get_channel_viewer_stats(
            channel_id=channel_id,
            provider=provider,
            provider_viewer_id=provider_viewer_id,
            session=session,
        )
        if (
            stats.last_channel_provider_stream
            and stats.last_channel_provider_stream.id == channel_provider_stream_id
        ):
            return

        data = ChannelViewerStatsUpdate(
            streams=stats.streams + 1,
            streams_row=stats.streams_row + 1,
            last_channel_provider_stream_id=channel_provider_stream_id,
        )
        if stats.streams_row + 1 > stats.streams_row_peak:
            data.streams_row_peak = stats.streams_row + 1
            data.streams_row_peak_date = datetime_now().date()

        await update_channel_viewer_stats(
            channel_id=channel_id,
            provider=provider,
            provider_viewer_id=provider_viewer_id,
            data=data,
            session=session,
        )


async def get_channel_viewer_stats(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    session: AsyncSession | None = None,
) -> ChannelViewerStats:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelViewerStats).where(
                MChannelViewerStats.channel_id == channel_id,
                MChannelViewerStats.provider == provider,
                MChannelViewerStats.provider_viewer_id == provider_viewer_id,
            )
        )
        if result:
            return ChannelViewerStats.model_validate(result)
        else:
            return ChannelViewerStats(
                channel_id=channel_id,
                provider=provider,
                provider_viewer_id=provider_viewer_id,
            )


async def update_channel_viewer_stats(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    data: ChannelViewerStatsUpdate,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        result = await session.execute(
            sa.update(MChannelViewerStats)
            .where(
                MChannelViewerStats.channel_id == channel_id,
                MChannelViewerStats.provider == provider,
                MChannelViewerStats.provider_viewer_id == provider_viewer_id,
            )
            .values(
                **data.model_dump(
                    exclude_unset=True,
                )
            )
        )
        if not result.rowcount:
            await session.execute(
                sa.insert(MChannelViewerStats).values(
                    id=uuid7(),
                    channel_id=channel_id,
                    provider=provider,
                    provider_viewer_id=provider_viewer_id,
                    **data.model_dump(),
                )
            )
