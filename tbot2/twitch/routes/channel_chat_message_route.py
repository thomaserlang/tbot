import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response

from tbot2.channel_command import handle_message
from tbot2.chatlog.actions.chatlog_action import create_chatlog
from tbot2.common import TProvider
from tbot2.common.schemas.chat_message_schema import ChatMessage
from tbot2.database import database

from ..actions.twitch_send_message_actions import twitch_send_message
from ..schemas.eventsub_channel_chat_message_schema import (
    EventChannelChatMessage,
)
from ..schemas.eventsub_headers import EventSubHeaders
from ..schemas.eventsub_notification_schema import (
    EventSubNotification,
)
from .dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/twitch/eventsub/channel.chat.message',
    status_code=204,
)
async def channel_chat_message_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
):
    if headers.message_type == 'webhook_callback_verification':
        return Response(status_code=200, content=(await request.json())['challenge'])

    if headers.message_type != 'notification':
        return

    data = EventSubNotification[EventChannelChatMessage].model_validate_json(
        await request.body()
    )

    # Don't handle messages from shared channels
    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        return

    data = ChatMessage(
        type='message',
        channel_id=channel_id,
        chatter_id=data.event.chatter_user_id,
        chatter_name=data.event.chatter_user_login,
        chatter_display_name=data.event.chatter_user_name,
        chatter_color=data.event.color,
        created_at=headers.message_timestamp,
        message=data.event.message.text,
        msg_id=data.event.message_id,
        provider=TProvider.twitch,
        provider_id=data.event.broadcaster_user_id,
        twitch_fragments=data.event.message.fragments,
        twitch_badges=data.event.badges,
    )

    try:
        response = await handle_message(
            chat_message=data,
        )
        if response:
            await twitch_send_message(
                broadcaster_id=data.provider_id,
                sender_id=data.provider_id,
                message=response.response,
                reply_parent_message_id=data.msg_id,
            )

    except Exception as e:
        logging.error(f'Failed to handle message: {e}')

    await create_chatlog(data=data)

    await database.redis.publish(  # type: ignore
        f'tbot:live_chat:{data.channel_id}', data.model_dump_json()
    )
