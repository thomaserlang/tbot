from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path
from fastapi.responses import RedirectResponse

from tbot2.common import (
    ErrorMessage,
    ImageSizeType,
)
from tbot2.twitch.actions.twitch_badges_action import get_twitch_cached_badges

router = APIRouter()


@router.get(
    '/channels/{channel_id}/twitch/badge-image/{provider_channel_id}/{size}/{id}',
    name='Get Twitch Badge Image',
    status_code=301,
)
async def get_twitch_badge_image_route(
    channel_id: UUID,
    provider_channel_id: str,
    id: Annotated[str, Path(description='Format: {set_id}-{id}')],
    size: ImageSizeType,
) -> RedirectResponse:
    data = await get_twitch_cached_badges(provider_channel_id)
    if id not in data:
        raise ErrorMessage(
            message='Badge not found', code=404, type='twitch_badge_not_found'
        )
    return RedirectResponse(
        url=data[id].image_url_1x
        if size == 'sm'
        else data[id].image_url_2x
        if size == 'md'
        else data[id].image_url_4x,
        status_code=301,
    )
