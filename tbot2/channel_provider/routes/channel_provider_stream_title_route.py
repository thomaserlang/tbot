from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Security

from tbot2.channel_provider import ChannelProviderScope
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.channel_provider_actions import (
    get_channel_provider_by_id,
    save_channel_provider,
)
from ..event_types import fire_event_update_stream_title
from ..schemas.channel_provider_schema import (
    ChannelProviderPublic,
    ChannelProviderRequest,
)

router = APIRouter()


@router.put(
    '/channels/{channel_id}/providers/{channel_provider_id}/stream-title',
    name='Update stream title',
    status_code=200,
)
async def update_stream_title_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelProviderScope.WRITE])
    ],
    stream_title: Annotated[str, Body(embed=True, min_length=1, max_length=140)],
) -> ChannelProviderPublic:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    channel_provider = await get_channel_provider_by_id(
        channel_provider_id=channel_provider_id,
    )
    if not channel_provider or channel_provider.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Channel provider not found',
        )

    channel_provider = await save_channel_provider(
        channel_id=channel_id,
        provider=channel_provider.provider,
        data=ChannelProviderRequest(stream_title=stream_title),
    )

    await fire_event_update_stream_title(
        channel_provider=channel_provider,
        stream_title=stream_title,
    )
    return ChannelProviderPublic.model_validate(channel_provider)
