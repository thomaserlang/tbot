from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.common import datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.command_template_model import MCommandTemplate
from ..schemas.command_template_schemas import (
    CommandTemplate,
    CommandTemplateCreate,
    CommandTemplateUpdate,
)


async def get_command_template(
    command_template_id: UUID,
    session: AsyncSession | None = None,
) -> CommandTemplate | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MCommandTemplate).where(
                MCommandTemplate.id == command_template_id
            )
        )
        if not result:
            return None
        return CommandTemplate.model_validate(result)


async def create_command_template(
    data: CommandTemplateCreate,
    session: AsyncSession | None = None,
) -> CommandTemplate:
    async with get_session(session) as session:
        data_ = data.model_dump()
        id = uuid7()
        await session.execute(
            sa.insert(MCommandTemplate).values(
                id=id,
                created_at=datetime_now(),
                updated_at=datetime_now(),
                **data_,
            )
        )
        command_template = await get_command_template(
            command_template_id=id,
            session=session,
        )
        if not command_template:
            raise Exception('Command template was not created')
        return command_template


async def update_command_template(
    command_template_id: UUID,
    data: CommandTemplateUpdate,
    session: AsyncSession | None = None,
) -> CommandTemplate:
    async with get_session(session) as session:
        data_ = data.model_dump(exclude_unset=True)
        if data.commands:
            data_['commands'] = [command.model_dump() for command in data.commands]
        await session.execute(
            sa.update(MCommandTemplate)
            .where(MCommandTemplate.id == command_template_id)
            .values(
                updated_at=datetime_now(),
                **data_,
            )
        )
        command_template = await get_command_template(
            command_template_id=command_template_id,
            session=session,
        )
        if not command_template:
            raise Exception('Command template was not updated')
        return command_template


async def delete_command_template(
    command_template_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        r = await session.execute(
            sa.delete(MCommandTemplate).where(
                MCommandTemplate.id == command_template_id
            )
        )
        return r.rowcount > 0
