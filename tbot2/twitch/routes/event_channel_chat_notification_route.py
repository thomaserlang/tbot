from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Security
from uuid6 import uuid7

from tbot2.channel_chatlog import create_chatlog, publish_chatlog
from tbot2.common import (
    ChatMessage,
    ChatMessagePartRequest,
    ChatMessageRequest,
    TAccessLevel,
    TokenData,
)
from tbot2.dependecies import authenticated
from tbot2.message_parse import message_to_parts
from tbot2.twitch.actions.twitch_message_utils import (
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

    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        return

    if (
        data.event.notice_type == 'sub_gift'
        and data.event.sub_gift
        and data.event.sub_gift.community_gift_id
    ):
        # Figure out how to handle multiple sub_gift events without spamming the chat
        # Save it somehow to the event so it's possible to see
        # which users got gifted
        return

    notice_message = data.event.system_message
    if not notice_message:
        if data.event.notice_type == 'announcement':
            notice_message = 'Announcement'

    await create_chatlog(
        data=ChatMessageRequest(
            type='notice',
            sub_type=data.event.notice_type,
            channel_id=channel_id,
            provider_viewer_id=data.event.chatter_user_id,
            viewer_name=data.event.chatter_user_login,
            viewer_display_name=data.event.chatter_user_name,
            viewer_color=data.event.color,
            created_at=headers.message_timestamp,
            notice_message=notice_message,
            msg_id=headers.message_id,
            provider='twitch',
            provider_id=data.event.broadcaster_user_id,
            message=data.event.message.text,
            badges=twitch_badges_to_badges(data.event.badges),
            parts=await message_to_parts(
                parts=twitch_fragments_to_parts(data.event.message.fragments),
                provider='twitch',
                provider_user_id=data.event.broadcaster_user_id,
            )
            if data.event.message.text
            else [],
        )
    )


@router.post(
    '/emulate-subscription',
    name='Emulate subscription',
    status_code=204,
)
async def emulate_automatic_reward_redemption_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    notice_message = "TestUser subscribed at Tier 1. They've subscribed for 41 months!"

    chat_message = ChatMessageRequest(
        type='notice',
        sub_type='sub',
        channel_id=channel_id,
        provider_viewer_id='123',
        viewer_name='test_user',
        viewer_display_name='TestUser',
        notice_message=notice_message,
        notice_parts=[
            ChatMessagePartRequest(
                type='text',
                text=notice_message,
            ),
        ],
        message='Wohoo!!',
        msg_id=str(uuid7()),
        provider='twitch',
        provider_id='123',
    )
    await publish_chatlog(
        channel_id=channel_id, data=ChatMessage.model_validate(chat_message)
    )
