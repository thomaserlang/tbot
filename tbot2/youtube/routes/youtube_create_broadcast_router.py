from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security

from tbot2.channel_provider import (
    ChannelProviderPublic,
    ChannelProviderRequest,
    ChannelProviderScope,
    create_or_update_channel_provider,
    get_channel_provider_by_id,
)
from tbot2.common import TAccessLevel, TokenData
from tbot2.contexts import get_session
from tbot2.dependecies import authenticated

from ..actions.youtube_live_broadcast_actions import (
    create_new_broadcast_from_previous,
)
from ..schemas.youtube_live_broadcast_schema import LiveBroadcastInsert

router = APIRouter()


@router.post(
    '/channels/{channel_id}/providers/{channel_provider_id}/youtube/broadcast',
    status_code=201,
)
async def youtube_create_broadcast_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChannelProviderScope.WRITE]),
    ],
    data: LiveBroadcastInsert,
) -> ChannelProviderPublic:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )

    channel_provider = await get_channel_provider_by_id(
        channel_provider_id=channel_provider_id,
    )

    if not channel_provider or channel_provider.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Channel provider not found',
        )

    broadcast = await create_new_broadcast_from_previous(
        channel_id=channel_provider.channel_id,
        overwrite_data=data,
    )
    async with get_session() as session:
        await create_or_update_channel_provider(
            channel_id=channel_id,
            provider='youtube',
            data=ChannelProviderRequest(
                live_stream_id=broadcast.id,
                stream_title=broadcast.snippet.title,
                stream_chat_id=broadcast.snippet.live_chat_id,
            ),
            session=session,
        )
        channel_provider = await get_channel_provider_by_id(
            channel_provider_id=channel_provider_id,
            session=session,
        )
        return ChannelProviderPublic.model_validate(channel_provider)
