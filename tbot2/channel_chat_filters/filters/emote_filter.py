from typing import Annotated, Literal

from pydantic import Field

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseSettings,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterEmoteSettings(ChatFilterBaseSettings):
    max_emotes: Annotated[int, Field(ge=0)] = 20


class ChatFilterEmote(ChatFilterBase):
    type: Literal['emote']
    settings: ChatFilterEmoteSettings


class ChatFilterEmoteCreate(ChatFilterCreate):
    type: Literal['emote']
    name: str = 'Emote Filter'
    settings: ChatFilterEmoteSettings = ChatFilterEmoteSettings()


class ChatFilterEmoteUpdate(ChatFilterUpdate):
    type: Literal['emote']
    settings: ChatFilterEmoteSettings | None = None
