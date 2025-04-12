from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema


class ChannelProviderStream(BaseSchema):
    id: UUID
    channel_id: UUID
    channel_stream_id: UUID
    provider: str
    provider_stream_id: str
    started_at: datetime
    ended_at: datetime | None
