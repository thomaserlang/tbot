from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from uuid6 import uuid7

from tbot2.channel_chatlog import create_chatlog
from tbot2.common import ChatMessageRequest
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

    messages: list[ChatMessageRequest] = [
        ChatMessageRequest(
            id=uuid7(),
            type='notice',
            sub_type=data.event.notice_type,
            channel_id=channel_id,
            provider_viewer_id=data.event.chatter_user_id,
            viewer_name=data.event.chatter_user_login,
            viewer_display_name=data.event.chatter_user_name,
            viewer_color=data.event.color,
            created_at=headers.message_timestamp,
            message=data.event.system_message,
            msg_id=headers.message_id,
            provider='twitch',
            provider_id=data.event.broadcaster_user_id,
        )
    ]

    if data.event.message.text:
        messages.append(
            ChatMessageRequest(
                id=uuid7(),
                type='message',
                channel_id=channel_id,
                provider_viewer_id=data.event.chatter_user_id,
                viewer_name=data.event.chatter_user_login,
                viewer_display_name=data.event.chatter_user_name,
                viewer_color=data.event.color,
                created_at=headers.message_timestamp,
                message=data.event.message.text,
                msg_id=data.event.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
                badges=twitch_badges_to_badges(data.event.badges),
                parts=await message_to_parts(
                    parts=twitch_fragments_to_parts(data.event.message.fragments),
                    provider='twitch',
                    provider_user_id=data.event.broadcaster_user_id,
                ),
            )
        )

    for message in messages:
        await create_chatlog(data=message)
