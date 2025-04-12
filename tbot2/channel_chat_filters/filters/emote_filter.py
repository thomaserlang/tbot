from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import ChatMessage, TProvider

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


class ChatFilterEmoteSettings(ChatFilterBaseSettings):
    max_emotes: Annotated[int, Field(ge=0)] = 20


class ChatFilterEmoteCreate(ChatFilterBaseCreate):
    type: Literal['emote']
    name: ChatFilterName = 'Emote Filter'
    warning_message: ChatFilterWarningMessage = 'Chill with the emotes'
    timeout_message: ChatFilterTimeoutMessage = 'Chill with the emotes'
    settings: ChatFilterEmoteSettings = ChatFilterEmoteSettings()


class ChatFilterEmoteUpdate(ChatFilterBaseUpdate):
    type: Literal['emote']
    settings: ChatFilterEmoteSettings | None = None


class ChatFilterEmote(ChatFilterBase):
    type: Literal['emote']
    settings: ChatFilterEmoteSettings

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        if message.provider == TProvider.youtube:
            emote_count = message.message.count(':') // 2
            return FilterMatchResult(
                filter=self, matched=emote_count > self.settings.max_emotes
            )
        elif message.provider == TProvider.twitch:
            if not message.twitch_fragments:
                return FilterMatchResult(filter=self, matched=False)
            emote_count = sum(
                1 for fragment in message.twitch_fragments if fragment.type == 'emote'
            )
            return FilterMatchResult(
                filter=self, matched=emote_count > self.settings.max_emotes
            )
        return FilterMatchResult(filter=self, matched=False)
