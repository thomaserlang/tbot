from tbot2.common import BaseSchema


class SlotsResult(BaseSchema):
    won: bool
    bet: int
    points: int
    points_name: str
    message: str
    emotes: list[str]
