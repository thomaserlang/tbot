from typing import Annotated
from uuid import UUID

from pydantic import Field

from tbot2.common import BaseRequestSchema, BaseSchema


class SlotsSettingsUpdate(BaseRequestSchema):
    emotes: list[str] = ['MrDestructoid', 'SeriousSloth', 'OSFrog', 'OhMyDog']
    emote_pool_size: Annotated[int, Field(ge=1, le=255)] = 3
    payout_percent: Annotated[int, Field(ge=0, le=100)] = 95
    min_bet: Annotated[int, Field(ge=1, le=4294967295)] = 5
    max_bet: Annotated[int, Field(ge=0, le=4294967295)] = 0
    win_message: Annotated[str, Field(min_length=1, max_length=250)] = (
        '{emotes} you won {bet} {points_name} '
        'and now have {points} {points_name}'
    )
    lose_message: Annotated[str, Field(min_length=1, max_length=250)] = (
        '{emotes} you lost {bet} {points_name}'
    )
    allin_win_message: Annotated[str, Field(min_length=1, max_length=250)] = (
        '{emotes} you WON {bet} {points_name} and '
        'now have {points} {points_name} EZ'
    )
    allin_lose_message: Annotated[str, Field(min_length=1, max_length=250)] = (
        '{emotes} you lost {bet} {points_name} PepeLaugh'
    )


class SlotsSettings(BaseSchema):
    channel_id: UUID
    emotes: list[str]
    emote_pool_size: int
    payout_percent: int
    win_message: str
    lose_message: str
    allin_win_message: str
    allin_lose_message: str
    min_bet: int
    max_bet: int
