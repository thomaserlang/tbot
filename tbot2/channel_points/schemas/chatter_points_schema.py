from uuid import UUID

from tbot2.common import BaseSchema


class ChatterPoints(BaseSchema):
    channel_id: UUID
    chatter_id: str
    provider: str
    points: int


class ChatterPointsRank(ChatterPoints):
    rank: int = 0
