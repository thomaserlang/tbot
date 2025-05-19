from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, field_validator

from tbot2.common import BaseSchema

from .command_schemas import CommandCreate


class CommandTemplate(BaseSchema):
    id: UUID
    title: str
    commands: list[CommandCreate]
    created_at: datetime
    updated_at: datetime | None = None


class CommandTemplateCreate(BaseSchema):
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    commands: list[CommandCreate]


class CommandTemplateUpdate(BaseSchema):
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)] | None = None
    commands: list[CommandCreate] | None = None

    @field_validator('title', 'commands', mode='before')
    @classmethod
    def check_not_none(
        cls, v: str | list[CommandCreate] | None
    ) -> str | list[CommandCreate]:
        if v is None:
            raise ValueError('Field must not be None')
        return v
