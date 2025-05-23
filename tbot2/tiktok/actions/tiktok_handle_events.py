import asyncio

from TikTokLive import TikTokLiveClient  # type: ignore
from TikTokLive.events import (  # type: ignore
    CommentEvent,
    GiftEvent,
)

from tbot2.channel_activity import ActivityCreate, create_activity
from tbot2.channel_chatlog import create_chatlog
from tbot2.channel_provider import (
    ChannelProvider,
)
from tbot2.common import (
    ChatMessagePartRequest,
    ChatMessageRequest,
    GiftPartRequest,
)
from tbot2.message_parse import message_to_parts


async def handle_comment_event(
    client: TikTokLiveClient, channel_provider: ChannelProvider, event: CommentEvent
) -> None:
    await create_chatlog(
        data=ChatMessageRequest(
            type='message',
            channel_id=channel_provider.channel_id,
            provider='tiktok',
            provider_id=client.unique_id,
            provider_viewer_id=event.user.unique_id,
            viewer_display_name=event.user.nickname,
            viewer_name=event.user.unique_id,
            message=event.comment,
            parts=await message_to_parts(
                message=event.comment,
                provider='tiktok',
                provider_user_id=channel_provider.provider_user_id or '',
            ),
            msg_id=str(event.base_message.message_id),
        )
    )


async def handle_gift_event(
    client: TikTokLiveClient, channel_provider: ChannelProvider, event: GiftEvent
) -> None:
    await asyncio.gather(
        handle_gift_chat_message(client, channel_provider, event),
        handle_gift_activity(client, channel_provider, event),
    )


async def handle_gift_chat_message(
    client: TikTokLiveClient, channel_provider: ChannelProvider, event: GiftEvent
) -> None:
    if event.gift.streakable and event.streaking:  # type: ignore
        return  # wait til streak ends
    diamonds = event.gift.diamond_count * event.repeat_count
    name = 'diamonds' if diamonds > 1 else 'diamond'
    message = (
        f'{event.user.nickname} sent {event.gift.name} '
        f'x{event.repeat_count} ({diamonds} {name})'
    )
    parts: list[ChatMessagePartRequest] = [
        ChatMessagePartRequest(
            type='text',
            text=f'{event.user.nickname} sent ',
        ),
        ChatMessagePartRequest(
            type='gift',
            text=event.gift.name,
            gift=GiftPartRequest(
                id=str(event.gift.id),
                type='gift',
                name=event.gift.name,
                count=event.gift.diamond_count,
            ),
        ),
        ChatMessagePartRequest(
            type='text',
            text=f' x{event.repeat_count} ({diamonds} {name})',
        ),
    ]
    await create_chatlog(
        data=ChatMessageRequest(
            type='notice',
            sub_type='gift',
            channel_id=channel_provider.channel_id,
            provider='tiktok',
            provider_id=channel_provider.provider_user_id or '',
            provider_viewer_id=event.user.unique_id,
            viewer_display_name=event.user.nickname,
            viewer_name=event.user.unique_id,
            message=message,
            parts=parts,
            msg_id=str(event.base_message.message_id),
        )
    )


async def handle_gift_activity(
    client: TikTokLiveClient, channel_provider: ChannelProvider, event: GiftEvent
) -> None:
    if event.gift.streakable and event.streaking:  # type: ignore
        return  # wait til streak ends

    await create_activity(
        data=ActivityCreate(
            channel_id=channel_provider.channel_id,
            type='gift',
            sub_type=event.gift.name,
            count=event.gift.diamond_count * event.repeat_count,
            provider='tiktok',
            provider_message_id=str(event.base_message.message_id),
            provider_user_id=channel_provider.provider_user_id or '',
            provider_viewer_id=event.user.unique_id,
            viewer_display_name=event.user.nickname,
            viewer_name=event.user.unique_id,
        )
    )
