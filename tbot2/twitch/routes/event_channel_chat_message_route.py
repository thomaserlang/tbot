import asyncio
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from loguru import logger
from uuid6 import uuid7

from tbot2.channel_chat_filters import matches_filter
from tbot2.channel_chatlog import create_chatlog
from tbot2.channel_command import CommandError, TCommand, handle_message_response
from tbot2.channel_command.fill_message import fill_message
from tbot2.common import ChatMessage
from tbot2.twitch import twitch_warn_chat_user

from ..actions.twitch_ban_user_actions import twitch_ban_user
from ..actions.twitch_delete_message_actions import twitch_delete_message
from ..actions.twitch_send_message_actions import twitch_bot_send_message
from ..schemas.event_channel_chat_message_schema import (
    EventChannelChatMessage,
)
from ..schemas.event_headers import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from .dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.chat.message',
    status_code=204,
)
async def event_channel_chat_message_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelChatMessage].model_validate_json(
        await request.body()
    )

    # Don't handle messages from shared channels
    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        return

    chat_message = ChatMessage(
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
        twitch_fragments=data.event.message.fragments,
        twitch_badges=data.event.badges,
    )

    try:
        if response := await handle_message_response(
            chat_message=chat_message,
        ):
            await twitch_bot_send_message(
                channel_id=chat_message.channel_id,
                broadcaster_id=chat_message.provider_id,
                message=response.response,
                reply_parent_message_id=chat_message.msg_id,
                bot_provider=response.bot_provider,
            )
    except Exception as e:
        logger.exception(e)

    await asyncio.gather(
        handle_filter_message(chat_message=chat_message),
        create_chatlog(data=chat_message),
    )


async def handle_filter_message(
    chat_message: ChatMessage,
) -> None:
    try:
        match = await matches_filter(chat_message=chat_message)
        if not match:
            return
        if match.action == 'warning':
            await twitch_delete_message(
                channel_id=chat_message.channel_id,
                broadcaster_id=chat_message.provider_id,
                message_id=chat_message.msg_id,
            )
            if match.filter.warning_message:
                await twitch_warn_chat_user(
                    channel_id=chat_message.channel_id,
                    broadcaster_id=chat_message.provider_id,
                    twitch_user_id=chat_message.provider_viewer_id,
                    reason=await fill_message(
                        response_message=match.filter.warning_message,
                        chat_message=chat_message,
                        command=TCommand(name='warning', args=[]),
                    ),
                )

        elif match.action == 'timeout':
            timeout_message = ''
            try:
                timeout_message = await fill_message(
                    response_message=match.filter.timeout_message,
                    chat_message=chat_message,
                    command=TCommand(name='timeout', args=[]),
                )
            except CommandError as e:
                logger.warning(f'Timeout message failed: {e}')

            await twitch_ban_user(
                channel_id=chat_message.channel_id,
                broadcaster_id=chat_message.provider_id,
                twitch_user_id=chat_message.provider_viewer_id,
                duration=match.filter.timeout_duration,
                reason=timeout_message,
            )

    except Exception as e:
        logger.exception(e)
