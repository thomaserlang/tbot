from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from uuid6 import uuid7

from tbot2.channel_chatlog import create_chatlog
from tbot2.common import ChatMessage

from ..schemas.event_channel_subscription_gift_schema import (
    EventChannelSubscriptionGift,
)
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from .dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.subscription.gift',
    status_code=204,
)
async def event_channel_chat_subscription_gift_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelSubscriptionGift].model_validate_json(
        await request.body()
    )
    message = ChatMessage(
        id=uuid7(),
        type='notice',
        sub_type='community_sub_gift',
        channel_id=channel_id,
        provider_viewer_id=data.event.user_id,
        viewer_name=data.event.user_login,
        viewer_display_name=data.event.user_name,
        created_at=headers.message_timestamp,
        message=(
            f'{data.event.user_name} is gifting {data.event.total} '
            f'tier {data.event.tier[:1]} subs'
        ),
        msg_id=headers.message_id,
        provider='twitch',
        provider_id=data.event.broadcaster_user_id,
    )
    await create_chatlog(data=message)
