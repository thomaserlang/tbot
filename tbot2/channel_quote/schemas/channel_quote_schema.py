from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema, Provider


class ChannelQuote(BaseSchema):
    id: UUID
    channel_id: UUID
    number: int
    message: str
    provider: Provider
    created_by_chatter_id: str
    created_by_display_name: str
    created_at: datetime
    updated_at: datetime | None = None
