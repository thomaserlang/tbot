from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator


class ChannelCreate(BaseModel):
    display_name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    twitch_id: (
        Annotated[str, StringConstraints(min_length=36, max_length=36)] | None
    ) = None
    bot_active: bool = True
    bot_muted: bool = False
    bot_chatlog_enabled: bool = True


class ChannelUpdate(BaseModel):
    display_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=200)] | None
    ) = None
    bot_active: bool | None = None
    bot_muted: bool | None = None
    bot_chatlog_enabled: bool | None = None

    @field_validator('bot_active', 'bot_muted', 'bot_chatlog_enabled', 'display_name')
    @classmethod
    def check_not_none(cls, value: str | bool | None):
        if value is None:
            raise ValueError('Must not be None')
        return value


class Channel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    display_name: str
    twitch_id: str | None
    created_at: datetime
    bot_active: bool
    bot_muted: bool
    bot_chatlog_enabled: bool
