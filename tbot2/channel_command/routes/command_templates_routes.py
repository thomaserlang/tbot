from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Security

from tbot2.channel_command import CommandScope
from tbot2.common import ErrorMessage, TokenData
from tbot2.dependecies import authenticated
from tbot2.page_cursor import PageCursor, PageCursorQueryDep, page_cursor

from ..actions.command_template_actions import (
    create_command_template,
    delete_command_template,
    get_command_template,
    update_command_template,
)
from ..models.command_template_model import MCommandTemplate
from ..schemas.command_template_schemas import (
    CommandTemplate,
    CommandTemplateCreate,
    CommandTemplateUpdate,
)

router = APIRouter()


@router.get('/command-templates', name='Get Command Templates')
async def get_command_templates_route(
    page_query: PageCursorQueryDep,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.READ])
    ],
) -> PageCursor[CommandTemplate]:
    stmt = sa.select(MCommandTemplate).order_by(
        MCommandTemplate.title, MCommandTemplate.id
    )
    return await page_cursor(
        query=stmt,
        page_query=page_query,
        response_model=CommandTemplate,
        count_total=False,
    )


@router.get('/command-templates/{command_template_id}', name='Get Command Template')
async def get_command_template_route(
    command_template_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.READ])
    ],
) -> CommandTemplate:
    command_template = await get_command_template(
        command_template_id=command_template_id,
    )
    if not command_template:
        raise ErrorMessage(
            'Command template not found',
            type='command_template_not_found',
            code=404,
        )
    return command_template


@router.post('/command-templates', status_code=201, name='Create Command Template')
async def create_command_template_route(
    data: CommandTemplateCreate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.WRITE])
    ],
) -> CommandTemplate:
    await token_data.require_global_admin()
    return await create_command_template(data)


@router.put('/command-templates/{command_template_id}', name='Update Command Template')
async def update_command_template_route(
    command_template_id: UUID,
    data: CommandTemplateUpdate,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.WRITE])
    ],
) -> CommandTemplate:
    await token_data.require_global_admin()
    return await update_command_template(
        command_template_id=command_template_id,
        data=data,
    )


@router.delete(
    '/command-templates/{command_template_id}',
    name='Delete Command Template',
    status_code=204,
)
async def delete_command_template_route(
    command_template_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[CommandScope.WRITE])
    ],
) -> None:
    await token_data.require_global_admin()
    await delete_command_template(
        command_template_id=command_template_id,
    )
