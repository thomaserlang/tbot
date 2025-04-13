from uuid import UUID

import sqlalchemy as sa

from tbot2.chatlog import ChatterRequest, save_chatters
from tbot2.contexts import AsyncSession, get_session

from ..actions.channel_provider_stream_actions import (
    get_channel_provider_stream,
)
from ..actions.channel_viewer_stats_actions import (
    set_channel_viewer_watched_stream,
)
from ..models.channel_provider_viewer_watchtime_model import (
    MChannelProviderStreamViewerWatchtime,
)
from ..schemas.stream_viewer_watchtime_schema import StreamViewerWatchtime


async def get_stream_viewer_watchtime(
    *,
    channel_provider_stream_id: UUID,
    provider_viewer_id: str,
    session: AsyncSession | None = None,
) -> StreamViewerWatchtime | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MChannelProviderStreamViewerWatchtime).where(
                MChannelProviderStreamViewerWatchtime.channel_provider_stream_id
                == channel_provider_stream_id,
                MChannelProviderStreamViewerWatchtime.provider_viewer_id
                == provider_viewer_id,
            )
        )
        if result:
            return StreamViewerWatchtime.model_validate(result)


async def inc_stream_viewer_watchtime(
    *,
    channel_provider_stream_id: UUID,
    provider_viewers: list[ChatterRequest],
    watchtime: int,
    session: AsyncSession | None = None,
) -> None:
    """
    Bulk update the watchtime of viewers of a stream.
    This will in turn also update the channel viewer stats for each viewer.

    TODO: Need a better bulk way of updating the channel viewer stats.

    Args:
        watchtime: Amount of seconds to add
    """
    async with get_session(session) as session:
        stream = await get_channel_provider_stream(
            channel_provider_stream_id=channel_provider_stream_id, session=session
        )
        chatter_ids = {viewer.chatter_id for viewer in provider_viewers}
        if not stream:
            raise ValueError(
                f'Channel provider stream {channel_provider_stream_id} not found'
            )
        r = await session.execute(
            sa.update(MChannelProviderStreamViewerWatchtime.__table__)  # type: ignore
            .where(
                MChannelProviderStreamViewerWatchtime.channel_provider_stream_id
                == channel_provider_stream_id,
                MChannelProviderStreamViewerWatchtime.provider_viewer_id.in_(
                    chatter_ids
                ),
            )
            .values(
                watchtime=MChannelProviderStreamViewerWatchtime.watchtime + watchtime
            )
        )
        if r.rowcount != len(provider_viewers):
            # Find the viewers that are new for the stream
            existing_viewer_ids = await session.scalars(
                sa.select(
                    MChannelProviderStreamViewerWatchtime.provider_viewer_id
                ).where(
                    MChannelProviderStreamViewerWatchtime.channel_provider_stream_id
                    == channel_provider_stream_id,
                    MChannelProviderStreamViewerWatchtime.provider_viewer_id.in_(
                        chatter_ids
                    ),
                )
            )
            new_viewer_ids = chatter_ids - set(existing_viewer_ids)
            await session.execute(
                sa.insert(MChannelProviderStreamViewerWatchtime.__table__).values(  # type: ignore
                    [
                        {
                            'channel_provider_stream_id': channel_provider_stream_id,  # noqa: E501
                            'provider_viewer_id': viewer_id,
                            'watchtime': watchtime,
                        }
                        for viewer_id in new_viewer_ids
                    ]
                )
            )
            for provider_viewer_id in new_viewer_ids:
                await set_channel_viewer_watched_stream(
                    channel_id=stream.channel_id,
                    provider=stream.provider,
                    provider_viewer_id=provider_viewer_id,
                    channel_provider_stream_id=stream.id,
                    session=session,
                )

            await save_chatters(
                provider=stream.provider,
                chatters=[
                    ChatterRequest(
                        chatter_id=viewer.chatter_id,
                        chatter_name=viewer.chatter_name,
                        chatter_display_name=viewer.chatter_display_name,
                    )
                    for viewer in provider_viewers
                    if viewer.chatter_id in new_viewer_ids
                ],
                session=session,
            )
