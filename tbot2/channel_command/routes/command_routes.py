from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, Security

from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQuery, page_cursor

from ..actions.command_actions import (
    create_command,
    delete_command,
    get_command,
    update_command,
)
from ..models.command_model import MCommand
from ..schemas.command_schemas import Command, CommandCreate, CommandUpdate
from ..types import CommandScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/commands',
    name='Get Commands',
)
async def get_commands_route(
    channel_id: UUID,
    page_query: Annotated[PageCursorQuery, Depends()],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.READ])
    ],
) -> PageCursor[Command]:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    stmt = (
        sa.select(MCommand)
        .where(
            MCommand.channel_id == channel_id,
        )
        .order_by(MCommand.id.desc())
    )
    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=Command,
    )


@router.get(
    '/channels/{channel_id}/commands/{command_id}',
    name='Get Command',
)
async def get_command_route(
    channel_id: UUID,
    command_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.READ])
    ],
) -> Command:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    cmd = await get_command(command_id=command_id)
    if not cmd or cmd.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Command not found',
        )
    return cmd


@router.post(
    '/channels/{channel_id}/commands',
    name='Create Command',
    status_code=201,
)
async def create_command_route(
    channel_id: UUID,
    data: CommandCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.WRITE])
    ],
) -> Command:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    return await create_command(
        channel_id=channel_id,
        data=data,
    )


@router.put(
    '/channels/{channel_id}/commands/{command_id}',
    name='Update Command',
)
async def update_command_route(
    channel_id: UUID,
    command_id: UUID,
    data: CommandUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.WRITE])
    ],
) -> Command:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    cmd = await get_command(command_id=command_id)
    if not cmd or cmd.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Command not found',
        )
    return await update_command(
        command_id=command_id,
        data=data,
    )


@router.delete(
    '/channels/{channel_id}/commands/{command_id}',
    name='Delete Command',
    status_code=204,
)
async def delete_command_route(
    channel_id: UUID,
    command_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.WRITE])
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    cmd = await get_command(command_id=command_id)
    if not cmd or cmd.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Command not found',
        )
    await delete_command(
        command_id=command_id,
    )
