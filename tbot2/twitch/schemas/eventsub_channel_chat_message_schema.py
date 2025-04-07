from typing import Literal

from pydantic import BaseModel

from tbot2.common.schemas.twitch_schemas import (
    TwitchBadge,
    TwitchMessageFragment,
)


class ChatMessageFragmentMention(BaseModel):
    user_id: str
    user_login: str
    user_name: str


class ChannelChatMessageMessage(BaseModel):
    text: str
    fragments: list[TwitchMessageFragment]


class ChannelChatMessage(BaseModel):
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    source_broadcaster_user_id: str | None
    source_broadcaster_user_login: str | None
    source_broadcaster_user_name: str | None
    chatter_user_id: str
    chatter_user_login: str
    chatter_user_name: str
    message_id: str
    source_message_id: str | None
    message: ChannelChatMessageMessage
    message_type: (
        Literal[
            'text',
            'channel_points_highlighted',
            'channel_points_sub_only',
            'user_intro',
        ]
        | str
    )
    badges: list[TwitchBadge]
    color: str
