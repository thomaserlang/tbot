from typing import Annotated, Literal

from pydantic import Field

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseSettings,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterSymbolSettings(ChatFilterBaseSettings):
    max_symbols: Annotated[int, Field(ge=0)] = 20


class ChatFilterSymbol(ChatFilterBase):
    type: Literal['symbol']
    settings: ChatFilterSymbolSettings


class ChatFilterSymbolCreate(ChatFilterCreate):
    type: Literal['symbol']
    name: str = 'Symbol Filter'
    settings: ChatFilterSymbolSettings = ChatFilterSymbolSettings()


class ChatFilterSymbolUpdate(ChatFilterUpdate):
    type: Literal['symbol']
    settings: ChatFilterSymbolSettings | None = None
