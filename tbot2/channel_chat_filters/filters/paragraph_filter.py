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


class ChatFilterParagraphSettings(ChatFilterBaseSettings):
    max_length: Annotated[int, Field(ge=0)] = 350


class ChatFilterParagraphCreate(ChatFilterBaseCreate):
    type: Literal['paragraph']
    name: ChatFilterName = 'Paragraph Filter'
    warning_message: ChatFilterWarningMessage = 'Your message was too long'
    timeout_message: ChatFilterTimeoutMessage = 'Your message was too long'
    settings: ChatFilterParagraphSettings = ChatFilterParagraphSettings()


class ChatFilterParagraphUpdate(ChatFilterBaseUpdate):
    type: Literal['paragraph']
    settings: ChatFilterParagraphSettings | None = None


class ChatFilterParagraph(ChatFilterBase):
    type: Literal['paragraph']
    settings: ChatFilterParagraphSettings

    async def check_message(self, message: ChatMessageCreate) -> FilterMatchResult:
        return FilterMatchResult(
            filter=self,
            matched=len(message.message_without_parts()) > self.settings.max_length,
        )
