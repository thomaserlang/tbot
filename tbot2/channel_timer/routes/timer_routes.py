from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, Security

from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

from ..actions.timer_actions import (
    create_timer,
    delete_timer,
    get_timer,
    update_timer,
)
from ..models.timer_model import MChannelTimer
from ..schemas.timer_schemas import Timer, TimerCreate, TimerUpdate
from ..types import TimerScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/timers',
    name='Get Channel Timers',
    responses={
        200: {
            'model': PageCursor[Timer],
        },
    },
)
async def get_timers_route(
    channel_id: UUID,
    page_query: Annotated[PageCursorQuery, Depends()],
    token_data: Annotated[TokenData, Security(authenticated, scopes=[TimerScope.READ])],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    stmt = (
        sa.select(MChannelTimer)
        .where(
            MChannelTimer.channel_id == channel_id,
        )
        .order_by(MChannelTimer.updated_at.desc())
    )

    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Timer,
    )
    return page


@router.get(
    '/channels/{channel_id}/timers/{timer_id}',
    name='Get Channel Timer',
    responses={
        200: {
            'model': Timer,
        },
    },
)
async def get_timer_route(
    channel_id: UUID,
    timer_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated, scopes=[TimerScope.READ])],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    timer = await get_timer(
        timer_id=timer_id,
    )
    if not timer or timer.channel_id != channel_id:
        raise HTTPException(status_code=404, detail='Timer not found')

    return timer


@router.post(
    '/channels/{channel_id}/timers',
    name='Create Channel Timer',
    responses={
        201: {
            'model': Timer,
        },
    },
    status_code=201,
)
async def create_timer_route(
    channel_id: UUID,
    data: TimerCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TimerScope.WRITE])
    ],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    timer = await create_timer(
        channel_id=channel_id,
        data=data,
    )
    return timer


@router.put(
    '/channels/{channel_id}/timers/{timer_id}',
    name='Update Channel Timer',
    responses={
        200: {
            'model': Timer,
        },
    },
)
async def update_timer_route(
    channel_id: UUID,
    timer_id: UUID,
    data: TimerUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TimerScope.WRITE])
    ],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    timer = await get_timer(
        timer_id=timer_id,
    )
    if not timer or timer.channel_id != channel_id:
        raise HTTPException(status_code=404, detail='Timer not found')

    timer = await update_timer(
        data=data,
        timer_id=timer.id,
    )
    return timer


@router.delete(
    '/channels/{channel_id}/timers/{timer_id}',
    name='Delete Channel Timer',
    status_code=204,
)
async def delete_timer_route(
    channel_id: UUID,
    timer_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[TimerScope.WRITE])
    ],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.MOD
    )
    timer = await get_timer(
        timer_id=timer_id,
    )
    if not timer or timer.channel_id != channel_id:
        raise HTTPException(status_code=404, detail='Timer not found')

    await delete_timer(
        timer_id=timer.id,
    )
