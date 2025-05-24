from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema, Provider


class ChannelProviderStream(BaseSchema):
    id: UUID
    channel_id: UUID
    channel_stream_id: UUID
    provider: Provider
    provider_channel_id: str
    provider_stream_id: str
    started_at: datetime
    ended_at: datetime | None
    avg_viewer_count: int | None
    peak_viewer_count: int | None
