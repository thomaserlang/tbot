from datetime import datetime
from typing import Literal

from tbot2.common import BaseSchema


class MessageEmote(BaseSchema):
    id: str
    'The emote ID.'
    begin: int
    'The index of where the Emote starts in the text.'
    end: int
    'The index of where the Emote ends in the text.'


class Message(BaseSchema):
    text: str
    'The text of the chat message.'
    emotes: list[MessageEmote] | None = None


class UnlockedEmote(BaseSchema):
    id: str
    'The emote ID.'
    name: str
    'The human readable emote token.'


RewardType = Literal[
    'single_message_bypass_sub_mode',
    'send_highlighted_message',
    'random_sub_emote_unlock',
    'chosen_sub_emote_unlock',
    'chosen_modified_sub_emote_unlock',
    'message_effect',
    'gigantify_an_emote',
    'celebration',
]


class Reward(BaseSchema):
    type: str | RewardType
    'The type of reward.'  # noqa: E501
    cost: int
    'The reward cost.'
    unlocked_emote: UnlockedEmote | None = None
    'Optional. Emote that was unlocked.'


class EventChannelPointsAutomaticRewardRedemption(BaseSchema):
    broadcaster_user_id: str
    'The ID of the channel where the reward was redeemed.'
    broadcaster_user_login: str
    'The login of the channel where the reward was redeemed.'
    broadcaster_user_name: str
    'The display name of the channel where the reward was redeemed.'
    user_id: str
    'The ID of the redeeming user.'
    user_login: str
    'The login of the redeeming user.'
    user_name: str
    'The display name of the redeeming user.'
    id: str
    'The ID of the Redemption.'
    reward: Reward
    'An object that contains the reward information.'
    message: Message
    'An object that contains the user message and emote information needed to recreate the message.'  # noqa: E501
    user_input: str | None = None
    'Optional. A string that the user entered if the reward requires input.'
    redeemed_at: datetime
