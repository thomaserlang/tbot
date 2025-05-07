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
    add_viewer_to_queue,
    clear_queue,
    move_viewer_to_top,
    remove_viewer_from_queue,
)
from ..models.queue_model import MQueue
from ..models.queue_viewer_model import MQueueViewer
from ..schemas.queue_viewer_schema import QueueViewer, QueueViewerCreate
from ..types import QueueScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers', name='Get Queue Viewers'
)
async def get_queue_viewers_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated, scopes=[QueueScope.READ])],
    page_query: PageCursorQueryDep,
    provider: Provider | None = None,
    provider_viewer_id: str | None = None,
) -> PageCursor[QueueViewer]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    stmt = (
        sa.select(MQueueViewer)
        .where(
            MQueueViewer.channel_queue_id == channel_queue_id,
            MQueue.channel_id == channel_id,
            MQueue.id == MQueueViewer.channel_queue_id,
        )
        .order_by(
            MQueueViewer.position,
        )
    )

    if provider and provider_viewer_id:
        stmt = stmt.where(
            MQueueViewer.provider == provider,
            MQueueViewer.provider_viewer_id == provider_viewer_id,
        )

    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=QueueViewer,
    )
    return page


@router.post(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers',
    name='Add Viewer to Queue',
    status_code=201,
)
async def add_viewer_to_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    data: QueueViewerCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[QueueScope.WRITE])
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
            message='Queue not found',
            type='queue_not_found',
        )

    viewer = await add_viewer_to_queue(
        channel_queue_id=channel_queue_id,
        data=data,
    )
    return viewer


@router.delete(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers/{channel_queue_viewer_id}',
    name='Remove Viewer from Queue',
    status_code=204,
)
async def remove_viewer_from_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    channel_queue_viewer_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[QueueScope.WRITE])
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
            message='Queue not found',
            type='queue_not_found',
        )

    await remove_viewer_from_queue(channel_queue_viewer_id)


@router.delete(
    '/channels/{channel_id}/queues/{channel_queue_id}/viewers',
    name='Clear queue',
    status_code=204,
)
async def clear_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[QueueScope.WRITE])
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
            message='Queue not found',
            type='queue_not_found',
        )

    await clear_queue(channel_queue_id)


@router.put(
    '/channels/{channel_id}/queues/{channel_queue_id}/move-to-top',
    name='Move Viewer to Top',
    status_code=204,
)
async def move_viewer_to_top_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    channel_queue_viewer_id: Annotated[UUID, Body(embed=True)],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[QueueScope.WRITE])
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
            message='Queue not found',
            type='queue_not_found',
        )

    await move_viewer_to_top(channel_queue_viewer_id)
