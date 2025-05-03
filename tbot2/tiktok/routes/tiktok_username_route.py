from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Security

from tbot2.channel_provider import (
    ChannelProvider,
    ChannelProviderRequest,
    ChannelProviderScope,
    save_channel_provider,
)
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated
from tbot2.tiktok.actions.task_tiktok_action import TikTokLiveClient

router = APIRouter()


@router.post('/channels/{channel_id}/register-provider/tiktok')
async def register_tiktok_username_route(
    channel_id: UUID,
    username: Annotated[
        str,
        Body(min_length=1, max_length=200, embed=True),
    ],
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelProviderScope.WRITE])
    ],
) -> ChannelProvider:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.ADMIN,
    )
    username = TikTokLiveClient.parse_unique_id(username)
    channel_provider = await save_channel_provider(
        channel_id=channel_id,
        provider='tiktok',
        data=ChannelProviderRequest(
            provider_user_name=username,
            provider_user_display_name=username,
            provider_user_id=username,
            stream_id=username,
            stream_title=username,
            stream_chat_id=username,
        ),
    )
    return channel_provider
