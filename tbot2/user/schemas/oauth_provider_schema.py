from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints


class UserOAuthProviderCreate(BaseModel):
    user_id: UUID
    provider: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    provider_user_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]


class UserOAuthProvider(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    provider: str
    provider_user_id: str
    created_at: datetime
    updated_at: datetime | None
