from typing import Annotated, Literal

from pydantic import Field

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseSettings,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterNonLatinSettings(ChatFilterBaseSettings):
    min_length: Annotated[int, Field(ge=0)] = 5
    max_percent: Annotated[int, Field(ge=0, le=100)] = 80


class ChatFilterNonLatin(ChatFilterBase):
    type: Literal['non_latin']
    settings: ChatFilterNonLatinSettings


class ChatFilterNonLatinCreate(ChatFilterCreate):
    type: Literal['non_latin']
    name: str = 'Non-latin Filter'
    settings: ChatFilterNonLatinSettings = ChatFilterNonLatinSettings()


class ChatFilterNonLatinUpdate(ChatFilterUpdate):
    type: Literal['non_latin']
    settings: ChatFilterNonLatinSettings | None = None
