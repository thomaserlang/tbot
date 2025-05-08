from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Body, Security

from tbot2.auth_backend import TokenData
from tbot2.common import ErrorMessage, Provider, TAccessLevel
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..actions.queue_actions import get_queue
from ..actions.queue_viewer_actions import (
    clear_viewer_queue,
    create_queue_viewer,
    delete_queue_viewer,
    move_viewer_to_top,
)
from ..models.channel_queue_model import MChannelQueue
from ..models.channel_queue_viewer_model import MChannelQueueViewer
from ..schemas.queue_viewer_schema import (
    QueueViewer,
    QueueViewerCreate,
)
from ..types import ChannelQueueScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers',
    name='Get Queue Viewers',
)
async def get_queue_viewers_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.READ])
    ],
    page_query: PageCursorQueryDep,
    provider: Provider | None = None,
    provider_viewer_id: str | None = None,
) -> PageCursor[QueueViewer]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    stmt = (
        sa.select(MChannelQueueViewer)
        .where(
            MChannelQueueViewer.channel_queue_id == channel_queue_id,
            MChannelQueue.channel_id == channel_id,
            MChannelQueue.id == MChannelQueueViewer.channel_queue_id,
        )
        .order_by(
            MChannelQueueViewer.position,
        )
    )

    if provider and provider_viewer_id:
        stmt = stmt.where(
            MChannelQueueViewer.provider == provider,
            MChannelQueueViewer.provider_viewer_id == provider_viewer_id,
        )

    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=QueueViewer,
    )


@router.post(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers',
    name='Add Viewer to Channel Queue',
    status_code=201,
)
async def add_viewer_to_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    data: QueueViewerCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.WRITE])
    ],
) -> QueueViewer:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    queue = await get_queue(channel_queue_id=channel_queue_id)
    if not queue or queue.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='queue not found',
            type='channel_queue_not_found',
        )

    return await create_queue_viewer(
        channel_queue_id=channel_queue_id,
        data=data,
    )


@router.delete(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers/{channel_queue_viewer_id}',
    name='Remove Viewer from Channel Queue',
    status_code=204,
)
async def remove_viewer_from_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    channel_queue_viewer_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.WRITE])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    queue = await get_queue(channel_queue_id=channel_queue_id)
    if not queue or queue.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='queue not found',
            type='channel_queue_not_found',
        )

    await delete_queue_viewer(channel_queue_viewer_id)


@router.delete(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers',
    name='Clear viewer queue',
    status_code=204,
)
async def clear_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.WRITE])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    queue = await get_queue(channel_queue_id=channel_queue_id)
    if not queue or queue.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='queue not found',
            type='channel_queue_not_found',
        )

    await clear_viewer_queue(channel_queue_id)


@router.put(
    '/channels/{channel_id}/queues/{channel_queue_id}/move-to-top',
    name='Move viewer to top of queue',
    status_code=204,
)
async def move_viewer_to_top_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    channel_queue_viewer_id: Annotated[UUID, Body(embed=True)],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.WRITE])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    queue = await get_queue(channel_queue_id=channel_queue_id)
    if not queue or queue.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='queue not found',
            type='channel_queue_not_found',
        )

    await move_viewer_to_top(channel_queue_viewer_id)
