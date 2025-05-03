from tbot2.common import BaseSchema


class Chatter(BaseSchema):
    user_id: str
    user_login: str
    user_name: str
