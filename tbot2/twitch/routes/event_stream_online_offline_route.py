from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from tbot2.channel_stream import (
    create_channel_provider_stream,
    end_channel_provider_stream,
)

from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..schemas.event_stream_online_offline_schema import (
    EventStreamOffline,
    EventStreamOnline,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/stream.online',
    status_code=204,
)
async def event_stream_online_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventStreamOnline].model_validate_json(
        await request.body()
    )
    if data.event.type != 'live':
        return

    await create_channel_provider_stream(
        channel_id=channel_id,
        provider='twitch',
        provider_id=data.event.broadcaster_user_id,
        provider_stream_id=data.event.id,
        started_at=data.event.started_at,
        stream_id=data.event.broadcaster_user_name,
    )


@router.post(
    '/stream.offline',
    status_code=204,
)
async def event_stream_offline_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    channel_id: UUID,
    request: Request,
) -> None:
    data = EventSubNotification[EventStreamOffline].model_validate_json(
        await request.body()
    )
    await end_channel_provider_stream(
        channel_id=channel_id,
        provider='twitch',
        provider_id=data.event.broadcaster_user_id,
    )
