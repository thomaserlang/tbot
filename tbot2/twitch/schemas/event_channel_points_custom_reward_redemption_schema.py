from datetime import datetime
from typing import Literal
from uuid import UUID

from tbot2.common import BaseSchema


class Reward(BaseSchema):
    id: UUID
    'The reward identifier.'
    title: str
    'The reward name.'
    cost: int
    'The reward cost.'
    prompt: str
    'The reward description.'


class EventChannelPointsCustomRewardRedemption(BaseSchema):
    id: str
    'The redemption identifier.'
    broadcaster_user_id: str
    'The requested broadcaster ID.'
    broadcaster_user_login: str
    'The requested broadcaster login.'
    broadcaster_user_name: str
    'The requested broadcaster display name.'
    user_id: str
    'User ID of the user that redeemed the reward.'
    user_login: str
    'Login of the user that redeemed the reward.'
    user_name: str
    'Display name of the user that redeemed the reward.'
    user_input: str | None = None
    'The user input provided. Empty string if not provided.'
    status: Literal['unknown', 'unfulfilled', 'fulfilled', 'canceled'] | str
    'Defaults to unfulfilled. Possible values are unknown, unfulfilled, fulfilled, and canceled.'  # noqa: E501
    reward: Reward
    'Basic information about the reward that was redeemed, at the time it was redeemed.'
    redeemed_at: datetime


class EventChannelPointsCustomRewardRedemptionUpdate(
    EventChannelPointsCustomRewardRedemption
): ...
