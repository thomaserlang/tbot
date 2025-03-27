from typing import Annotated
from uuid import UUID

from pydantic import ConfigDict, StringConstraints, field_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Doc

from tbot2.common import BaseRequestSchema, BaseSchema, ChatMessage, TAccessLevel


class ChatFilterBaseSettings(BaseSchema):
    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid',
    )


@dataclass(slots=True)
class FilterMatchResult:
    filter: 'ChatFilterBase'
    matched: bool = False
    sub_id: Annotated[UUID | None, Doc('Used e.g. for which banned term matched')] = (
        None
    )


class ChatFilterBase(BaseSchema):
    id: UUID
    channel_id: UUID
    name: str
    enabled: bool
    exclude_access_level: TAccessLevel
    warning_enabled: bool
    warning_message: str
    warning_expire_duration: int
    timeout_message: str
    timeout_duration: int

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        return FilterMatchResult(filter=self, matched=False)


class ChatFilterBaseCreate(BaseRequestSchema):
    name: Annotated[str, StringConstraints(min_length=1, max_length=500)]
    enabled: bool = True
    exclude_access_level: TAccessLevel = TAccessLevel.MOD
    warning_enabled: bool = False
    warning_message: Annotated[
        str, StringConstraints(min_length=1, max_length=1000)
    ] = ''
    warning_expire_duration: int = 3600
    timeout_message: Annotated[
        str, StringConstraints(min_length=1, max_length=1000)
    ] = 'Not permitted.'
    timeout_duration: int = 60


class ChatFilterBaseUpdate(BaseRequestSchema):
    name: Annotated[str, StringConstraints(min_length=1, max_length=500)] | None = None
    enabled: bool | None = None
    exclude_access_level: TAccessLevel | None = None
    warning_enabled: bool | None = None
    warning_message: (
        Annotated[str, StringConstraints(min_length=1, max_length=1000)] | None
    ) = None
    warning_expire_duration: int | None = None
    timeout_message: (
        Annotated[str, StringConstraints(min_length=1, max_length=1000)] | None
    ) = None
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
