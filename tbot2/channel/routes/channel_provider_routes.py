from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Security

from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.channel_oauth_provider_actions import (
    get_channel_oauth_providers,
)
from ..schemas.channel_oauth_provider_schema import ChannelProvider

router = APIRouter()


@router.get(
    '/channels/{channel_id}/providers',
    name='Get Channel Providers',
    response_model=list[ChannelProvider],
)
async def get_channel_providers_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
):
    await token_data.channel_has_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )
    providers = await get_channel_oauth_providers(
        channel_id=channel_id,
    )
    return providers
