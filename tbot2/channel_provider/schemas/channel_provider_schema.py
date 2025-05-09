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
from tbot2.common.exceptions import ErrorMessage
from tbot2.contexts import AsyncSession


class ChannelProviderBase(BaseSchema):
    id: UUID
    channel_id: UUID
    provider: Provider
    provider_user_id: str | None
    provider_user_name: str | None
    provider_user_display_name: str | None
    scope: str | None
    stream_title: str | None
    stream_id: str | None
    stream_live: bool = False
    stream_live_at: datetime | None = None
    stream_chat_id: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def scope_needed(self) -> bool:
        if not channel_provider_scopes.get(self.provider):
            return False
        required_scopes = set(channel_provider_scopes.get(self.provider, '').split(' '))
        scopes: set[str] = set(self.scope.split(' ')) if self.scope else set()
        return bool(required_scopes - scopes)


class ChannelProvider(ChannelProviderBase):
    bot_provider: BotProvider | None

    async def get_default_or_system_bot_provider(
        self,
        session: AsyncSession | None = None,
    ) -> BotProvider:
        from ..actions.channel_bot_provider_actions import (
            get_channel_bot_provider,
        )

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


class ChannelProviderPublic(ChannelProviderBase):
    bot_provider: BotProviderPublic | None


class ChannelProviderRequest(BaseRequestSchema):
    provider_user_id: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    provider_user_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    provider_user_display_name: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    scope: Annotated[str, StringConstraints(min_length=1, max_length=2000)] | None = (
        None
    )
    bot_provider_id: UUID | None = None
    stream_title: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    stream_id: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
    """
    Used to update the channel provider's stream_id. 
    This is meant to be the id to watch the stream. 
    For Twitch it would be the username and for YouTube the broadcast id.
    """
    stream_live: bool = False
    stream_live_at: datetime | None = None
    stream_chat_id: (
        Annotated[str, StringConstraints(min_length=1, max_length=255)] | None
    ) = None
