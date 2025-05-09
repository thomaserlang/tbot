from typing import Annotated
from uuid import UUID

import humanize.time
from fastapi import APIRouter, Depends, Request
from uuid6 import uuid7

from tbot2.channel_chatlog import create_chatlog
from tbot2.common import ChatMessageRequest, datetime_now

from ..schemas.event_channel_moderate_schema import EventChannelModerate
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

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

    chat_message: ChatMessageRequest | None = None

    match data.event.action:
        case 'mod':
            if data.event.mod:
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='mod',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.mod.user_id,
                    viewer_name=data.event.mod.user_login,
                    viewer_display_name=data.event.mod.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} modded '
                        f'{data.event.mod.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'unmod':
            if data.event.unmod:
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='unmod',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.unmod.user_id,
                    viewer_name=data.event.unmod.user_login,
                    viewer_display_name=data.event.unmod.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} unmodded '
                        f'{data.event.unmod.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'vip':
            if data.event.vip:
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='vip',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.vip.user_id,
                    viewer_name=data.event.vip.user_login,
                    viewer_display_name=data.event.vip.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} vipped '
                        f'{data.event.vip.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'unvip':
            if data.event.unvip:
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='unmod',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.unvip.user_id,
                    viewer_name=data.event.unvip.user_login,
                    viewer_display_name=data.event.unvip.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} unvipped '
                        f'{data.event.unvip.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'ban':
            if data.event.ban:
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='ban',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.ban.user_id,
                    viewer_name=data.event.ban.user_login,
                    viewer_display_name=data.event.ban.user_name,
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
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='unban',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.unban.user_id,
                    viewer_name=data.event.unban.user_login,
                    viewer_display_name=data.event.unban.user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} unbanned '
                        f'{data.event.unban.user_name}'
                    ),
                    msg_id=headers.message_id,
                    provider='twitch',
                    provider_id=data.event.broadcaster_user_id,
                )
        case 'delete':
            if data.event.delete:
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='delete',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.moderator_user_id,
                    viewer_name=data.event.moderator_user_login,
                    viewer_display_name=data.event.moderator_user_name,
                    created_at=headers.message_timestamp,
                    message=(
                        f'{data.event.moderator_user_name} deleted message: '
                        f'{data.event.delete.message_body}'
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
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='timeout',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.timeout.user_id,
                    viewer_name=data.event.timeout.user_login,
                    viewer_display_name=data.event.timeout.user_name,
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
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='untimeout',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.untimeout.user_id,
                    viewer_name=data.event.untimeout.user_login,
                    viewer_display_name=data.event.untimeout.user_name,
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
                chat_message = ChatMessageRequest(
                    id=uuid7(),
                    type='mod_action',
                    sub_type='warn',
                    channel_id=channel_id,
                    provider_viewer_id=data.event.warn.user_id,
                    viewer_name=data.event.warn.user_login,
                    viewer_display_name=data.event.warn.user_name,
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
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='clear',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=f'{data.event.moderator_user_name} cleared chat',
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'emoteonly':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='emoteonly',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=f'{data.event.moderator_user_name} activated emoteonly mode',
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'emoteonlyoff':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='emoteonlyoff',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated emoteonly mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'followers':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='followers',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(f'{data.event.moderator_user_name} activated followers mode'),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'followersoff':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='followersoff',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated followers mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'uniquechat':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='uniquechat',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} activated unique chat mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'uniquechatoff':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='uniquechatoff',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} deactivated unique chat mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'slow':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='slow',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(f'{data.event.moderator_user_name} activated slow mode'),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'slowoff':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='slowoff',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(f'{data.event.moderator_user_name} deactivated slow mode'),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'subscribers':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='subscribers',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
                created_at=headers.message_timestamp,
                message=(
                    f'{data.event.moderator_user_name} activated subscribers mode'
                ),
                msg_id=headers.message_id,
                provider='twitch',
                provider_id=data.event.broadcaster_user_id,
            )
        case 'subscribersoff':
            chat_message = ChatMessageRequest(
                id=uuid7(),
                type='mod_action',
                sub_type='subscribersoff',
                channel_id=channel_id,
                provider_viewer_id=data.event.moderator_user_id,
                viewer_name=data.event.moderator_user_login,
                viewer_display_name=data.event.moderator_user_name,
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
        await create_chatlog(data=chat_message)
