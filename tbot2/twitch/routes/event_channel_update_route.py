from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from tbot2.channel_provider import ChannelProviderRequest, save_channel_provider

from ..schemas.event_channel_update_schema import EventChannelUpdate
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.update',
    status_code=204,
)
async def event_channel_update_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelUpdate].model_validate_json(
        await request.body()
    )
    await save_channel_provider(
        channel_id=channel_id,
        provider='twitch',
        data=ChannelProviderRequest(
            provider_user_display_name=data.event.broadcaster_user_name,
            provider_user_name=data.event.broadcaster_user_name,
            stream_title=data.event.title,
        ),
    )
