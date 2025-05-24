from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from tbot2.channel_activity import delete_activity, get_activity

from ..schemas.event_channel_points_custom_reward_redemption_schema import (
    EventChannelPointsCustomRewardRedemptionUpdate,
)
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.channel_points_custom_reward_redemption.update',
    include_in_schema=False,
    status_code=204,
)
async def event_channel_points_custom_reward_redemption_add_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[
        EventChannelPointsCustomRewardRedemptionUpdate
    ].model_validate_json(await request.body())

    if data.event.status == 'canceled':
        activity = await get_activity(provider_message_id=data.event.id)
        if activity:
            await delete_activity(activity_id=activity.id)
