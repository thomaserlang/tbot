from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, BaseSchema, TProvider

from ..types import TimerActiveMode, TimerPickMode


class Timer(BaseSchema):
    id: UUID
    channel_id: UUID
    name: str
    messages: list[str]
    interval: int  # in minutes
    enabled: bool
    next_run_at: datetime
    provider: Literal['all'] | TProvider
    pick_mode: TimerPickMode
    active_mode: TimerActiveMode
    last_message_index: int | None
    created_at: datetime
    updated_at: datetime


Name = Annotated[str, StringConstraints(min_length=1, max_length=255)]
Messages = Annotated[
    list[
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True,
                min_length=1,
                max_length=500,
            ),
        ]
    ],
    Field(
        min_length=1,
        max_length=100,
    ),
]


class TimerCreate(BaseRequestSchema):
    name: Name
    messages: Messages
    interval: Annotated[int, Field(ge=1, description='Minutes')] = 30
    enabled: bool = True
    provider: Literal['all'] | TProvider = 'all'
    pick_mode: TimerPickMode = 'order'
    active_mode: TimerActiveMode = 'always'

    @field_validator('messages', mode='before')
    @classmethod
    def check_messages(cls, values: list[str] | None) -> list[str] | None:
        if values is None:
            return None
        return [message.strip() for message in values if message.strip()]


class TimerUpdate(BaseRequestSchema):
    name: Name | None = None
    messages: Messages | None = None
    interval: Annotated[int, Field(ge=1, description='Minutes')] | None = None
    enabled: bool | None = None
    provider: Literal['all'] | TProvider | None = None
    pick_mode: TimerPickMode | None = None
    active_mode: TimerActiveMode | None = None

    @field_validator(
        'name',
        'messages',
        'interval',
        'enabled',
        'provider',
        'pick_mode',
        'active_mode',
    )
    @classmethod
    def check_not_none(
        cls, value: str | int | bool | TProvider | TimerPickMode | TimerActiveMode
    ) -> str | int | bool | TProvider | TimerPickMode | TimerActiveMode:
        if value is None:
            raise ValueError('Cannot be None')
        return value

    @field_validator('messages', mode='before')
    @classmethod
    def check_messages(cls, values: list[str] | None) -> list[str] | None:
        if values is None:
            return None
        return [message.strip() for message in values if message.strip()]
