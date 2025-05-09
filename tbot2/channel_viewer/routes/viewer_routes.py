from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Security
from pydantic import StringConstraints

from tbot2.channel_stream import MChannelProviderStream
from tbot2.common import Feature, Provider, TAccessLevel, TokenData
from tbot2.contexts import get_session
from tbot2.dependecies import authenticated
from tbot2.page_cursor import (
    PageCursor,
    PageCursorQueryDep,
    page_cursor,
)

from ..actions.channel_viewer_actions import (
    get_channel_viewer_stats,
)
from ..actions.provider_viewer_name_actions import get_viewer_name
from ..models.channel_provider_viewer_watchtime_model import (
    MChannelProviderStreamViewerWatchtime,
)
from ..models.provider_viewer_name_history_model import MProviderViewerNameHistory
from ..schemas.channel_viewer_schema import ChannelViewer, ViewerStream
from ..schemas.viewer_schemas import ViewerName
from ..types import ChannelViewerScope

router = APIRouter()


@router.get('/viewer-search', name='Viewer Search')
async def get_viewer_search_route(
    query: Annotated[
        str, StringConstraints(min_length=2, max_length=100, strip_whitespace=True)
    ],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelViewerScope.READ])
    ],
) -> list[ViewerName]:
    if len(query) < 3:
        return []

    async with get_session() as session:
        result = await session.scalars(
            sa.select(MProviderViewerNameHistory)
            .where(sa.or_(MProviderViewerNameHistory.display_name.ilike(f'{query}%')))
            .limit(20)
            .order_by(MProviderViewerNameHistory.last_seen_at.desc())
        )
        return [ViewerName.model_validate(row) for row in result.all()]


@router.get(
    '/channels/{channel_id}/viewers/{provider}/{provider_viewer_id}', name='Viewer info'
)
async def get_channel_viewer_route(
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelViewerScope.READ])
    ],
) -> ChannelViewer:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    viewer = await get_viewer_name(
        provider=provider,
        provider_viewer_id=provider_viewer_id,
    )
    if not viewer:
        raise HTTPException(
            status_code=404,
            detail='Viewer not found',
        )

    stats = await get_channel_viewer_stats(
        channel_id=channel_id,
        provider=provider,
        provider_viewer_id=viewer.provider_viewer_id,
    )

    return ChannelViewer(
        viewer=viewer,
        stats=stats,
    )


@router.get(
    '/channels/{channel_id}/viewers/{provider}/{provider_viewer_id}/streams',
    name='Viewer watched streams',
)
async def get_channel_viewer_streams_route(
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    page_query: PageCursorQueryDep,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelViewerScope.READ])
    ],
) -> PageCursor[ViewerStream]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
        feature=Feature.CHANNEL_VIEWER_EXTRA_STATS,
    )

    stmt = (
        sa.select(MChannelProviderStream, MChannelProviderStreamViewerWatchtime)
        .where(
            MChannelProviderStream.channel_id == channel_id,
            MChannelProviderStream.provider == provider,
            MChannelProviderStreamViewerWatchtime.channel_provider_stream_id
            == MChannelProviderStream.id,
            MChannelProviderStreamViewerWatchtime.provider_viewer_id
            == provider_viewer_id,
        )
        .order_by(
            MChannelProviderStream.started_at.desc(),
        )
    )

    pages = await page_cursor(
        query=stmt,
        page_query=page_query,
    )
    pages.records = [
        ViewerStream(
            channel_provider_stream=row[0],
            viewer_watchtime=row[1],
        )
        for row in pages.records
    ]
    return pages
