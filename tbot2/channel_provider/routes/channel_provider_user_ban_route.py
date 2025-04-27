from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Security

from tbot2.auth_backend import TokenData
from tbot2.common import TAccessLevel
from tbot2.dependecies import authenticated

from ..actions.channel_provider_actions import get_channel_provider_by_id
from ..event_types import fire_event_ban_user, fire_event_unban_user
from ..schemas.event_ban_user_schema import EventBanUser, EventUnbanUser
from ..types import ChannelProviderScope

router = APIRouter()


@router.post(
    '/channels/{channel_id}/providers/{channel_provider_id}/user-ban',
    name='Ban/timeout User',
    status_code=204,
)
async def ban_user_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    provider_viewer_id: Annotated[str, Body(embed=True)],
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChannelProviderScope.CHAT_MODERATION]),
    ],
    ban_duration: Annotated[int | None, Body(embed=True)] = None,
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    channel_provider = await get_channel_provider_by_id(
        channel_provider_id=channel_provider_id,
    )
    if not channel_provider or channel_provider.channel_id != channel_id:
        raise HTTPException(status_code=404, detail='Channel provider not found')

    results = await fire_event_ban_user(
        data=EventBanUser(
            channel_provider=channel_provider,
            provider_viewer_id=provider_viewer_id,
            ban_duration=ban_duration,
        )
    )
    if not all(results):
        raise HTTPException(
            status_code=400,
            detail=f'Failed to {"timeout" if ban_duration else "ban"} user',
        )


@router.delete(
    '/channels/{channel_id}/providers/{channel_provider_id}/user-ban',
    name='Unban User',
    status_code=204,
)
async def unban_user_route(
    channel_id: UUID,
    channel_provider_id: UUID,
    provider_viewer_id: Annotated[str, Body(embed=True)],
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChannelProviderScope.CHAT_MODERATION]),
    ],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    channel_provider = await get_channel_provider_by_id(
        channel_provider_id=channel_provider_id,
    )
    if not channel_provider or channel_provider.channel_id != channel_id:
        raise HTTPException(status_code=404, detail='Channel provider not found')

    results = await fire_event_unban_user(
        data=EventUnbanUser(
            channel_provider=channel_provider,
            provider_viewer_id=provider_viewer_id,
        )
    )
    if not all(results):
        raise HTTPException(status_code=400, detail='Failed to unban user')
