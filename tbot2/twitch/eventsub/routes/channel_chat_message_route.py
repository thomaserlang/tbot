from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from tbot2.channel.actions.lookup_twitch_id_to_channel_id_action import (
    lookup_twitch_id_to_channel_id,
)
from tbot2.chatlog.actions.chatlog_action import create_chatlog
from tbot2.common.schemas.chat_message_schema import ChatMessage
from tbot2.database import database

from ..dependencies import validate_twitch_webhook_signature
from ..schemas.eventsub_channel_chat_message_schema import (
    ChannelChatMessage,
)
from ..schemas.eventsub_headers import EventSubHeaders
from ..schemas.eventsub_notification_schema import (
    EventSubNotification,
)

router = APIRouter()


@router.post('/channel.chat.message')
async def eventsub_message(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
):
    if headers.message_type == 'webhook_callback_verification':
        return Response(content=(await request.json())['challenge'])
    if headers.message_type != 'notification':
        return

    data = EventSubNotification[ChannelChatMessage].model_validate_json(
        await request.body()
    )

    user_id = await lookup_twitch_id_to_channel_id(
        twitch_id=data.event.broadcaster_user_id
    )
    if not user_id:
        raise HTTPException(400, 'Twitch channel not conneccted to any user')

    data = ChatMessage(
        type='message',
        channel_id=user_id,
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
    await create_chatlog(data=data)

    await database.redis.publish(  # type: ignore
        f'tbot:live_chat:{data.channel_id}', data.model_dump_json()
    )

    return Response(status_code=204)
