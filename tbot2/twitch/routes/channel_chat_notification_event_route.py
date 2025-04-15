import asyncio
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from uuid6 import uuid7

from tbot2.chatlog import create_chatlog
from tbot2.common import ChatMessage
from tbot2.database import database

from ..schemas.eventsub_channel_chat_notification_schema import (
    EventChannelChatNotification,
)
from ..schemas.eventsub_headers import EventSubHeaders
from ..schemas.eventsub_notification_schema import (
    EventSubNotification,
)
from .dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.chat.notification',
    status_code=204,
)
async def channel_chat_notification_event_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelChatNotification].model_validate_json(
        await request.body()
    )

    # Don't handle messages from shared channels
    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        return

    messages: list[ChatMessage] = [
        ChatMessage(
            id=uuid7(),
            type='notice',
            sub_type=data.event.notice_type,
            channel_id=channel_id,
            chatter_id=data.event.chatter_user_id,
            chatter_name=data.event.chatter_user_login,
            chatter_display_name=data.event.chatter_user_name,
            chatter_color=data.event.color,
            created_at=headers.message_timestamp,
            message=data.event.system_message,
            msg_id=str(uuid7()),
            provider='twitch',
            provider_id=data.event.broadcaster_user_id,
        )
    ]

    if data.event.message.text:
        messages.append(
            ChatMessage(
                id=uuid7(),
                type='message',
                channel_id=channel_id,
                chatter_id=data.event.chatter_user_id,
                chatter_name=data.event.chatter_user_login,
                chatter_display_name=data.event.chatter_user_name,
                chatter_color=data.event.color,
                created_at=headers.message_timestamp,
                message=data.event.message.text,
                msg_id=data.event.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
                twitch_fragments=data.event.message.fragments,
                twitch_badges=data.event.badges,
            )
        )

    for message in messages:
        await asyncio.gather(
            create_chatlog(data=message),
            database.redis.publish(  # type: ignore
                f'tbot:live_chat:{message.channel_id}',
                message.model_dump_json(),
            ),
        )
