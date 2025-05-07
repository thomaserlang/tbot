from datetime import datetime
from uuid import UUID

from tbot2.common import BaseRequestSchema, BaseSchema, Provider


class QueueViewer(BaseSchema):
    id: UUID
    channel_queue_id: UUID
    position: int
    provider: Provider
    provider_viewer_id: str
    display_name: str
    created_at: datetime


class QueueViewerCreate(BaseRequestSchema):
    provider: Provider
    provider_viewer_id: str
    display_name: str
