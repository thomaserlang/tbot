import asyncio

from loguru import logger
from uuid6 import uuid7

from tbot2.channel_activity import (
    ActivityCreate,
    ActivityId,
    add_gift_recipient,
    create_activity,
    start_collect_gift_recipients,
)
from tbot2.channel_activity.schemas.activity_schemas import ISO4217
from tbot2.channel_chat_filters import matches_filter
from tbot2.channel_chat_message import create_chat_message
from tbot2.channel_command import TCommand, handle_message_response
from tbot2.channel_command.fill_message import fill_message
from tbot2.channel_provider import ChannelProvider
from tbot2.common import (
    ChatMessageCreate,
    MentionPartRequest,
    TAccessLevel,
    datetime_now,
)
from tbot2.database import conn
from tbot2.message_parse import message_to_parts

from ..actions.youtube_live_chat_ban_actions import live_chat_ban
from ..actions.youtube_live_chat_message_actions import (
    delete_live_chat_message,
    send_live_chat_message,
)
from ..schemas.youtube_live_chat_message_schema import LiveChatMessage


async def handle_message(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    if (datetime_now() - live_message.snippet.published_at).total_seconds() > 30:
        return
    asyncio.create_task(
        conn.elasticsearch.index(
            index='youtube_live_chat_message_events',
            document={
                'channel_id': channel_provider.channel_id,
                'channel_provider_id': channel_provider.id,
                **live_message.model_dump(mode='json'),
            },
        )
    )
    match live_message.snippet.type:
        case 'superChatEvent':
            logger.debug(
                f'New super chat message: {live_message.snippet.display_message}'
            )

        case 'messageDeletedEvent':
            await handle_type_message_deleted_event(
                channel_provider=channel_provider,
                live_message=live_message,
            )

        case 'userBannedEvent':
            await handle_type_user_banned_event(
                channel_provider=channel_provider,
                live_message=live_message,
            )

        case 'textMessageEvent':
            await handle_text_message_event(
                channel_provider=channel_provider, message=live_message
            )

        case (
            'newSponsorEvent'
            | 'memberMilestoneChatEvent'
            | 'superChatEvent'
            | 'superStickerEvent'
            | 'membershipGiftingEvent'
            | 'giftMembershipReceivedEvent'
        ):
            await handle_notice(
                channel_provider=channel_provider, live_message=live_message
            )

        case 'sponsorOnlyModeEndedEvent' | 'sponsorOnlyModeStartedEvent':
            await handle_sponsor_only_mode(
                channel_provider=channel_provider, live_message=live_message
            )

        case 'pollDetails':
            await handle_poll_details(
                channel_provider=channel_provider, live_message=live_message
            )

        case _:
            logger.debug(f'Unhandled type: {live_message.snippet.type}')


async def handle_text_message_event(
    channel_provider: ChannelProvider,
    message: LiveChatMessage,
) -> None:
    if not message.snippet.text_message_details:
        raise Exception('Missing text_message_details')
    chat_message = ChatMessageCreate(
        type='message',
        channel_id=channel_provider.channel_id,
        provider_viewer_id=message.author_details.channel_id,
        viewer_name=message.author_details.display_name,
        viewer_display_name=message.author_details.display_name,
        created_at=message.snippet.published_at,
        message=message.snippet.text_message_details.message_text,
        message_parts=await message_to_parts(
            message=message.snippet.text_message_details.message_text,
            provider='youtube',
            provider_channel_id=channel_provider.provider_channel_id or '',
        ),
        provider_message_id=message.id,
        provider='youtube',
        provider_channel_id=channel_provider.provider_channel_id or '',
        access_level=access_level_from_live_chat_message(message),
    )

    try:
        if response := await handle_message_response(
            chat_message=chat_message,
        ):
            await send_live_chat_message(
                channel_id=channel_provider.channel_id,
                live_chat_id=message.snippet.live_chat_id,
                message=response.response,
            )
    except Exception as e:
        logger.exception(e)

    await asyncio.gather(
        handle_filter_message(
            channel_provider=channel_provider,
            chat_message=chat_message,
            live_chat_id=message.snippet.live_chat_id,
        ),
        create_chat_message(data=chat_message),
    )


def access_level_from_live_chat_message(
    live_chat_message: LiveChatMessage,
) -> TAccessLevel:
    if live_chat_message.author_details.is_chat_moderator:
        return TAccessLevel.MOD
    if live_chat_message.author_details.is_chat_owner:
        return TAccessLevel.OWNER
    if live_chat_message.author_details.is_chat_sponsor:
        return TAccessLevel.SUB
    return TAccessLevel.PUBLIC


async def handle_filter_message(
    channel_provider: ChannelProvider,
    chat_message: ChatMessageCreate,
    live_chat_id: str,
) -> None:
    try:
        match = await matches_filter(chat_message=chat_message)
        if not match:
            return
        if match.action == 'warning':
            await delete_live_chat_message(
                channel_id=channel_provider.channel_id,
                message_id=chat_message.provider_message_id,
            )
            if match.filter.warning_message:
                message = await fill_message(
                    response_message=match.filter.warning_message,
                    chat_message=chat_message,
                    command=TCommand(name='warning', args=[]),
                )
                message = f'@{chat_message.viewer_name}, {message}'
                await send_live_chat_message(
                    channel_id=channel_provider.channel_id,
                    live_chat_id=live_chat_id,
                    message=message,
                )

        elif match.action == 'timeout':
            await live_chat_ban(
                channel_id=channel_provider.channel_id,
                live_chat_id=live_chat_id,
                type='temporary',
                ban_duration_seconds=match.filter.timeout_duration,
                banned_youtube_user_channel_id=chat_message.provider_viewer_id,
            )
    except Exception as e:
        logger.exception(e)


async def handle_type_message_deleted_event(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    details = live_message.snippet.message_deleted_details
    if not details:
        raise Exception('Missing message_deleted_details')
    chat_message = ChatMessageCreate(
        type='status',
        sub_type='delete_message',
        channel_id=channel_provider.channel_id,
        provider='youtube',
        provider_channel_id=channel_provider.provider_channel_id or '',
        provider_viewer_id=live_message.author_details.channel_id,
        viewer_name=live_message.author_details.display_name,
        viewer_display_name=live_message.author_details.display_name,
        viewer_color='',
        created_at=live_message.snippet.published_at,
        notice_message=f'{live_message.author_details.display_name} deleted message '
        f'"{details.deleted_message_id}"',
        provider_message_id=live_message.id,
    )
    await create_chat_message(data=chat_message)


async def handle_type_user_banned_event(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    details = live_message.snippet.user_banned_details
    if not details:
        raise Exception('Missing user_banned_details')
    msg = ''
    sub_type = ''
    if details.ban_type == 'temporary':
        msg = (
            f'{live_message.author_details.display_name} timed out '
            f'{details.banned_user_details.display_name} for '
            f'{details.ban_duration_seconds} seconds'
        )
        sub_type = 'timeout'

    if details.ban_type == 'permanent':
        msg = (
            f'{live_message.author_details.display_name} banned '
            f'{details.banned_user_details.display_name}'
        )
        sub_type = 'ban'

    if not sub_type:
        logger.error(f'Unknown ban type: {details.ban_type} ')
        return

    chat_message = ChatMessageCreate(
        type='status',
        sub_type=sub_type,
        channel_id=channel_provider.channel_id,
        provider='youtube',
        provider_channel_id=channel_provider.provider_channel_id or '',
        provider_viewer_id=details.banned_user_details.channel_id,
        viewer_name=details.banned_user_details.display_name,
        viewer_display_name=details.banned_user_details.display_name,
        created_at=live_message.snippet.published_at,
        notice_message=msg,
        provider_message_id=live_message.id,
    )
    await create_chat_message(data=chat_message)


async def handle_notice(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    await asyncio.gather(
        handle_notice_chat_message(
            channel_provider=channel_provider,
            live_message=live_message,
        ),
        handle_notice_activity(
            channel_provider=channel_provider,
            live_message=live_message,
        ),
    )


async def handle_notice_chat_message(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    chat_message = ChatMessageCreate(
        type='notice',
        sub_type=live_message.snippet.type,
        channel_id=channel_provider.channel_id,
        provider='youtube',
        provider_channel_id=channel_provider.provider_channel_id or '',
        provider_viewer_id=live_message.author_details.channel_id,
        viewer_name=live_message.author_details.display_name,
        viewer_display_name=live_message.author_details.display_name,
        created_at=live_message.snippet.published_at,
        notice_message=live_message.snippet.display_message,
        provider_message_id=live_message.id,
    )
    await create_chat_message(data=chat_message)


async def handle_notice_activity(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    activity_id = ActivityId(uuid7())
    sub_type = ''
    count = 0
    count_decimal_places = 0
    count_currency: ISO4217 | None = None
    gifted_viewers: list[MentionPartRequest] | None = None
    message = ''

    snippet = live_message.snippet
    if snippet.new_sponsor_details:
        sub_type = snippet.new_sponsor_details.member_level_name

    elif snippet.super_chat_details:
        sub_type = str(snippet.super_chat_details.tier)
        count = snippet.super_chat_details.amount_micros
        count_currency = ISO4217(snippet.super_chat_details.currency)
        count_decimal_places = 6
        message = snippet.super_chat_details.user_comment

    elif snippet.super_sticker_details:
        sub_type = str(snippet.super_sticker_details.tier)
        count = snippet.super_sticker_details.amount_micros
        count_currency = ISO4217(snippet.super_sticker_details.currency)
        count_decimal_places = 6

    elif snippet.member_milestone_chat_details:
        sub_type = snippet.member_milestone_chat_details.member_level_name
        count = snippet.member_milestone_chat_details.member_month
        message = snippet.member_milestone_chat_details.user_comment

    elif snippet.membership_gifting_details:
        sub_type = snippet.membership_gifting_details.gift_memberships_level_name
        count = snippet.membership_gifting_details.gift_memberships_count
        await start_collect_gift_recipients(
            activity_id=activity_id,
            gift_id=live_message.id,
            total=snippet.membership_gifting_details.gift_memberships_count,
        )

    elif snippet.gift_membership_received_details:
        await add_gift_recipient(
            gift_id=snippet.gift_membership_received_details.associated_membership_gifting_message_id,
            recipient=MentionPartRequest(
                user_id=live_message.author_details.channel_id,
                username=live_message.author_details.display_name,
                display_name=live_message.author_details.display_name,
            ),
        )
        return
    else:
        return

    await create_activity(
        data=ActivityCreate(
            id=activity_id,
            channel_id=channel_provider.channel_id,
            type=live_message.snippet.type,
            sub_type=sub_type,
            count=count,
            count_decimal_place=count_decimal_places,
            count_currency=count_currency,
            provider='youtube',
            provider_channel_id=channel_provider.provider_channel_id or '',
            provider_message_id=live_message.id,
            provider_viewer_id=live_message.author_details.channel_id,
            viewer_name=live_message.author_details.display_name,
            viewer_display_name=live_message.author_details.display_name,
            created_at=live_message.snippet.published_at,
            gifted_viewers=gifted_viewers,
            system_message=live_message.snippet.display_message,
            message=message,
        )
    )


async def handle_sponsor_only_mode(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    await create_chat_message(
        data=ChatMessageCreate(
            type='notice',
            sub_type=live_message.snippet.type,
            channel_id=channel_provider.channel_id,
            provider='youtube',
            provider_channel_id=channel_provider.provider_channel_id or '',
            provider_viewer_id=live_message.author_details.channel_id,
            viewer_name=live_message.author_details.display_name,
            viewer_display_name=live_message.author_details.display_name,
            created_at=live_message.snippet.published_at,
            notice_message=live_message.snippet.display_message,
            provider_message_id=live_message.id,
        )
    )


async def handle_poll_details(
    channel_provider: ChannelProvider,
    live_message: LiveChatMessage,
) -> None:
    chat_message = ChatMessageCreate(
        type='status',
        sub_type='poll',
        channel_id=channel_provider.channel_id,
        provider='youtube',
        provider_channel_id=channel_provider.provider_channel_id or '',
        provider_viewer_id=live_message.author_details.channel_id,
        viewer_name=live_message.author_details.display_name,
        viewer_display_name=live_message.author_details.display_name,
        created_at=live_message.snippet.published_at,
        notice_message=live_message.snippet.display_message,
        provider_message_id=live_message.id,
    )
    await create_chat_message(data=chat_message)
