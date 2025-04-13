from uuid import UUID

from tbot2.common import BaseSchema


class StreamViewerWatchtime(BaseSchema):
    channel_provider_stream_id: UUID
    provider_viewer_id: str
    watchtime: int
