from tbot2.common import BaseSchema


class RouletteResult(BaseSchema):
    won: bool
    bet: int
    points: int
    points_name: str
    message: str
