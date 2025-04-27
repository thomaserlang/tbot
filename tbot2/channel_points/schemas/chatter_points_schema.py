from uuid import UUID

from tbot2.common import BaseSchema, Provider


class ChatterPoints(BaseSchema):
    channel_id: UUID
    provider_viewer_id: str
    provider: Provider
    points: int


class ChatterPointsRank(ChatterPoints):
    rank: int = 0
