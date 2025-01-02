from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from tbot2.common import TProvider

from .twitch_schemas import TwitchBadge, TwitchMessageFragment


class ChatMessage(BaseModel):
    type: Literal['message', 'notice', 'mod_action']
    sub_type: str | None = None
    created_at: datetime
    provider: TProvider
    "The provider of the chat message, e.g. 'twitch' or 'youtube'"
    provider_id: str
    'The ID of e.g. the Twitch channel or YouTube live stream'
    channel_id: UUID
    'The ID of the TBot user account aka the streamer'
    chatter_id: str
    chatter_name: str
    chatter_display_name: str
    chatter_color: str | None = None
    message: str
    msg_id: str
    twitch_badges: list[TwitchBadge] | None = None
    twitch_fragments: list[TwitchMessageFragment] | None = None
