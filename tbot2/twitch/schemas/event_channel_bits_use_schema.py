from typing import Literal

from tbot2.common import BaseSchema

from .event_channel_chat_message_schema import ChannelChatMessageMessage


class PowerUpEmote(BaseSchema):
    id: str
    'The ID that uniquely identifies this emote.'
    name: str
    'The human readable emote token.'


class PowerUp(BaseSchema):
    type: str | Literal['message_effect', 'celebration', 'gigantify_an_emote']
    emote: PowerUpEmote | None = None
    'Optional. Emote associated with the reward.'
    message_effect_id: str | None = None
    'Optional. The ID of the message effect.'


class EventChannelBitsUse(BaseSchema):
    broadcaster_user_id: str
    'The User ID of the channel where the Bits were redeemed.'
    broadcaster_user_login: str
    'The login of the channel where the Bits were used.'
    broadcaster_user_name: str
    'The display name of the channel where the Bits were used.'
    user_id: str
    'The User ID of the redeeming user.'
    user_login: str
    'The login name of the redeeming user.'
    user_name: str
    'The display name of the redeeming user.'
    bits: int
    'The number of Bits used.'
    type: Literal['cheer', 'power_up', 'combo']
    'Possible values are: cheer, power_up, combo'
    message: ChannelChatMessageMessage | None = None
    'Optional. An object that contains the user message and emote information needed to recreate the message.'  # noqa: E501
    power_up: PowerUp | None = None
    'Optional. Data about Power-up.'
