from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints, field_validator

from tbot2.common import BaseSchema


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=100)]
    email: EmailStr
    display_name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    default_channel_id: UUID | None = None


class UserUpdate(BaseModel):
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
    def check_not_none(cls, value: str | bool | None):
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


class UserPublic(BaseSchema):
    id: UUID
    username: str
    display_name: str
