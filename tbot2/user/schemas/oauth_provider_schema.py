from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator


class OAuthProviderCreate(BaseModel):
    user_id: UUID
    provider: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    provider_user_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    access_token: Annotated[str, StringConstraints(min_length=1, max_length=1024)]
    refresh_token: (
        Annotated[str, StringConstraints(min_length=1, max_length=1024)] | None
    ) = None
    expires_at: datetime | None = None


class OAuthProviderUpdate(BaseModel):
    access_token: (
        Annotated[str, StringConstraints(min_length=1, max_length=1024)] | None
    ) = None
    refresh_token: (
        Annotated[str, StringConstraints(min_length=1, max_length=1024)] | None
    ) = None
    expires_at: datetime | None = None

    @field_validator('access_token', 'refresh_token')
    def check_not_none(cls, value: str | None):
        if value is None:
            raise ValueError('Must not be None')
        return value


class OAuthProvider(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    provider: str
    provider_user_id: str
    access_token: str
    refresh_token: str | None
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime | None


class OAuthProviderInfo(BaseModel):
    provider: str
    provider_user_id: str
    connected_at: datetime
