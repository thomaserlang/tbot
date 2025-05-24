from pydantic import Field

from tbot2.channel_activity.types.activity_types import ActivityType
from tbot2.common import BaseRequestSchema


class UserSettings(BaseRequestSchema):
    activity_feed_not_types: list[ActivityType | str] = Field(default_factory=list)
    activity_feed_type_min_count: dict[ActivityType | str, int] = Field(
        default_factory=dict
    )
    activity_feed_read_indicator: bool = False
