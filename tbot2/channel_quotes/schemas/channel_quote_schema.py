from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChannelQuote(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    channel_id: UUID
    number: int
    message: str
    provider: str
    created_by_chatter_id: str
    created_by_display_name: str
    created_at: datetime
    updated_at: datetime | None = None
