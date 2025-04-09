from typing import Annotated, Literal
from uuid import UUID

from pydantic import ConfigDict, StringConstraints, field_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Doc

from tbot2.common import (
    BaseRequestSchema,
    BaseSchema,
    ChatMessage,
    TAccessLevel,
    TProvider,
)


class ChatFilterBaseSettings(BaseSchema):
    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid',
    )


@dataclass(slots=True)
class FilterMatchResult:
    filter: 'ChatFilterBase'
    matched: bool = False
    action: Literal['warning', 'timeout'] | None = None
    sub_id: Annotated[UUID | None, Doc('Used e.g. for which banned term matched')] = (
        None
    )


class ChatFilterBase(BaseSchema):
    id: UUID
    channel_id: UUID
    name: str
    provider: Literal['all'] | TProvider
    enabled: bool
    exclude_access_level: TAccessLevel
    warning_enabled: bool
    warning_message: str
    warning_expire_duration: int
    timeout_message: str
    timeout_duration: int

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        return FilterMatchResult(filter=self, matched=False)


ChatFilterName = Annotated[str, StringConstraints(min_length=1, max_length=500)]
ChatFilterWarningMessage = Annotated[
    str, StringConstraints(min_length=0, max_length=500)
]
ChatFilterTimeoutMessage = Annotated[
    str, StringConstraints(min_length=0, max_length=500)
]


class ChatFilterBaseCreate(BaseRequestSchema):
    name: ChatFilterName
    enabled: bool = True
    provider: Literal['all'] | TProvider = 'all'
    exclude_access_level: TAccessLevel = TAccessLevel.MOD
    warning_enabled: bool = False
    warning_message: ChatFilterWarningMessage = ''
    warning_expire_duration: int = 3600
    timeout_message: ChatFilterTimeoutMessage = ''
    timeout_duration: int = 60


class ChatFilterBaseUpdate(BaseRequestSchema):
    name: ChatFilterName | None = None
    enabled: bool | None = None
    provider: Literal['all'] | TProvider = 'all'
    exclude_access_level: TAccessLevel | None = None
    warning_enabled: bool | None = None
    warning_message: ChatFilterWarningMessage | None = None
    warning_expire_duration: int | None = None
    timeout_message: ChatFilterTimeoutMessage | None = None
    timeout_duration: int | None = None

    @field_validator(
        'name',
        'enabled',
        'exclude_access_level',
        'warning_enabled',
        'warning_message',
        'warning_expire_duration',
        'timeout_message',
        'timeout_duration',
    )
    def check_not_none(cls, v: str | bool | int | None) -> str | bool | int:
        if v is None:
            raise ValueError('Field cannot be None')
        return v
