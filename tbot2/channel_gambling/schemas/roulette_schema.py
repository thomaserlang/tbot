from pydantic import BaseModel


class RouletteResult(BaseModel):
    won: bool
    bet: int
    points: int
    points_name: str
    message: str