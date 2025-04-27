from uuid import UUID

from tbot2.common import BaseRequestSchema, BaseSchema, Provider


class ChatterGamblingStatsUpdate(BaseRequestSchema):
    slots_wins: int = 0
    slots_losses: int = 0
    roulette_wins: int = 0
    roulette_losses: int = 0


class ChatterGamblingStats(BaseSchema):
    channel_id: UUID
    provider_viewer_id: str
    provider: Provider
    slots_wins: int = 0
    slots_losses: int = 0
    roulette_wins: int = 0
    roulette_losses: int = 0
