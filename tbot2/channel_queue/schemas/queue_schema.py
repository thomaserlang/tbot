from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, BaseSchema


class Queue(BaseSchema):
    id: UUID
    channel_id: UUID
    name: str
    created_at: datetime


class QueueCreate(BaseRequestSchema):
    name: Annotated[str, StringConstraints(min_length=1, max_length=255)]


class QueueUpdate(BaseRequestSchema):
    name: Annotated[str, StringConstraints(min_length=1, max_length=255)] | None = None

    @field_validator('name')
    @classmethod
    def check_not_none(cls, v: str | None) -> str:
        if v is None:
            raise ValueError('name cannot be None')
        return v
