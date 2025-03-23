from typing import Annotated, Literal

from pydantic import Field

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseSettings,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterCapsSettings(ChatFilterBaseSettings):
    min_length: Annotated[int, Field(ge=0)] = 20
    max_percent: Annotated[int, Field(ge=0, le=100)] = 60


class ChatFilterCaps(ChatFilterBase):
    type: Literal['caps']
    settings: ChatFilterCapsSettings


class ChatFilterCapsCreate(ChatFilterCreate):
    type: Literal['caps']
    name: str = 'Caps Filter'
    settings: ChatFilterCapsSettings = ChatFilterCapsSettings()


class ChatFilterCapsUpdate(ChatFilterUpdate):
    type: Literal['caps']
    settings: ChatFilterCapsSettings | None = None
