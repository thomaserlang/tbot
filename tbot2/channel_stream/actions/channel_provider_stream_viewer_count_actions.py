from uuid import UUID

import sqlalchemy as sa

from tbot2.channel_provider import (
    ChannelProviderUpdate,
    update_channel_provider,
)
from tbot2.common import datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.channel_provider_stream_model import MChannelProviderStream
from ..models.channel_provider_stream_viewer_count_model import (
    MChannelProviderStreamViewerCount,
)
from ..models.channel_stream_model import MChannelStream


async def add_viewer_count(
    channel_provider_id: UUID,
    channel_provider_stream_id: UUID,
    viewer_count: int,
    session: AsyncSession | None = None,
) -> None:
    async with get_session(session) as session:
        await session.execute(
            sa.insert(MChannelProviderStreamViewerCount.__table__).values(  # type: ignore
                channel_provider_stream_id=channel_provider_stream_id,
                timestamp=datetime_now(),
                viewer_count=viewer_count,
            )
        )
        provider_stream_viewer_stats = (
            await session.execute(
                sa.select(
                    sa.func.avg(MChannelProviderStreamViewerCount.viewer_count).label(
                        'avg_viewer_count'
                    ),
                    sa.func.max(MChannelProviderStreamViewerCount.viewer_count).label(
                        'peak_viewer_count'
                    ),
                ).where(
                    MChannelProviderStreamViewerCount.channel_provider_stream_id
                    == channel_provider_stream_id
                )
            )
        ).first()
        if provider_stream_viewer_stats:
            await session.execute(
                sa.update(MChannelProviderStream.__table__)  # type: ignore
                .where(
                    MChannelProviderStream.id == channel_provider_stream_id,
                )
                .values(
                    avg_viewer_count=provider_stream_viewer_stats.avg_viewer_count,
                    peak_viewer_count=provider_stream_viewer_stats.peak_viewer_count,
                )
            )
            await update_channel_provider(
                channel_provider_id=channel_provider_id,
                data=ChannelProviderUpdate(
                    stream_viewer_count=viewer_count,
                ),
                session=session,
            )


async def update_channel_stream_viewer_count(channel_stream_id: UUID) -> None:
    async with get_session() as session:
        stream_viewer_stats = (
            await session.execute(
                sa.select(
                    sa.func.avg(MChannelProviderStreamViewerCount.viewer_count).label(
                        'avg_viewer_count'
                    ),
                    sa.func.max(MChannelProviderStreamViewerCount.viewer_count).label(
                        'peak_viewer_count'
                    ),
                ).where(
                    MChannelProviderStream.channel_stream_id == channel_stream_id,
                    MChannelProviderStreamViewerCount.channel_provider_stream_id
                    == MChannelProviderStream.id,
                )
            )
        ).first()
        if stream_viewer_stats:
            await session.execute(
                sa.update(MChannelStream.__table__)  # type: ignore
                .where(
                    MChannelStream.id == channel_stream_id,
                )
                .values(
                    avg_viewer_count=stream_viewer_stats.avg_viewer_count,
                    peak_viewer_count=stream_viewer_stats.peak_viewer_count,
                )
            )
