from typing import Annotated, Literal

from pydantic import Field

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseSettings,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterParagraphSettings(ChatFilterBaseSettings):
    max_length: Annotated[int, Field(ge=0)] = 350


class ChatFilterParagraph(ChatFilterBase):
    type: Literal['paragraph']
    settings: ChatFilterParagraphSettings


class ChatFilterParagraphCreate(ChatFilterCreate):
    type: Literal['paragraph']
    name: str = 'Paragraph Filter'
    settings: ChatFilterParagraphSettings = ChatFilterParagraphSettings()


class ChatFilterParagraphUpdate(ChatFilterUpdate):
    type: Literal['paragraph']
    settings: ChatFilterParagraphSettings | None = None
