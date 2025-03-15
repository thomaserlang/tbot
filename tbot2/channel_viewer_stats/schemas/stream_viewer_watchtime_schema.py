from uuid import UUID

from tbot2.common import BaseSchema


class StreamViewerWatchtime(BaseSchema):
    channel_id: UUID
    provider: str
    stream_id: str
    viewer_id: str
    watchtime: int
