from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Request, Security
from uuid6 import uuid7

from tbot2.channel_chatlog import create_chatlog, publish_chatlog
from tbot2.common import (
    ChatMessage,
    ChatMessageRequest,
    TAccessLevel,
    TokenData,
    datetime_now,
)
from tbot2.dependecies import authenticated

from ..schemas.event_channel_points_custom_reward_redemption_add_schema import (
    EventChannelPointsCustomRewardRedemptionAdd,
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
        EventChannelPointsCustomRewardRedemptionAdd
    ].model_validate_json(await request.body())

    notice_message = (
        f'Redeemed {data.event.reward.title} • {data.event.reward.cost}'
        if data.event.reward.prompt
        else (
            f'{data.event.user_name} redeemed {data.event.reward.title} '
            f'• {data.event.reward.cost}'
        )
    )

    chat_message = ChatMessageRequest(
        type='notice',
        sub_type='custom_reward_redemption',
        channel_id=channel_id,
        provider_viewer_id=data.event.user_id,
        viewer_name=data.event.user_login,
        viewer_display_name=data.event.user_name,
        created_at=data.event.redeemed_at,
        message=data.event.reward.prompt,
        notice_message=notice_message,
        msg_id=data.event.id,
        provider='twitch',
        provider_id=data.event.broadcaster_user_id,
    )
    await create_chatlog(data=chat_message)


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

    chat_message = ChatMessageRequest(
        type='notice',
        sub_type='custom_reward_redemption',
        channel_id=channel_id,
        provider_viewer_id='123',
        viewer_name='test_user',
        viewer_display_name='TestUser',
        created_at=datetime_now(),
        notice_message=notice_message,
        message=user_input,
        msg_id=str(uuid7()),
        provider='twitch',
        provider_id='123',
    )
    await publish_chatlog(
        channel_id=channel_id, data=ChatMessage.model_validate(chat_message)
    )
