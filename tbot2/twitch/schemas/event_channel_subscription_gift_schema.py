from typing import Literal

from tbot2.common import BaseSchema


class EventChannelSubscriptionGift(BaseSchema):
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    user_id: str
    user_login: str
    user_name: str
    total: int
    tier: str | Literal['1000', '2000', '3000']
    cumulative_total: int | None = None
    is_anonymous: bool
