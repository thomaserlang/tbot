from tbot2.common import BaseSchema


class TikTokUserInfoSchema(BaseSchema):
    open_id: str
    display_name: str
    username: str
