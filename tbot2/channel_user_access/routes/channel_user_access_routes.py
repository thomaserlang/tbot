from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Security

from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..actions.channel_user_access_level_actions import (
    delete_channel_user_access_level,
    get_channel_user_access_level_by_id,
)
from ..models.channel_user_access_levels_model import (
    MChannelUserAccessLevelWithUser,
)
from ..schemas.channel_user_access_level_schemas import ChannelUserAccessLevelWithUser
from ..types import ChannelUserAccessScope

router = APIRouter()


@router.get('/channels/{channel_id}/users-access', name='Get Channel Users Access')
async def get_channel_users_access_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelUserAccessScope.READ])
    ],
    page_query: PageCursorQueryDep,
) -> PageCursor[ChannelUserAccessLevelWithUser]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    stmt = (
        sa.select(MChannelUserAccessLevelWithUser)
        .where(
            MChannelUserAccessLevelWithUser.channel_id == channel_id,
        )
        .order_by(
            MChannelUserAccessLevelWithUser.id.desc(),
        )
    )
    page = await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=ChannelUserAccessLevelWithUser,
    )
    return page


@router.delete(
    '/channels/{channel_id}/users-access/{channel_user_access_id}',
    name='Delete Channel User Access',
    status_code=204,
)
async def delete_channel_user_access_route(
    channel_id: UUID,
    channel_user_access_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelUserAccessScope.WRITE])
    ],
) -> None:
    user_access_level = await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    user_access = await get_channel_user_access_level_by_id(
        channel_user_access_id=channel_user_access_id,
    )
    if not user_access or user_access.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='User access not found',
        )

    if (
        user_access_level <= user_access.access_level
        and user_access.access_level != TAccessLevel.OWNER
    ):
        raise HTTPException(
            status_code=403,
            detail='Insufficient access level',
        )

    await delete_channel_user_access_level(
        channel_user_access_id=user_access.id,
    )
