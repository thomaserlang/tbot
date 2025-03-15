from datetime import date, datetime
from uuid import UUID

from tbot2.common import BaseSchema


class ChannelViewerStats(BaseSchema):
    channel_id: UUID
    provider: str
    viewer_id: str
    streams: int = 0
    streams_row: int = 0
    streams_row_peak: int = 0
    streams_row_peak_date: date | None = None
    last_stream_id: str | None = None
    last_stream_at: datetime | None = None


class ChannelViewerStatsUpdate(BaseSchema):
    streams: int | None = 0
    streams_row: int | None = 0
    streams_row_peak: int | None = 0
    streams_row_peak_date: date | None = None
    last_stream_id: str | None = None
    last_stream_at: datetime | None = None
