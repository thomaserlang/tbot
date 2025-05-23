from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from tbot2.channel_activity import (
    ActivityCreate,
    create_activity,
)
from tbot2.twitch.schemas.event_channel_follow_schema import EventChannelFollow

from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.follow',
    include_in_schema=False,
    status_code=204,
)
async def event_channel_follow_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelFollow].model_validate_json(
        await request.body()
    )

    await create_activity(
        data=ActivityCreate(
            type='follow',
            provider='twitch',
            provider_message_id=headers.message_id,
            provider_user_id=data.event.broadcaster_user_id,
            provider_viewer_id=data.event.user_id,
            viewer_name=data.event.user_login,
            viewer_display_name=data.event.user_name,
            channel_id=channel_id,
            created_at=data.event.followed_at,
        )
    )
