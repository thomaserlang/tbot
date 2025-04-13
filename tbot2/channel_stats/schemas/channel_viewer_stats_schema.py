from datetime import date
from uuid import UUID

from tbot2.common import BaseSchema


class ChannelViewerStats(BaseSchema):
    channel_id: UUID
    provider: str
    provider_viewer_id: str
    streams: int = 0
    streams_row: int = 0
    streams_row_peak: int = 0
    streams_row_peak_date: date | None = None
    last_channel_provider_stream_id: UUID | None = None


class ChannelViewerStatsUpdate(BaseSchema):
    streams: int | None = 0
    streams_row: int | None = 0
    streams_row_peak: int | None = 0
    streams_row_peak_date: date | None = None
    last_channel_provider_stream_id: UUID | None = None
