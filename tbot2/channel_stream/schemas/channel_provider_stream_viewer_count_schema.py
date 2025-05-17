from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema


class ChannelProviderStreamViewerCount(BaseSchema):
    channel_provider_stream_id: UUID
    timestamp: datetime
    viewer_count: int
