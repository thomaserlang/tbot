from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security

from tbot2.channel import ChannelScope
from tbot2.channel.actions.channel_bot_provider_actions import (
    disconnect_channel_bot_provider,
)
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.channel_oauth_provider_actions import (
    delete_channel_oauth_provider,
    get_channel_oauth_provider_by_id,
    get_channel_oauth_providers,
)
from ..schemas.channel_oauth_provider_schema import ChannelProvider

router = APIRouter()


@router.get(
    '/channels/{channel_id}/providers',
    name='Get Channel Providers',
)
async def get_channel_providers_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_READ])
    ],
) -> list[ChannelProvider]:
    await token_data.channel_has_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )
    providers = await get_channel_oauth_providers(
        channel_id=channel_id,
    )
    return [ChannelProvider.model_validate(provider) for provider in providers]


@router.get(
    '/channels/{channel_id}/providers/{channel_provider_id}',
)
async def get_channel_provider_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_READ])
    ],
) -> ChannelProvider:
    await token_data.channel_has_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )
    provider = await get_channel_oauth_provider_by_id(
        channel_id=channel_id,
        provider_id=channel_provider_id,
    )

    if not provider:
        raise HTTPException(
            status_code=404,
            detail='Channel provider not found',
        )

    return ChannelProvider.model_validate(provider)


@router.delete(
    '/channels/{channel_id}/providers/{channel_provider_id}',
    name='Delete Channel Provider',
    status_code=204,
)
async def delete_channel_provider_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_WRITE])
    ],
) -> None:
    await token_data.channel_has_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    await delete_channel_oauth_provider(
        channel_id=channel_id,
        channel_provider_id=channel_provider_id,
    )


@router.delete(
    '/channels/{channel_id}/providers/{channel_provider_id}/bot',
    name='Disconnect Channel Provider Bot',
    status_code=204,
)
async def disconnect_channel_provider_bot_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_WRITE])
    ],
) -> None:
    await token_data.channel_has_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    await disconnect_channel_bot_provider(
        channel_id=channel_id,
        channel_provider_id=channel_provider_id,
    )
