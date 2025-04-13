from typing import Annotated
from uuid import UUID

from pydantic import Field, StringConstraints

from tbot2.common import BaseRequestSchema, BaseSchema


class ChannelPointSettingsUpdate(BaseRequestSchema):
    enabled: bool = True
    points_name: Annotated[str, StringConstraints(min_length=1, max_length=45)] = (
        'points'
    )
    points_per_min: Annotated[int, Field(ge=0, le=65535)] = 10
    points_per_min_sub_multiplier: Annotated[int, Field(ge=0, le=255)] = 2
    points_per_sub: Annotated[int, Field(ge=0, le=65535)] = 1000
    points_per_cheer: Annotated[int, Field(ge=0, le=65535)] = 2
    ignore_users: list[str] = []


class ChannelPointSettings(BaseSchema):
    channel_id: UUID
    enabled: bool = False
    points_name: str = 'points'
    points_per_min: int = 10
    points_per_min_sub_multiplier: int = 2
    points_per_sub: int = 1000
    points_per_cheer: int = 2
    ignore_users: list[str] = []
