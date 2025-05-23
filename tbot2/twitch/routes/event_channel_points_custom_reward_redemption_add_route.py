import asyncio
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Request, Security
from uuid6 import uuid7

from tbot2.channel_activity import ActivityCreate, create_activity
from tbot2.channel_chat_message import create_chat_message, publish_chat_message
from tbot2.common import (
    ChatMessage,
    ChatMessageCreate,
    PubSubEvent,
    TAccessLevel,
    TokenData,
)
from tbot2.dependecies import authenticated

from ..schemas.event_channel_points_custom_reward_redemption_schema import (
    EventChannelPointsCustomRewardRedemption,
)
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.channel_points_custom_reward_redemption.add',
    include_in_schema=False,
    status_code=204,
)
async def event_channel_points_custom_reward_redemption_add_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[
        EventChannelPointsCustomRewardRedemption
    ].model_validate_json(await request.body())

    await asyncio.gather(
        handle_chat_message(channel_id=channel_id, data=data),
        handle_activity(channel_id=channel_id, data=data),
    )


async def handle_chat_message(
    channel_id: UUID,
    data: EventSubNotification[EventChannelPointsCustomRewardRedemption],
) -> None:
    if data.event.user_input:
        # if it has user input it also gets sent to the channel.chat.message endpoint
        # so we don't need to handle it here. There we get user badges, fragments etc.
        return

    notice_message = (
        f'{data.event.user_name} redeemed {data.event.reward.title} '
        f'• {data.event.reward.cost}'
    )

    await create_chat_message(
        data=ChatMessageCreate(
            type='notice',
            sub_type='custom_reward_redemption',
            channel_id=channel_id,
            provider_viewer_id=data.event.user_id,
            viewer_name=data.event.user_login,
            viewer_display_name=data.event.user_name,
            created_at=data.event.redeemed_at,
            notice_message=notice_message,
            provider_message_id=data.event.id,
            provider='twitch',
            provider_channel_id=data.event.broadcaster_user_id,
        )
    )


async def handle_activity(
    channel_id: UUID,
    data: EventSubNotification[EventChannelPointsCustomRewardRedemption],
) -> None:
    await create_activity(
        data=ActivityCreate(
            type='points',
            sub_type=data.event.reward.title,
            count=data.event.reward.cost,
            provider='twitch',
            provider_message_id=data.event.id,
            provider_channel_id=data.event.broadcaster_user_id,
            provider_viewer_id=data.event.user_id,
            viewer_name=data.event.user_login,
            viewer_display_name=data.event.user_name,
            channel_id=channel_id,
            created_at=data.event.redeemed_at,
            message=data.event.user_input,
        )
    )


@router.post(
    '/emulate-custom-reward-redemption',
    name='Emulate Custom Reward Redemption',
    status_code=204,
)
async def emulate_custom_reward_redemption_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
    reward_title: Annotated[str, Body(embed=True)] = 'Test Reward',
    user_input: Annotated[str, Body(embed=True)] = '',
    reward_cost: Annotated[int, Body(embed=True)] = 100,
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    notice_message = (
        f'Redeemed {reward_title} • {reward_cost}'
        if user_input
        else f'TestUser redeemed {reward_title}'
    )

    chat_message = ChatMessageCreate(
        type='notice',
        sub_type='custom_reward_redemption',
        channel_id=channel_id,
        provider_viewer_id='123',
        viewer_name='test_user',
        viewer_display_name='TestUser',
        notice_message=notice_message,
        message=user_input,
        provider_message_id=str(uuid7()),
        provider='twitch',
        provider_channel_id='123',
    )
    await publish_chat_message(
        channel_id=channel_id,
        event=PubSubEvent[ChatMessage](
            type='chat_message',
            action='new',
            data=ChatMessage.model_validate(chat_message),
        ),
    )
