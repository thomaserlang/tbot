from re import findall
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import ChatMessage

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseSettings,
    ChatFilterBaseUpdate,
    FilterMatchResult,
)


class ChatFilterCapsSettings(ChatFilterBaseSettings):
    min_length: Annotated[int, Field(ge=0)] = 20
    max_percent: Annotated[int, Field(ge=0, le=100)] = 60


class ChatFilterCapsCreate(ChatFilterBaseCreate):
    type: Literal['caps']
    name: str = 'Caps Filter'
    settings: ChatFilterCapsSettings = ChatFilterCapsSettings()


class ChatFilterCapsUpdate(ChatFilterBaseUpdate):
    type: Literal['caps']
    settings: ChatFilterCapsSettings | None = None


class ChatFilterCaps(ChatFilterBase):
    type: Literal['caps']
    settings: ChatFilterCapsSettings

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        caps = findall(r'[A-Z]', message.message_without_fragments())
        return FilterMatchResult(
            filter=self,
            matched=(len(caps) / len(message.message_without_fragments())) * 100
            > self.settings.max_percent,
        )
