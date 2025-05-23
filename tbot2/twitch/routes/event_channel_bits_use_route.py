from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Request, Security

from tbot2.channel_activity import (
    Activity,
    ActivityCreate,
    create_activity,
)
from tbot2.channel_activity.actions.activity_actions import publish_activity
from tbot2.common import TAccessLevel, TokenData
from tbot2.common.schemas.pub_sub_event import PubSubEvent
from tbot2.dependecies import authenticated
from tbot2.message_parse import message_to_parts

from ..actions.twitch_message_utils import twitch_fragments_to_parts
from ..schemas.event_channel_bits_use_schema import EventChannelBitsUse
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.bits.use',
    include_in_schema=False,
    status_code=204,
)
async def event_channel_bits_use_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelBitsUse].model_validate_json(
        await request.body()
    )

    await create_activity(
        data=ActivityCreate(
            type='bits',
            sub_type=data.event.type,
            count=data.event.bits,
            provider='twitch',
            provider_message_id=headers.message_id,
            provider_user_id=data.event.broadcaster_user_id,
            provider_viewer_id=data.event.user_id,
            viewer_name=data.event.user_login,
            viewer_display_name=data.event.user_name,
            channel_id=channel_id,
            created_at=headers.message_timestamp,
            message=data.event.message.text if data.event.message else None,
            message_parts=await message_to_parts(
                parts=twitch_fragments_to_parts(data.event.message.fragments),
                provider='twitch',
                provider_user_id=data.event.broadcaster_user_id,
            )
            if data.event.message
            else None,
        )
    )


@router.post(
    '/emulate-cheer',
    name='Emulate cheer',
    status_code=204,
)
async def emulate_cheer_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
    bits: Annotated[int, Body(embed=True)] = 1500,
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    activity = ActivityCreate(
        channel_id=channel_id,
        type='bits',
        provider='twitch',
        provider_message_id='123',
        provider_user_id='123',
        provider_viewer_id='123',
        viewer_name='testuser',
        viewer_display_name='Test User',
        count=bits,
    )
    await publish_activity(
        channel_id=channel_id,
        event=PubSubEvent[Activity](
            type='activity',
            action='new',
            data=Activity.model_validate(activity),
        ),
    )
