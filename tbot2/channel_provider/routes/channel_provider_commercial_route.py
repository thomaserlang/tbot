from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Security

from tbot2.channel_provider import (
    ChannelProviderScope,
    get_channel_provider_by_id,
)
from tbot2.common import ErrorMessage, TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..event_types import fire_event_run_commercial

router = APIRouter()


@router.post(
    '/channels/{channel_id}/providers/{channel_provider_id}/run-commercial',
    status_code=204,
    name='Start Commercial',
)
async def start_commercial(
    channel_id: UUID,
    channel_provider_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelProviderScope.WRITE])
    ],
    length: Annotated[
        int,
        Body(
            embed=True, gt=0, le=1800, description='Length of the commercial in seconds'
        ),
    ] = 180,
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )
    channel_provider = await get_channel_provider_by_id(
        channel_provider_id=channel_provider_id,
    )
    if not channel_provider or channel_provider.channel_id != channel_id:
        raise ErrorMessage(
            code=404,
            message='Channel provider not found',
            type='channel_provider_not_found',
        )
    r = await fire_event_run_commercial(
        channel_provider=channel_provider,
        length=length,
    )
    if not r:
        raise ErrorMessage(
            code=400,
            message='Not supported on this provider',
            type='run_commercial_not_supported',
        )
