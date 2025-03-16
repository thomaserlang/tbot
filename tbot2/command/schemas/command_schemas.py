from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StringConstraints, conint, field_validator

from tbot2.common import BaseSchema


class Command(BaseSchema):
    id: UUID
    channel_id: UUID
    cmd: str
    response: str
    group_name: str
    global_cooldown: int
    chatter_cooldown: int
    mod_cooldown: int
    enabled_status: int
    enabled: bool
    public: bool
    aliases: list[str] | None
    patterns: list[str] | None
    access_level: int
    created_at: datetime
    updated_at: datetime | None = None


class CommandCreate(BaseModel):
    cmd: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
    ]
    response: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)
    ]
    group_name: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
    ] = ''
    global_cooldown: Annotated[int, conint(ge=0, le=2147483647)] = 0
    chatter_cooldown: Annotated[int, conint(ge=0, le=2147483647)] = 0
    mod_cooldown: Annotated[int, conint(ge=0, le=2147483647)] = 0
    enabled_status: Annotated[int, conint(ge=0, le=32767)] = 0
    enabled: bool = True
    public: bool = True
    aliases: list[str] | None = None
    patterns: list[str] | None = None
    access_level: Annotated[int, conint(ge=0, le=32767)] = 0


class CommandUpdate(BaseModel):
    cmd: (
        Annotated[
            str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
        ]
        | None
    ) = None
    response: (
        Annotated[
            str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)
        ]
        | None
    ) = None
    group_name: (
        Annotated[
            str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
        ]
        | None
    ) = None
    global_cooldown: Annotated[int, conint(ge=0, le=2147483647)] | None = None
    chatter_cooldown: Annotated[int, conint(ge=0, le=2147483647)] | None = None
    mod_cooldown: Annotated[int, conint(ge=0, le=2147483647)] | None = None
    enabled_status: Annotated[int, conint(ge=0, le=32767)] | None = None
    enabled: bool | None = None
    public: bool | None = None
    aliases: list[str] | None = None
    patterns: list[str] | None = None
    access_level: Annotated[int, conint(ge=0, le=32767)] | None = None

    @field_validator(
        'cmd',
        'response',
        'group_name',
        'global_cooldown',
        'chatter_cooldown',
        'mod_cooldown',
        'enabled_status',
        'enabled',
        'public',
        'access_level',
    )
    def check_none(cls, value: str | bool | None):
        if value is None:
            raise ValueError('Value cannot be None')
        return value
