from tbot2.common import BaseSchema


class TwitchError(BaseSchema):
    error: str
    status: int
    message: str
