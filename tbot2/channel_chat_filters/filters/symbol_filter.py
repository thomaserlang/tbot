from re import findall
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common.schemas.chat_message_schema import ChatMessage

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


class ChatFilterSymbolSettings(ChatFilterBaseSettings):
    max_symbols: Annotated[int, Field(ge=0)] = 20


class ChatFilterSymbolCreate(ChatFilterBaseCreate):
    type: Literal['symbol']
    name: ChatFilterName = 'Symbol Filter'
    warning_message: ChatFilterWarningMessage = (
        'Your message contained too many symbols'
    )
    timeout_message: ChatFilterTimeoutMessage = (
        'Your message contained too many symbols'
    )
    settings: ChatFilterSymbolSettings = ChatFilterSymbolSettings()


class ChatFilterSymbolUpdate(ChatFilterBaseUpdate):
    type: Literal['symbol']
    settings: ChatFilterSymbolSettings | None = None


class ChatFilterSymbol(ChatFilterBase):
    type: Literal['symbol']
    settings: ChatFilterSymbolSettings

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        symbols = findall(r'[^ \w]', message.message_without_parts())
        return FilterMatchResult(
            filter=self, matched=len(symbols) > self.settings.max_symbols
        )
