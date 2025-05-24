from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, computed_field

from tbot2.common import BaseRequestSchema, BaseSchema, Provider, bot_provider_scopes


class BotProvider(BaseSchema):
    id: UUID
    provider: Provider
    provider_channel_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    scope: str | None
    name: str | None

    @computed_field
    def scope_needed(self) -> bool:
        required_scopes = set(bot_provider_scopes.get(self.provider, '').split(' '))
        scopes: set[str] = set(self.scope.split(' ')) if self.scope else set()
        return bool(required_scopes - scopes)


class BotProviderPublic(BaseSchema):
    id: UUID
    provider: Provider
    provider_channel_id: str | None
    scope: str | None
    name: str | None

    @computed_field
    def scope_needed(self) -> bool:
        required_scopes = set(bot_provider_scopes.get(self.provider, '').split(' '))
        scopes: set[str] = set(self.scope.split(' ')) if self.scope else set()
        return bool(required_scopes - scopes)


class BotProviderRequest(BaseRequestSchema):
    provider: Provider
    provider_channel_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
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
    system_default: bool | None = None
