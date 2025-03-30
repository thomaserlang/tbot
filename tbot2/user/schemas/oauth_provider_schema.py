from datetime import datetime
from uuid import UUID

from tbot2.common import BaseSchema, TProvider


class UserOAuthProvider(BaseSchema):
    id: UUID
    user_id: UUID
    provider: TProvider
    provider_user_id: str
    created_at: datetime
    updated_at: datetime | None
