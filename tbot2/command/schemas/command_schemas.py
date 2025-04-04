from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field, StringConstraints, field_validator
from typing_extensions import Doc

from tbot2.common import BaseSchema, TAccessLevel, TProvider

from ..types import TCommandActiveMode


class Command(BaseSchema):
    id: UUID
    channel_id: UUID
    cmds: list[str]
    patterns: list[str] | None
    response: str
    group_name: str
    global_cooldown: int
    chatter_cooldown: int
    mod_cooldown: int
    active_mode: TCommandActiveMode
    enabled: bool
    public: bool
    access_level: Annotated[
        int, Doc(f'{" - ".join([f"{e.value}: {e.name}" for e in TAccessLevel])}')
    ]
    created_at: datetime
    updated_at: datetime | None = None
    provider: Literal['all'] | TProvider


Cmds = Annotated[
    list[
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True,
                to_lower=True,
                min_length=1,
                max_length=100,
                pattern=r'^[a-z0-9_-]+$',
            ),
        ]
    ],
    Field(max_length=15),
]

Patterns = Annotated[
    list[
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True,
                to_lower=True,
                min_length=1,
                max_length=100,
            ),
        ]
    ],
    Field(max_length=15),
]

Response = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)
]

GroupName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=0, max_length=100)
]


class CommandCreate(BaseModel):
    cmds: Cmds = []
    patterns: Patterns = []
    response: Response
    group_name: GroupName = ''
    global_cooldown: Annotated[int, Field(ge=0, le=2147483647)] = 0
    chatter_cooldown: Annotated[int, Field(ge=0, le=2147483647)] = 0
    mod_cooldown: Annotated[int, Field(ge=0, le=2147483647)] = 0
    active_mode: TCommandActiveMode = TCommandActiveMode.ALWAYS
    enabled: bool = True
    public: bool = True
    access_level: Annotated[
        TAccessLevel,
        Body(
            description=f'{" - ".join([f"{e.value}: {e.name}" for e in TAccessLevel])}'
        ),
    ] = TAccessLevel.PUBLIC
    provider: Literal['all'] | TProvider = 'all'


class CommandUpdate(BaseModel):
    cmds: Cmds | None = None
    patterns: Patterns | None = None
    response: Response | None = None
    group_name: GroupName | None = None
    global_cooldown: Annotated[int, Field(ge=0, le=2147483647)] | None = None
    chatter_cooldown: Annotated[int, Field(ge=0, le=2147483647)] | None = None
    mod_cooldown: Annotated[int, Field(ge=0, le=2147483647)] | None = None
    active_mode: TCommandActiveMode | None = None
    enabled: bool | None = None
    public: bool | None = None
    access_level: (
        Annotated[
            TAccessLevel,
            Body(
                description=f'{" - ".join([f"{e.value}: {e.name}" for e in TAccessLevel])}'
            ),
        ]
        | None
    ) = None
    provider: Literal['all'] | TProvider | None = None

    @field_validator(
        'cmds',
        'patterns',
        'response',
        'group_name',
        'global_cooldown',
        'chatter_cooldown',
        'mod_cooldown',
        'active_mode',
        'enabled',
        'public',
        'access_level',
        'provider',
    )
    def check_none(cls, value: str | bool | Cmds | Patterns | None):
        if value is None:
            raise ValueError('Value cannot be None')
        return value
