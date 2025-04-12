from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, BaseSchema


class UserCreate(BaseRequestSchema):
    username: Annotated[str, StringConstraints(min_length=3, max_length=100)]
    email: EmailStr
    display_name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    default_channel_id: UUID | None = None


class UserUpdate(BaseRequestSchema):
    username: Annotated[str, StringConstraints(min_length=3, max_length=100)] | None = (
        None
    )
    email: EmailStr | None = None
    display_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    is_active: bool | None = None
    default_channel_id: UUID | None = None

    @field_validator('username', 'email', 'display_name', 'is_active')
    def check_not_none(cls, value: str | bool | None) -> str | bool:
        if value is None:
            raise ValueError('Must not be None')
        return value


class User(BaseSchema):
    id: UUID
    username: str
    email: str
    display_name: str
    created_at: datetime
    updated_at: datetime | None = None
    is_active: bool
    default_channel_id: UUID | None = None


class UserPublic(BaseSchema):
    id: UUID
    username: str
    display_name: str
    default_channel_id: UUID | None = None
