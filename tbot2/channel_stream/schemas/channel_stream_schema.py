from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema


class ChannelStream(BaseSchema):
    id: UUID
    channel_id: UUID
    started_at: datetime
