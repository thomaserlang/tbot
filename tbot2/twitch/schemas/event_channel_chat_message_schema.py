from typing import Literal

from tbot2.common import BaseSchema


class ChannelChatMessageCheermote(BaseSchema):
    prefix: str
    'The name portion of the Cheermote string that you use in chat to cheer Bits.'
    bits: int
    'The amount of Bits cheered.'
    tier: int
    'The tier level of the cheermote.'


class ChannelChatMessageEmote(BaseSchema):
    id: str
    'An ID that uniquely identifies this emote.'
    emote_set_id: str
    'An ID that identifies the emote set that the emote belongs to.'
    owner_id: str
    'The ID of the broadcaster who owns the emote.'
    format: list[Literal['animated', 'static'] | str]
    'The formats that the emote is available in.'


class ChannelChatMessageMention(BaseSchema):
    user_id: str
    'The user ID of the mentioned user.'
    user_name: str
    'The user name of the mentioned user.'
    user_login: str
    'The user login of the mentioned user.'


class ChannelChatMessageFragment(BaseSchema):
    type: Literal['text', 'cheermote', 'emote', 'mention'] | str
    'The type of message fragment.'
    text: str
    'Message text in fragment.'
    cheermote: ChannelChatMessageCheermote | None = None
    'Optional. Metadata pertaining to the cheermote.'
    emote: ChannelChatMessageEmote | None = None
    'Optional. Metadata pertaining to the emote.'
    mention: ChannelChatMessageMention | None = None
    'Optional. Metadata pertaining to the mention.'


class ChannelChatMessageMessage(BaseSchema):
    text: str
    'The chat message in plain text.'
    fragments: list[ChannelChatMessageFragment]
    'Ordered list of chat message fragments.'


class ChannelChatMessageBadge(BaseSchema):
    set_id: str
    'An ID that identifies this set of chat badges.'
    id: str
    'An ID that identifies this version of the badge.'
    info: str
    'Contains metadata related to the chat badges in the badges tag.'


class ChannelChatMessageCheer(BaseSchema):
    bits: int
    'The amount of Bits the user cheered.'


class ChannelChatMessageReply(BaseSchema):
    parent_message_id: str
    'An ID that uniquely identifies the parent message that this message is replying to.'  # noqa: E501
    parent_message_body: str
    'The message body of the parent message.'
    parent_user_id: str
    'User ID of the sender of the parent message.'
    parent_user_name: str
    'User name of the sender of the parent message.'
    parent_user_login: str
    'User login of the sender of the parent message.'
    thread_message_id: str
    'An ID that identifies the parent message of the reply thread.'
    thread_user_id: str
    "User ID of the sender of the thread's parent message."
    thread_user_name: str
    "User name of the sender of the thread's parent message."
    thread_user_login: str
    "User login of the sender of the thread's parent message."


class ChannelChatMessageSourceBadge(BaseSchema):
    set_id: str
    'The ID that identifies this set of chat badges.'
    id: str
    'The ID that identifies this version of the badge.'
    info: str
    'Contains metadata related to the chat badges in the badges tag.'


class EventChannelChatMessage(BaseSchema):
    broadcaster_user_id: str
    'The broadcaster user ID.'
    broadcaster_user_name: str
    'The broadcaster display name.'
    broadcaster_user_login: str
    'The broadcaster login.'
    chatter_user_id: str
    'The user ID of the user that sent the message.'
    chatter_user_name: str
    'The user name of the user that sent the message.'
    chatter_user_login: str
    'The user login of the user that sent the message.'
    message_id: str
    'A UUID that identifies the message.'
    message: ChannelChatMessageMessage
    'The structured chat message.'
    message_type: (
        Literal[
            'text',
            'channel_points_highlighted',
            'channel_points_sub_only',
            'user_intro',
            'power_ups_message_effect',
            'power_ups_gigantified_emote',
        ]
        | str
    )
    'The type of message.'
    badges: list[ChannelChatMessageBadge]
    'List of chat badges.'
    cheer: ChannelChatMessageCheer | None = None
    'Optional. Metadata if this message is a cheer.'
    color: str
    "The color of the user's name in the chat room."
    reply: ChannelChatMessageReply | None = None
    'Optional. Metadata if this message is a reply.'
    channel_points_custom_reward_id: str | None = None
    'Optional. The ID of a channel points custom reward that was redeemed.'
    source_broadcaster_user_id: str | None = None
    'Optional. The broadcaster user ID of the channel the message was sent from.'
    source_broadcaster_user_name: str | None = None
    'Optional. The user name of the broadcaster of the channel the message was sent from.'  # noqa: E501
    source_broadcaster_user_login: str | None = None
    'Optional. The login of the broadcaster of the channel the message was sent from.'
    source_message_id: str | None = None
    'Optional. The UUID that identifies the source message from the channel the message was sent from.'  # noqa: E501
    source_badges: list[ChannelChatMessageSourceBadge] | None = None
    'Optional. The list of chat badges for the chatter in the channel the message was sent from.'  # noqa: E501
    is_source_only: bool | None = None
    'Optional. Determines if a message delivered during a shared chat session is only sent to the source channel.'  # noqa: E501
