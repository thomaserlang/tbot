from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema


class UserOAuthProvider(BaseSchema):
    id: UUID
    user_id: UUID
    provider: str
    provider_user_id: str
    created_at: datetime
    updated_at: datetime | None
