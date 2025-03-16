from datetime import datetime, timezone
from uuid import UUID

import sqlalchemy as sa
from uuid6 import uuid7

from tbot2.contexts import AsyncSession, get_session

from ..models.command_model import MCommand
from ..schemas.command_schemas import Command, CommandCreate, CommandUpdate


async def get_command(
    *,
    command_id: UUID,
    session: AsyncSession | None = None,
) -> Command | None:
    async with get_session(session) as session:
        result = await session.scalar(
            sa.select(MCommand).where(MCommand.id == command_id)
        )
        if result:
            return Command.model_validate(result)


async def create_command(
    *,
    channel_id: UUID,
    data: CommandCreate,
    session: AsyncSession | None = None,
) -> Command:
    async with get_session(session) as session:
        command_id = uuid7()
        await session.execute(
            sa.insert(MCommand).values(
                id=command_id,
                channel_id=channel_id,
                created_at=datetime.now(tz=timezone.utc),
                updated_at=datetime.now(tz=timezone.utc),
                **data.model_dump(),
            )
        )

        cmd = await get_command(command_id=command_id, session=session)
        if not cmd:
            raise Exception('Failed to create command')
        return cmd


async def update_command(
    *,
    command_id: UUID,
    data: CommandUpdate,
    session: AsyncSession | None = None,
) -> Command:
    async with get_session(session) as session:
        await session.execute(
            sa.update(MCommand)
            .where(MCommand.id == command_id)
            .values(
                updated_at=datetime.now(tz=timezone.utc),
                **data.model_dump(exclude_unset=True),
            )
        )

        cmd = await get_command(command_id=command_id, session=session)
        if not cmd:
            raise Exception('Failed to update command')
        return cmd


async def delete_command(
    *,
    command_id: UUID,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        result = await session.execute(
            sa.delete(MCommand).where(MCommand.id == command_id)
        )
        return result.rowcount > 0
