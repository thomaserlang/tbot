from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, Security

from tbot2.channel.models.channel_model import MChannel
from tbot2.channel.models.channel_user_access_levels_model import (
    MChannelUserAccessLevel,
)
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import Annotated, authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

from ..actions.channel_actions import get_channel
from ..schemas.channel_schemas import Channel

router = APIRouter()


@router.get(
    '/channels/{channel_id}',
    name='Get Channel',
    responses={
        200: {
            'model': Channel,
        },
    },
)
async def get_channel_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
):
    await token_data.channel_has_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    channel = await get_channel(
        id=channel_id,
    )
    if not channel:
        raise HTTPException(
            status_code=404,
            detail='Channel not found',
        )
    return channel


@router.get(
    '/channels',
    name='Get Channels',
    responses={
        200: {
            'model': PageCursor[Channel],
        },
    },
)
async def get_channels_route(
    token_data: Annotated[TokenData, Security(authenticated)],
    page_query: Annotated[PageCursorQuery, Depends()],
    name: str | None = None,
):
    stmt = (
        sa.select(MChannel)
        .where(
            MChannel.id == MChannelUserAccessLevel.channel_id,
            MChannelUserAccessLevel.user_id == token_data.user_id,
            MChannelUserAccessLevel.access_level >= TAccessLevel.MOD.value,
        )
        .order_by(MChannel.id)
    )

    if name:
        stmt = stmt.where(MChannel.display_name.ilike(f'%{name}%'))

    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Channel,
    )
    return page
