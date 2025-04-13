from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema, TProvider


class ChannelProviderStream(BaseSchema):
    id: UUID
    channel_id: UUID
    channel_stream_id: UUID
    provider: TProvider
    provider_id: str
    provider_stream_id: str
    started_at: datetime
    ended_at: datetime | None
