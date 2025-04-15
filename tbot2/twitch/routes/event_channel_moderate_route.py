import asyncio
from typing import Annotated
from uuid import UUID

import humanize.time
from fastapi import APIRouter, Depends, Request
from uuid6 import uuid7

from tbot2.chatlog import create_chatlog
from tbot2.common import ChatMessage, datetime_now
from tbot2.database import database

from ..schemas.event_channel_moderate_schema import EventChannelModerate
from ..schemas.event_headers import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from .dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.moderate',
    status_code=204,
)
async def event_channel_chat_message_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[EventChannelModerate].model_validate_json(
        await request.body()
    )

    # Don't handle messages from shared channels
    if (
        data.event.source_broadcaster_user_id
        and data.event.source_broadcaster_user_id != data.event.broadcaster_user_id
    ):
        return

    chat_message: ChatMessage | None = None

    match data.event.action:
        case 'ban':
            if data.event.ban:
                chat_message = ChatMessage(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='ban',
                    channel_id=channel_id,
                    chatter_id=data.event.ban.user_id,
                    chatter_name=data.event.ban.user_login,
                    chatter_display_name=data.event.ban.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} banned '
                        f'{data.event.ban.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'unban':
            if data.event.unban:
                chat_message = ChatMessage(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='unban',
                    channel_id=channel_id,
                    chatter_id=data.event.unban.user_id,
                    chatter_name=data.event.unban.user_login,
                    chatter_display_name=data.event.unban.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} unbanned '
                        f'{data.event.unban.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'timeout':
            if data.event.timeout:
                until = humanize.time.precisedelta(
                    datetime_now() - data.event.timeout.expires_at, format='%0.0f'
                )
                chat_message = ChatMessage(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='timeout',
                    channel_id=channel_id,
                    chatter_id=data.event.timeout.user_id,
                    chatter_name=data.event.timeout.user_login,
                    chatter_display_name=data.event.timeout.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} timed out '
                        f'{data.event.timeout.user_name} for {until}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'untimeout':
            if data.event.untimeout:
                chat_message = ChatMessage(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='untimeout',
                    channel_id=channel_id,
                    chatter_id=data.event.untimeout.user_id,
                    chatter_name=data.event.untimeout.user_login,
                    chatter_display_name=data.event.untimeout.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} removed time out on '
                        f'{data.event.untimeout.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'warn':
            if data.event.warn:
                chat_message = ChatMessage(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='warn',
                    channel_id=channel_id,
                    chatter_id=data.event.warn.user_id,
                    chatter_name=data.event.warn.user_login,
                    chatter_display_name=data.event.warn.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} warned '
                        f'{data.event.warn.user_name}: "{data.event.warn.reason}"'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'clear':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='clear',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=f'{data.event.moderator_user_name} cleared chat',
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'emoteonly':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='emoteonly',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=f'{data.event.moderator_user_name} activated emoteonly mode',
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'emoteonlyoff':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='emoteonlyoff',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated emoteonly mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'followers':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='followers',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(f'{data.event.moderator_user_name} activated followers mode'),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'followersoff':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='followersoff',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated followers mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'uniquechat':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='uniquechat',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} activated unique chat mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'uniquechatoff':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='uniquechatoff',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated unique chat mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'slow':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='slow',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(f'{data.event.moderator_user_name} activated slow mode'),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'slowoff':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='slowoff',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(f'{data.event.moderator_user_name} deactivated slow mode'),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'subscribers':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='subscribers',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} activated subscribers mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'subscribersoff':
            chat_message = ChatMessage(
                id=uuid7(),
                type='mod_action',
                sub_type='subscribersoff',
                channel_id=channel_id,
                chatter_id=data.event.moderator_user_id,
                chatter_name=data.event.moderator_user_login,
                chatter_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated subscribers mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case _:
            pass

    if chat_message:
        await asyncio.gather(
            create_chatlog(data=chat_message),
            database.redis.publish(  # type: ignore
                f'tbot:live_chat:{chat_message.channel_id}',
                chat_message.model_dump_json(),
            ),
        )
