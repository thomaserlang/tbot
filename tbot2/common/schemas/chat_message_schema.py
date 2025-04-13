from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel
from typing_extensions import Doc

from ..types.access_level_type import TAccessLevel
from ..types.provider_type import Provider
from .twitch_schemas import TwitchBadge, TwitchMessageFragment


class ChatMessage(BaseModel):
    type: Literal['message', 'notice', 'mod_action']
    sub_type: str | None = None
    created_at: datetime
    provider: Provider
    provider_id: Annotated[
        str, Doc('The ID of the chat message in the provider system')
    ]
    channel_id: Annotated[UUID, Doc('The ID of the TBot channel')]
    chatter_id: str
    chatter_name: str
    chatter_display_name: str
    chatter_color: str | None = None
    message: str
    msg_id: str
    twitch_badges: list[TwitchBadge] | None = None
    twitch_fragments: list[TwitchMessageFragment] | None = None

    def message_without_fragments(self) -> str:
        if not self.twitch_fragments:
            return self.message
        return ''.join(
            fragment.text
            for fragment in self.twitch_fragments
            if fragment.type == 'text'
        )

    @property
    def access_level(self) -> TAccessLevel:
        if self.twitch_badges:
            for badge in self.twitch_badges:
                match badge.set_id:
                    case 'moderator':
                        return TAccessLevel.MOD
                    case 'broadcaster':
                        return TAccessLevel.OWNER
                    case 'vip':
                        return TAccessLevel.VIP
                    case _:
                        return TAccessLevel.PUBLIC
        return TAccessLevel.PUBLIC
