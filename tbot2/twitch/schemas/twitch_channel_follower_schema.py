from datetime import datetime

from tbot2.common import BaseSchema


class ChannelFollower(BaseSchema):
    followed_at: datetime
    user_id: str
    user_name: str
    user_login: str
