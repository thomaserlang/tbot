from uuid import UUID

import sqlalchemy as sa
from more_itertools import chunked

from tbot2.contexts import AsyncSession, get_session

from ..actions.channel_viewer_stats_actions import (
    set_channel_viewer_watched_stream,
)
from ..models.stream_viewer_watchtime_model import (
    MStreamViewerWatchtime,
)
from ..schemas.stream_viewer_watchtime_schema import StreamViewerWatchtime


async def get_stream_viewer_watchtime(
    *,
    channel_id: UUID,
    provider: str,
    stream_id: str,
    viewer_id: str,
    session: AsyncSession | None = None,
) -> StreamViewerWatchtime | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MStreamViewerWatchtime).where(
                MStreamViewerWatchtime.channel_id == channel_id,
                MStreamViewerWatchtime.provider == provider,
                MStreamViewerWatchtime.stream_id == stream_id,
                MStreamViewerWatchtime.viewer_id == viewer_id,
            )
        )
        if result:
            return StreamViewerWatchtime.model_validate(result)


async def inc_stream_viewer_watchtime(
    *,
    channel_id: UUID,
    provider: str,
    stream_id: str,
    viewer_ids: set[str],
    watchtime: int,
    session: AsyncSession | None = None,
) -> None:
    """
    Bulk update the watchtime of viewers of a stream.
    This will in turn also update the channel viewer stats for each viewer.

    TODO: Need a better bulk way of updating the channel viewer stats.
    """
    async with get_session(session) as session:
        for viewer_ids_ in chunked(viewer_ids, 1000):
            r = await session.execute(
                sa.update(MStreamViewerWatchtime.__table__)  # type: ignore
                .where(
                    MStreamViewerWatchtime.channel_id == channel_id,
                    MStreamViewerWatchtime.provider == provider,
                    MStreamViewerWatchtime.stream_id == stream_id,
                    MStreamViewerWatchtime.viewer_id.in_(viewer_ids_),
                )
                .values(watchtime=MStreamViewerWatchtime.watchtime + watchtime)
            )
            if r.rowcount != len(viewer_ids_):
                # Find the viewers that are new for the stream
                existing_viewer_ids = await session.scalars(
                    sa.select(MStreamViewerWatchtime.viewer_id).where(
                        MStreamViewerWatchtime.channel_id == channel_id,
                        MStreamViewerWatchtime.provider == provider,
                        MStreamViewerWatchtime.stream_id == stream_id,
                        MStreamViewerWatchtime.viewer_id.in_(viewer_ids_),
                    )
                )
                new_viewer_ids = set(viewer_ids_) - set(existing_viewer_ids)

                await session.execute(
                    sa.insert(MStreamViewerWatchtime.__table__).values(  # type: ignore
                        [
                            {
                                'channel_id': channel_id,
                                'provider': provider,
                                'stream_id': stream_id,
                                'viewer_id': viewer_id,
                                'watchtime': watchtime,
                            }
                            for viewer_id in new_viewer_ids
                        ]
                    )
                )
                for viewer_id in new_viewer_ids:
                    await set_channel_viewer_watched_stream(
                        channel_id=channel_id,
                        provider=provider,
                        viewer_id=viewer_id,
                        stream_id=stream_id,
                        session=session,
                    )
