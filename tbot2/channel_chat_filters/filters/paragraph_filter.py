from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import ChatMessage

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseSettings,
    ChatFilterBaseUpdate,
)


class ChatFilterParagraphSettings(ChatFilterBaseSettings):
    max_length: Annotated[int, Field(ge=0)] = 350


class ChatFilterParagraphCreate(ChatFilterBaseCreate):
    type: Literal['paragraph']
    name: str = 'Paragraph Filter'
    settings: ChatFilterParagraphSettings = ChatFilterParagraphSettings()


class ChatFilterParagraphUpdate(ChatFilterBaseUpdate):
    type: Literal['paragraph']
    settings: ChatFilterParagraphSettings | None = None


class ChatFilterParagraph(ChatFilterBase):
    type: Literal['paragraph']
    settings: ChatFilterParagraphSettings

    async def check_message(self, message: ChatMessage) -> bool:
        return len(message.message_without_fragments()) > self.settings.max_length
