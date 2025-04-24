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

from ..actions.channel_actions import delete_channel, get_channel
from ..schemas.channel_schemas import Channel

router = APIRouter()


@router.get(
    '/channels/{channel_id}',
    name='Get Channel',
)
async def get_channel_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> Channel:
    await token_data.channel_require_access(
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


@router.delete(
    '/channels/{channel_id}',
    name='Delete Channel',
)
async def delete_channel_route(
    channel_id: UUID,
    channel_name: str,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.OWNER,
    )
    channel = await get_channel(
        id=channel_id,
    )
    if not channel:
        raise HTTPException(
            status_code=404,
            detail='Channel not found',
        )
    if channel.display_name.lower() != channel_name:
        raise HTTPException(
            status_code=400,
            detail='Channel name does not match',
        )
    await delete_channel(
        channel_id=channel_id,
    )


@router.get(
    '/channels',
    name='Get Channels',
)
async def get_channels_route(
    token_data: Annotated[TokenData, Security(authenticated)],
    page_query: Annotated[PageCursorQuery, Depends()],
    name: str | None = None,
) -> PageCursor[Channel]:
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
