from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema, Provider


class UserOAuthProvider(BaseSchema):
    id: UUID
    user_id: UUID
    provider: Provider
    provider_channel_id: str
    created_at: datetime
    updated_at: datetime | None
