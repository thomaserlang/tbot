from pydantic import BaseModel


class SlotsResult(BaseModel):
    won: bool
    bet: int
    points: int
    points_name: str
    message: str
    emotes: list[str]
