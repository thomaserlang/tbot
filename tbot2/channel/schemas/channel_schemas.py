from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, field_validator

from tbot2.common import BaseRequestSchema, BaseSchema


class ChannelCreate(BaseRequestSchema):
    display_name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    bot_active: bool = True
    bot_muted: bool = False
    bot_chatlog_enabled: bool = True


class ChannelUpdate(BaseRequestSchema):
    display_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=200)] | None
    ) = None
    bot_active: bool | None = None
    bot_muted: bool | None = None
    bot_chatlog_enabled: bool | None = None

    @field_validator('bot_active', 'bot_muted', 'bot_chatlog_enabled', 'display_name')
    def check_not_none(cls, value: str | bool | None) -> str | bool:
        if value is None:
            raise ValueError('Must not be None')
        return value


class Channel(BaseSchema):
    id: UUID
    display_name: str
    created_at: datetime
