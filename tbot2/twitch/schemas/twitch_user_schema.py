from datetime import datetime

from tbot2.common import BaseSchema


class TwitchUser(BaseSchema):
    id: str
    login: str
    display_name: str
    type: str
    broadcaster_type: str
    description: str
    profile_image_url: str
    offline_image_url: str
    view_count: int
    email: str | None = None
    created_at: datetime
