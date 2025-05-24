from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path
from fastapi.responses import RedirectResponse

from tbot2.common import (
    ErrorMessage,
    ImageSizeType,
)

router = APIRouter()


@router.get(
    '/channels/{channel_id}/twitch/gift-image/{provider_channel_id}/{size}/{id}',
    name='Get Twitch Cheermote Image',
)
async def get_twitch_gift_image_route(
    channel_id: UUID,
    provider_channel_id: str,
    id: Annotated[str, Path(description='Format: {prefix}-{tier}')],
    size: ImageSizeType,
) -> RedirectResponse:
    # If we want to support the channel custom cheermotes later,
    # check the twitch_cheermote_action.py
    prefix, tier = id.lower().split('-')
    url = f'https://d3aqoihi2n8ty8.cloudfront.net/actions/{prefix}/dark/animated/{tier}'
    match size:
        case 'sm':
            return RedirectResponse(url=url + '/1.gif')
        case 'md':
            return RedirectResponse(url=url + '/2.gif')
        case 'lg':
            return RedirectResponse(url=url + '/4.gif')
        case _:
            raise ErrorMessage(
                message='Invalid size', code=400, type='twitch_badge_not_found'
            )
