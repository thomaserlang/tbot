from re import IGNORECASE, findall, sub
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import ChatMessageCreate

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseSettings,
    ChatFilterBaseUpdate,
    ChatFilterName,
    ChatFilterTimeoutMessage,
    ChatFilterWarningMessage,
    FilterMatchResult,
)


class ChatFilterNonLatinSettings(ChatFilterBaseSettings):
    min_length: Annotated[int, Field(ge=0)] = 5
    max_percent: Annotated[int, Field(ge=0, le=100)] = 80


class ChatFilterNonLatinCreate(ChatFilterBaseCreate):
    type: Literal['non_latin']
    name: ChatFilterName = 'Non-latin Filter'
    warning_message: ChatFilterWarningMessage = 'Please use latin letters'
    timeout_message: ChatFilterTimeoutMessage = 'Please use latin letters'

    settings: ChatFilterNonLatinSettings = ChatFilterNonLatinSettings()


class ChatFilterNonLatinUpdate(ChatFilterBaseUpdate):
    type: Literal['non_latin']
    settings: ChatFilterNonLatinSettings | None = None


class ChatFilterNonLatin(ChatFilterBase):
    type: Literal['non_latin']
    settings: ChatFilterNonLatinSettings

    async def check_message(self, message: ChatMessageCreate) -> FilterMatchResult:
        chars = sub(r'[\W]', '', message.message_without_parts())
        if not chars:
            return FilterMatchResult(filter=self, matched=False)

        non_latin = findall(r'[^a-z0-9_]', chars, IGNORECASE)
        return FilterMatchResult(
            filter=self,
            matched=((len(non_latin) / len(chars)) * 100 > self.settings.max_percent)
            and (len(non_latin)) >= self.settings.min_length,
        )
