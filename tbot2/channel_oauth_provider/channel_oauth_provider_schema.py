from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints

from tbot2.common import BaseRequestSchema, BaseSchema, TProvider


class ChannelOAuthProvider(BaseSchema):
    id: UUID
    channel_id: UUID
    provider: TProvider
    provider_user_id: str | None
    access_token: str | None
    refresh_token: str | None
    expires_at: datetime | None
    scope: str | None
    name: str | None


class ChannelOAuthProviderRequest(BaseRequestSchema):
    provider_user_id: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    access_token: (
        Annotated[str, StringConstraints(min_length=1, max_length=2000)] | None
    ) = None
    refresh_token: (
        Annotated[str, StringConstraints(min_length=1, max_length=2000)] | None
    ) = None
    expires_at: datetime | None = None
    expires_in: int | None = None
    scope: Annotated[str, StringConstraints(min_length=1, max_length=2000)] | None = (
        None
    )
    name: Annotated[str, StringConstraints(min_length=1, max_length=255)] | None = None
