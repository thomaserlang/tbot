from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChatterGamblingStatsUpdate(BaseModel):
    slots_wins: int = 0
    slots_losses: int = 0
    roulette_wins: int = 0
    roulette_losses: int = 0


class ChatterGamblingStats(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    channel_id: UUID
    chatter_id: str
    provider: str
    slots_wins: int = 0
    slots_losses: int = 0
    roulette_wins: int = 0
    roulette_losses: int = 0
