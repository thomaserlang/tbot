import asyncio
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Security
from loguru import logger
from uuid6 import uuid7

from tbot2.channel_activity import (
    Activity,
    ActivityCreate,
    ActivityId,
    add_gift_recipient,
    create_activity,
    start_collect_gift_recipients,
)
from tbot2.channel_activity.actions.activity_actions import publish_activity
from tbot2.channel_activity.schemas.activity_schemas import ISO4217
from tbot2.channel_chat_message import create_chat_message, publish_chat_message
from tbot2.common import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessagePartRequest,
    MentionPartRequest,
    PubSubEvent,
    TAccessLevel,
    TokenData,
)
from tbot2.dependecies import authenticated
from tbot2.message_parse import message_to_parts

from ..actions.twitch_message_utils import (
    twitch_badges_to_badges,
    twitch_fragments_to_parts,
)
from ..schemas.event_channel_chat_notification_schema import (
    EventChannelChatNotification,
)
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.chat.notification',
    include_in_schema=False,
    status_code=204,
)
async def event_channel_chat_notification_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelChatNotification].model_validate_json(
        await request.body()
    )

    await asyncio.gather(
        handle_chat_message(data, headers, channel_id),
        handle_activity(data, headers, channel_id),
    )


async def handle_chat_message(
    data: EventSubNotification[EventChannelChatNotification],
    headers: EventSubHeaders,
    channel_id: UUID,
) -> None:
    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        # Ignore notifications from other channels for now
        return

    notice_message = data.event.system_message
    if not notice_message:
        if data.event.notice_type == 'announcement':
            notice_message = 'Announcement'

    message_parts = (
        await message_to_parts(
            parts=twitch_fragments_to_parts(data.event.message.fragments),
            provider='twitch',
            provider_channel_id=data.event.broadcaster_user_id,
        )
        if data.event.message.text
        else []
    )

    await create_chat_message(
        data=ChatMessageCreate(
            type='notice',
            sub_type=data.event.notice_type,
            channel_id=channel_id,
            provider_viewer_id=data.event.chatter_user_id,
            viewer_name=data.event.chatter_user_login,
            viewer_display_name=data.event.chatter_user_name,
            viewer_color=data.event.color,
            created_at=headers.message_timestamp,
            notice_message=notice_message,
            provider_message_id=data.event.message_id,
            provider='twitch',
            provider_channel_id=data.event.broadcaster_user_id,
            message=data.event.message.text,
            badges=twitch_badges_to_badges(data.event.badges),
            message_parts=message_parts,
        )
    )


async def handle_activity(
    data: EventSubNotification[EventChannelChatNotification],
    headers: EventSubHeaders,
    channel_id: UUID,
) -> None:
    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        # Ignore notifications from other channels
        return

    activity_id = ActivityId(uuid7())
    sub_type = ''
    count = 0
    count_decimal_places = 0
    count_currency: ISO4217 | None = None
    gifted_viewers: list[MentionPartRequest] | None = None

    if data.event.sub:
        sub_type = data.event.sub.sub_tier
        count = data.event.sub.duration_months

    elif data.event.resub:
        sub_type = data.event.resub.sub_tier
        count = data.event.resub.cumulative_months

    elif data.event.community_sub_gift:
        sub_type = data.event.community_sub_gift.sub_tier
        count = data.event.community_sub_gift.total
        await start_collect_gift_recipients(
            activity_id=activity_id,
            gift_id=data.event.community_sub_gift.id,
            total=data.event.community_sub_gift.total,
        )

    elif data.event.sub_gift:
        if data.event.sub_gift.community_gift_id:
            await add_gift_recipient(
                gift_id=data.event.sub_gift.community_gift_id,
                recipient=MentionPartRequest(
                    user_id=data.event.sub_gift.recipient_user_id,
                    username=data.event.sub_gift.recipient_user_login,
                    display_name=data.event.sub_gift.recipient_user_name,
                ),
            )
            return
        sub_type = data.event.sub_gift.sub_tier
        count = data.event.sub_gift.duration_months
        gifted_viewers = [
            MentionPartRequest(
                user_id=data.event.sub_gift.recipient_user_id,
                username=data.event.sub_gift.recipient_user_login,
                display_name=data.event.sub_gift.recipient_user_name,
            )
        ]

    elif data.event.raid:
        count = data.event.raid.viewer_count

    elif data.event.charity_donation:
        count = data.event.charity_donation.amount.value
        count_decimal_places = data.event.charity_donation.amount.decimal_places
        count_currency = ISO4217(data.event.charity_donation.amount.currency)
    else:
        logger.debug(f'Unhandled event type: {data.event.notice_type}')
        return

    await create_activity(
        data=ActivityCreate(
            id=activity_id,
            type=data.event.notice_type,
            sub_type=sub_type,
            count=count,
            count_decimal_place=count_decimal_places,
            count_currency=count_currency,
            provider='twitch',
            provider_message_id=data.event.message_id,
            provider_channel_id=data.event.broadcaster_user_id,
            provider_viewer_id=data.event.chatter_user_id,
            viewer_name=data.event.chatter_user_login,
            viewer_display_name=data.event.chatter_user_name,
            channel_id=channel_id,
            created_at=headers.message_timestamp,
            gifted_viewers=gifted_viewers,
            system_message=data.event.system_message,
        )
    )


@router.post(
    '/emulate-subscription',
    name='Emulate subscription',
    status_code=204,
)
async def emulate_subscription_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    notice_message = "TestUser subscribed at Tier 1. They've subscribed for 41 months!"

    chat_message = ChatMessageCreate(
        type='notice',
        sub_type='sub',
        channel_id=channel_id,
        provider_viewer_id='123',
        viewer_name='test_user',
        viewer_display_name='TestUser',
        notice_message=notice_message,
        notice_message_parts=[
            ChatMessagePartRequest(
                type='text',
                text=notice_message,
            ),
        ],
        message='Wohoo!!',
        provider_message_id=str(uuid7()),
        provider='twitch',
        provider_channel_id='123',
    )
    await publish_chat_message(
        channel_id=channel_id,
        event=PubSubEvent[ChatMessage](
            type='activity',
            action='new',
            data=ChatMessage.model_validate(chat_message),
        ),
    )

    activity = ActivityCreate(
        channel_id=channel_id,
        type='sub',
        sub_type='1000',
        provider='twitch',
        provider_message_id='123',
        provider_channel_id='123',
        provider_viewer_id='123',
        viewer_name='testuser',
        viewer_display_name='Test User',
        count=2,
        count_decimal_place=0,
        system_message=notice_message,
    )
    await publish_activity(
        channel_id=channel_id,
        event=PubSubEvent[Activity](
            type='activity',
            action='new',
            data=Activity.model_validate(activity),
        ),
    )
