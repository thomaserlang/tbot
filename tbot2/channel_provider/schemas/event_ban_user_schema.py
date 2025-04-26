from tbot2.common import BaseRequestSchema

from .channel_provider_schema import ChannelProvider


class EventBanUser(BaseRequestSchema):
    channel_provider: ChannelProvider
    ban_duration: int | None = None
    provider_viewer_id: str


class EventUnbanUser(BaseRequestSchema):
    channel_provider: ChannelProvider
    provider_viewer_id: str
