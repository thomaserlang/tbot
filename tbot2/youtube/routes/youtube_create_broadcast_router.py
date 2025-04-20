from uuid import UUID

from fastapi import APIRouter, HTTPException

from tbot2.channel import (
    ChannelProviderPublic,
    ChannelProviderRequest,
    get_channel_provider_by_id,
    save_channel_provider,
)
from tbot2.contexts import get_session
from tbot2.youtube.actions.youtube_live_broadcast_actions import (
    create_new_broadcast_from_previous,
)

router = APIRouter()


@router.post(
    '/channels/{channel_id}/providers/{channel_provider_id}/youtube/broadcast',
    status_code=201,
)
async def youtube_create_broadcast_route(
    channel_id: UUID,
    channel_provider_id: UUID,
) -> ChannelProviderPublic:
    channel_provider = await get_channel_provider_by_id(
        channel_provider_id=channel_provider_id,
    )

    if not channel_provider or channel_provider.channel_id != channel_id:
        raise HTTPException(
            status_code=404,
            detail='Channel provider not found',
        )

    broadcast = await create_new_broadcast_from_previous(
        channel_provider=channel_provider,
    )
    async with get_session() as session:
        await save_channel_provider(
            channel_id=channel_id,
            provider='youtube',
            data=ChannelProviderRequest(
                stream_id=broadcast.id,
                stream_title=broadcast.snippet.title,
            ),
            session=session,
        )
        channel_provider = await get_channel_provider_by_id(
            channel_provider_id=channel_provider_id,
            session=session,
        )
        return ChannelProviderPublic.model_validate(channel_provider)
