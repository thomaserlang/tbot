from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class RouletteSettingsUpdate(BaseModel):
    win_chance: Annotated[int, Field(ge=0, le=100)] = 45
    win_message: Annotated[str, StringConstraints(min_length=1, max_length=250)] = (
        '@{user}, You won {bet} {points_name} and now have {points} {points_name}'
    )
    lose_message: Annotated[str, StringConstraints(min_length=1, max_length=250)] = (
        '@{user}, You lost {bet} {points_name} and now have {points} {points_name}'
    )
    allin_win_message: Annotated[
        str, StringConstraints(min_length=1, max_length=250)
    ] = '@{user}, You WON {bet} {points_name} and now have {points} {points_name} EZ'
    allin_lose_message: Annotated[
        str, StringConstraints(min_length=1, max_length=250)
    ] = '@{user}, You lost {bet} {points_name} PepeLaugh'
    min_bet: Annotated[int, Field(ge=0)] = 5
    max_bet: Annotated[int, Field(ge=0)] = 0


class RouletteSettings(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    channel_id: UUID
    win_chance: int
    win_message: str
    lose_message: str
    allin_win_message: str
    allin_lose_message: str
    min_bet: int
    max_bet: int
