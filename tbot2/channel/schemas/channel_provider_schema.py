from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, computed_field

from tbot2.bot_providers import BotProvider, BotProviderPublic
from tbot2.common import (
    BaseRequestSchema,
    BaseSchema,
    Provider,
    channel_provider_scopes,
)
from tbot2.contexts import AsyncSession
from tbot2.exceptions import ErrorMessage


class ChannelProvider(BaseSchema):
    id: UUID
    channel_id: UUID
    provider: Provider
    provider_user_id: str | None
    access_token: str | None
    refresh_token: str | None
    expires_at: datetime | None
    scope: str | None
    name: str | None
    bot_provider_id: UUID | None
    bot_provider: BotProvider | None

    async def get_default_or_system_bot_provider(
        self,
        session: AsyncSession | None = None,
    ) -> BotProvider:
        from tbot2.channel import get_channel_bot_provider

        bot_provider = self.bot_provider
        if not bot_provider:
            bot_provider = await get_channel_bot_provider(
                provider=self.provider,
                channel_id=self.channel_id,
                session=session,
            )
            if not bot_provider:
                raise ErrorMessage(f'No bot provider found for {self.provider}')
        return bot_provider


class ChannelProviderPublic(BaseSchema):
    id: UUID
    channel_id: UUID
    provider: Provider
    name: str | None
    scope: str | None
    bot_provider_id: UUID | None
    bot_provider: BotProviderPublic | None

    @computed_field
    def scope_needed(self) -> bool:
        required_scopes = set(channel_provider_scopes.get(self.provider, '').split(' '))
        scopes: set[str] = set(self.scope.split(' ')) if self.scope else set()
        return bool(required_scopes - scopes)


class ChannelProviderRequest(BaseRequestSchema):
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
    bot_provider_id: UUID | None = None
