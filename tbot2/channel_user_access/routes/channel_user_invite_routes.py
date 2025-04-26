from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Security

from tbot2.channel import Channel, get_channel
from tbot2.common import TAccessLevel, TokenData, datetime_now
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..actions.channel_user_access_level_actions import (
    get_channel_user_access_level,
)
from ..actions.channel_user_invite_actions import (
    MChannelUserInvite,
    channel_user_invite_accept,
    create_channel_user_invite,
    delete_channel_user_invite,
    get_channel_user_invite,
    update_channel_user_invite,
)
from ..schemas.channel_user_invite_schema import (
    ChannelUserInvite,
    ChannelUserInviteCreate,
    ChannelUserInviteUpdate,
)
from ..types import ChannelUserAccessScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/user-invites',
    name='Channel User Invites',
)
async def get_channel_user_invites_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelUserAccessScope.WRITE])
    ],
    page_query: PageCursorQueryDep,
) -> PageCursor[ChannelUserInvite]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    stmt = (
        sa.select(MChannelUserInvite)
        .where(
            MChannelUserInvite.channel_id == channel_id,
        )
        .order_by(
            MChannelUserInvite.id.desc(),
        )
    )
    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=ChannelUserInvite,
    )
    return page


@router.post('/channels/{channel_id}/user-invites', name='Channel User Invite')
async def create_channel_user_invite_route(
    channel_id: UUID,
    data: ChannelUserInviteCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelUserAccessScope.WRITE])
    ],
) -> ChannelUserInvite:
    user_access_level = await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    if (
        user_access_level <= data.access_level
        and user_access_level != TAccessLevel.OWNER
    ):
        raise HTTPException(
            status_code=403,
            detail='You cannot create an invite with an equal or higher access level',
        )

    invite = await create_channel_user_invite(
        channel_id=channel_id,
        data=data,
    )
    return invite


@router.put(
    '/channels/{channel_id}/user-invites/{channel_user_invite_id}',
    name='Channel User Invite Update',
)
async def update_channel_user_invite_route(
    channel_id: UUID,
    channel_user_invite_id: UUID,
    data: ChannelUserInviteUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelUserAccessScope.WRITE])
    ],
) -> ChannelUserInvite:
    user_access_level = await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    invite = await get_channel_user_invite(
        channel_user_invite_id=channel_user_invite_id,
    )
    if not invite or invite.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Invite not found',
        )

    if (
        user_access_level <= data.access_level
        and user_access_level != TAccessLevel.OWNER
    ):
        raise HTTPException(
            status_code=403,
            detail='You cannot update an invite with an equal or higher access level',
        )

    updated_invite = await update_channel_user_invite(
        channel_user_invite_id=channel_user_invite_id,
        data=data,
    )
    return updated_invite


@router.delete(
    '/channels/{channel_id}/user-invites/{channel_user_invite_id}',
    name='Channel User Invite Delete',
    status_code=204,
)
async def delete_channel_user_invite_route(
    channel_id: UUID,
    channel_user_invite_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelUserAccessScope.WRITE])
    ],
) -> None:
    user_access_level = await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    invite = await get_channel_user_invite(
        channel_user_invite_id=channel_user_invite_id,
    )
    if not invite or invite.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Invite not found',
        )

    if (
        user_access_level <= invite.access_level
        and user_access_level != TAccessLevel.OWNER
    ):
        raise HTTPException(
            status_code=403,
            detail='You cannot delete an invite with an equal or higher access level',
        )

    await delete_channel_user_invite(
        channel_user_invite_id=channel_user_invite_id,
    )


@router.post(
    '/channel-user-invites/{channel_user_invite_id}/accept',
    name='Channel User Invite Accept',
)
async def accept_channel_user_invite_route(
    channel_user_invite_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> Channel:
    invite = await get_channel_user_invite(
        channel_user_invite_id=channel_user_invite_id,
    )
    if not invite:
        raise HTTPException(
            status_code=404,
            detail='Invite not found',
        )

    user_level = await get_channel_user_access_level(
        user_id=token_data.user_id,
        channel_id=invite.channel_id,
    )
    if user_level:
        raise HTTPException(
            status_code=400,
            detail='You already have access to this channel',
        )

    if invite.expires_at < datetime_now():
        raise HTTPException(
            status_code=400,
            detail='Invite expired',
        )

    await channel_user_invite_accept(
        channel_user_invite_id=channel_user_invite_id,
        user_id=token_data.user_id,
    )

    channel = await get_channel(
        channel_id=invite.channel_id,
    )
    if not channel:
        raise HTTPException(
            status_code=404,
            detail='Channel not found',
        )
    return channel
