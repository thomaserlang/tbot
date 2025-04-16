from datetime import date
from uuid import UUID

from tbot2.channel_stream import ChannelProviderStream
from tbot2.common import BaseSchema, Provider

from .viewer_schemas import ViewerName


class ChannelViewerStats(BaseSchema):
    channel_id: UUID
    provider: Provider
    provider_viewer_id: str
    streams: int = 0
    streams_row: int = 0
    streams_row_peak: int = 0
    streams_row_peak_date: date | None = None
    watchtime: int = 0
    last_channel_provider_stream: ChannelProviderStream | None = None


class ChannelViewer(BaseSchema):
    viewer: ViewerName
    stats: ChannelViewerStats


class ChannelViewerStatsUpdate(BaseSchema):
    streams: int | None = 0
    streams_row: int | None = 0
    streams_row_peak: int | None = 0
    streams_row_peak_date: date | None = None
    last_channel_provider_stream_id: UUID | None = None


class StreamViewerWatchtime(BaseSchema):
    channel_provider_stream_id: UUID
    provider_viewer_id: str
    watchtime: int


class ViewerStream(BaseSchema):
    channel_provider_stream: ChannelProviderStream
    viewer_watchtime: StreamViewerWatchtime
