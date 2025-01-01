from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChatterPoints(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    channel_id: UUID
    chatter_id: str
    provider: str
    points: int
