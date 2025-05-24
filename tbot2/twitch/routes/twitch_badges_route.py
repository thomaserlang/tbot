import asyncio
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security

from tbot2.channel_chat_message import ChatMessageScope
from tbot2.channel_provider import get_channel_provider
from tbot2.common import TokenData
from tbot2.dependecies import authenticated

from ..actions.twitch_badges_action import (
    twitch_channel_badges,
    twitch_global_badges,
)
from ..schemas.twitch_chat_badge_schema import ChannelBadges

router = APIRouter()


@router.get('/channels/{channel_id}/twitch-badges', name='Get Twitch Badges')
async def get_twitch_badges_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChatMessageScope.READ])
    ],
) -> ChannelBadges:
    provider = await get_channel_provider(
        channel_id=channel_id,
        provider='twitch',
    )
    if not provider:
        raise HTTPException(
            status_code=400,
            detail='No Twitch provider found for this channel',
        )

    data = await asyncio.gather(
        twitch_channel_badges(provider.provider_user_id or ''),
        twitch_global_badges(),
    )

    return ChannelBadges(
        channel_badges=data[0] or [],
        global_badges=data[1] or [],
    )
