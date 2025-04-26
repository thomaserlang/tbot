from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints

from tbot2.common import BaseSchema


class ChannelProviderOAuth(BaseSchema):
    channel_provider_id: UUID
    access_token: str
    refresh_token: str
    expires_at: datetime


class ChannelProviderOAuthRequest(BaseSchema):
    access_token: Annotated[str, StringConstraints(min_length=1, max_length=2000)]
    refresh_token: Annotated[str, StringConstraints(min_length=1, max_length=2000)]
    expires_in: int
