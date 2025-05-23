from datetime import datetime

from tbot2.common import BaseSchema


class EventChannelFollow(BaseSchema):
    user_id: str
    user_login: str
    user_name: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    followed_at: datetime
