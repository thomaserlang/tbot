from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends, Security

from tbot2.channel_user_access import (
    MChannelUserAccessLevel,
    set_channel_user_access_level,
)
from tbot2.common import ErrorMessage, TAccessLevel, TokenData
from tbot2.contexts import get_session
from tbot2.dependecies import Annotated, authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

from ..actions.channel_actions import (
    create_channel,
    delete_channel,
    get_channel,
    update_channel,
)
from ..models.channel_model import MChannel
from ..schemas.channel_schemas import Channel, ChannelCreate, ChannelUpdate
from ..types import ChannelScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}',
    name='Get Channel',
)
async def get_channel_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.READ])
    ],
) -> Channel:
    channel = await get_channel(
        channel_id=channel_id,
    )
    if not channel:
        raise ErrorMessage(
            code=404, type='channel_not_found', message='Channel not found'
        )
    
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    return channel


@router.post(
    '/channels',
    name='Create Channel',
    status_code=201,
)
async def create_channel_route(
    data: ChannelCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.WRITE])
    ],
) -> Channel:
    async with get_session() as session:
        channel = await create_channel(data=data, session=session)
        await set_channel_user_access_level(
            channel_id=channel.id,
            user_id=token_data.user_id,
            access_level=TAccessLevel.OWNER,
            session=session,
        )
    return channel


@router.put(
    '/channels/{channel_id}',
    name='Update Channel',
)
async def update_channel_route(
    channel_id: UUID,
    data: ChannelUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.WRITE])
    ],
) -> Channel:
    channel = await get_channel(
        channel_id=channel_id,
    )
    if not channel:
        raise ErrorMessage(
            code=404, type='channel_not_found', message='Channel not found'
        )

    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    channel = await update_channel(
        channel_id=channel_id,
        data=data,
    )
    return channel


@router.delete(
    '/channels/{channel_id}',
    name='Delete Channel',
    status_code=204,
)
async def delete_channel_route(
    channel_id: UUID,
    channel_name: str,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.DELETE])
    ],
) -> None:
    channel = await get_channel(
        channel_id=channel_id,
    )
    if not channel:
        raise ErrorMessage(
            code=404, type='channel_not_found', message='Channel not found'
        )

    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.OWNER,
    )

    if channel.display_name.lower() != channel_name.lower():
        raise ErrorMessage(
            code=400,
            type='channel_name_mismatch',
            message='Channel name does not match',
        )
    await delete_channel(
        channel_id=channel_id,
    )


@router.get(
    '/channels',
    name='Get Channels',
)
async def get_channels_route(
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.READ])
    ],
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
