from typing import Literal

from tbot2.common import BaseSchema

from .queue_viewer_schema import QueueViewer


class QueueEvent(BaseSchema):
    type: Literal[
        'channel_queue_viewer_created',
        'channel_queue_viewer_deleted',
        'channel_queue_viewer_moved',
        'channel_queue_cleared',
    ]
    channel_queue_viewer: QueueViewer | None = None
