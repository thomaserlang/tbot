from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import ChatMessage, TProvider

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseSettings,
    ChatFilterBaseUpdate,
)


class ChatFilterEmoteSettings(ChatFilterBaseSettings):
    max_emotes: Annotated[int, Field(ge=0)] = 20


class ChatFilterEmoteCreate(ChatFilterBaseCreate):
    type: Literal['emote']
    name: str = 'Emote Filter'
    settings: ChatFilterEmoteSettings = ChatFilterEmoteSettings()


class ChatFilterEmoteUpdate(ChatFilterBaseUpdate):
    type: Literal['emote']
    settings: ChatFilterEmoteSettings | None = None


class ChatFilterEmote(ChatFilterBase):
    type: Literal['emote']
    settings: ChatFilterEmoteSettings

    async def check_message(self, message: ChatMessage) -> bool:
        if message.provider == TProvider.youtube:
            emote_count = message.message.count(':') // 2
            return emote_count > self.settings.max_emotes
        elif message.provider == TProvider.twitch:
            if not message.twitch_fragments:
                return False
            emote_count = sum(
                1 for fragment in message.twitch_fragments if fragment.type == 'emote'
            )
            return emote_count > self.settings.max_emotes
        return False
