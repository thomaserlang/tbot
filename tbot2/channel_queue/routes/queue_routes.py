from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Security

from tbot2.auth_backend import TokenData
from tbot2.common import ErrorMessage, TAccessLevel
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..actions.queue_actions import (
    create_queue,
    delete_queue,
    get_queue,
    update_queue,
)
from ..models.channel_queue_model import MChannelQueue
from ..schemas.queue_schema import (
    Queue,
    QueueCreate,
    QueueUpdate,
)
from ..types import ChannelQueueScope

router = APIRouter()


@router.get('/channels/{channel_id}/queues', name='Get Queues')
async def get_queues_route(
    channel_id: UUID,
    page_query: PageCursorQueryDep,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.READ])
    ],
) -> PageCursor[Queue]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    stmt = (
        sa.select(MChannelQueue)
        .where(
            MChannelQueue.channel_id == channel_id,
        )
        .order_by(
            MChannelQueue.id.desc(),
        )
    )

    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Queue,
    )


@router.get('/channels/{channel_id}/queues/{channel_queue_id}', name='Get Queue')
async def get_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.READ])
    ],
) -> Queue:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    queue = await get_queue(channel_queue_id=channel_queue_id)
    if not queue or queue.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='Channel queue not found',
            type='channel_queue_not_found',
        )
    return queue


@router.post('/channels/{channel_id}/queues', name='Create Queue', status_code=201)
async def create_queue_route(
    channel_id: UUID,
    data: QueueCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.WRITE])
    ],
) -> Queue:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    return await create_queue(
        channel_id=channel_id,
        data=data,
    )


@router.put(
    '/channels/{channel_id}/queues/{channel_queue_id}',
    name='Update Queue',
)
async def update_queue_route(
    channel_id: UUID,
    channel_queue_id: UUID,
    data: QueueUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelQueueScope.WRITE])
    ],
) -> Queue:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    queue = await get_queue(channel_queue_id=channel_queue_id)
    if not queue or queue.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='Channel queue not found',
            type='channel_queue_not_found',
        )

    return await update_queue(
        channel_queue_id=channel_queue_id,
        data=data,
    )


@router.delete(
    '/channels/{channel_id}/queues/{channel_queue_id}',
    name='Delete Queue',
    status_code=204,
)
async def delete_queue_route(
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
            message='Channel queue not found',
            type='channel_queue_not_found',
        )

    await delete_queue(
        channel_queue_id=channel_queue_id,
    )
