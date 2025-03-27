from re import findall
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common.schemas.chat_message_schema import ChatMessage

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseSettings,
    ChatFilterBaseUpdate,
    FilterMatchResult,
)


class ChatFilterSymbolSettings(ChatFilterBaseSettings):
    max_symbols: Annotated[int, Field(ge=0)] = 20


class ChatFilterSymbolCreate(ChatFilterBaseCreate):
    type: Literal['symbol']
    name: str = 'Symbol Filter'
    settings: ChatFilterSymbolSettings = ChatFilterSymbolSettings()


class ChatFilterSymbolUpdate(ChatFilterBaseUpdate):
    type: Literal['symbol']
    settings: ChatFilterSymbolSettings | None = None


class ChatFilterSymbol(ChatFilterBase):
    type: Literal['symbol']
    settings: ChatFilterSymbolSettings

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        symbols = findall(r'[^ \w]', message.message_without_fragments())
        return FilterMatchResult(
            filter=self, matched=len(symbols) > self.settings.max_symbols
        )
