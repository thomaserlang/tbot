from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from tbot2.channel_stats import (
    create_channel_provider_stream,
    end_channel_provider_stream,
)
from tbot2.common import TProvider

from ..schemas.eventsub_headers import EventSubHeaders
from ..schemas.eventsub_notification_schema import (
    EventSubNotification,
)
from ..schemas.eventsub_stream_online_offline_schema import EventStreamOnline
from .dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/twitch/eventsub/stream.online',
    status_code=204,
)
async def stream_online_event_route(
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
        provider=TProvider.twitch,
        provider_stream_id=data.event.id,
        started_at=data.event.started_at,
    )


@router.post(
    '/twitch/eventsub/stream.offline',
    status_code=204,
)
async def stream_offline_event_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    channel_id: UUID,
) -> None:
    await end_channel_provider_stream(
        channel_id=channel_id,
        provider=TProvider.twitch,
    )
