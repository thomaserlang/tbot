from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Request, Security
from uuid6 import uuid7

from tbot2.channel_chat_message import create_chat_message, publish_chat_message
from tbot2.common import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessagePartRequest,
    GiftPartRequest,
    TAccessLevel,
    TokenData,
)
from tbot2.dependecies import authenticated

from ..schemas.event_channel_points_automatic_reward_redemption_schema import (
    EventChannelPointsAutomaticRewardRedemption,
    RewardType,
)
from ..schemas.event_headers_schema import EventSubHeaders
from ..schemas.event_notification_schema import (
    EventSubNotification,
)
from ..twitch_event_dependencies import validate_twitch_webhook_signature

router = APIRouter()


@router.post(
    '/channel.channel_points_automatic_reward_redemption.add',
    include_in_schema=False,
    status_code=204,
)
async def event_channel_points_automatic_reward_redemption_add_route(
    headers: Annotated[EventSubHeaders, Depends(validate_twitch_webhook_signature)],
    request: Request,
    channel_id: UUID,
) -> None:
    data = EventSubNotification[
        EventChannelPointsAutomaticRewardRedemption
    ].model_validate_json(await request.body())

    # Only one we are interested in here
    if data.event.reward.type != 'celebration':
        return

    title = 'Celebration'

    notice_message = (
        f'Redeemed {title}'
        if data.event.user_input
        else (f'{data.event.user_name} redeemed {title}')
    )

    chat_message = ChatMessageCreate(
        type='notice',
        sub_type='automatic_reward_redemption',
        channel_id=channel_id,
        provider_viewer_id=data.event.user_id,
        viewer_name=data.event.user_login,
        viewer_display_name=data.event.user_name,
        created_at=data.event.redeemed_at,
        message=data.event.user_input or '',
        notice_message=f'{notice_message} ♢ {data.event.reward.cost}',
        notice_message_parts=[
            ChatMessagePartRequest(
                type='text',
                text=f'{notice_message} ',
            ),
            ChatMessagePartRequest(
                type='text',
                text=f'Cheer{data.event.reward.cost}',
                gift=GiftPartRequest(
                    id='1',
                    name='Bits',
                    type='cheermote',
                    count=data.event.reward.cost,
                ),
            ),
        ],
        provider_message_id=data.event.id,
        provider='twitch',
        provider_channel_id=data.event.broadcaster_user_id,
    )
    await create_chat_message(data=chat_message)


@router.post(
    '/emulate-automatic-reward-redemption',
    name='Emulate Automatic Reward Redemption',
    status_code=204,
)
async def emulate_automatic_reward_redemption_route(
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
    reward_type: Annotated[RewardType, Body(embed=True)],
    user_input: Annotated[str, Body(embed=True)] = '',
    reward_cost: Annotated[int, Body(embed=True)] = 100,
) -> None:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    notice_message = (
        f'Redeemed {reward_type}' if user_input else f'TestUser redeemed {reward_type}'
    )

    chat_message = ChatMessageCreate(
        type='notice',
        sub_type='automatic_reward_redemption',
        channel_id=channel_id,
        provider_viewer_id='123',
        viewer_name='test_user',
        viewer_display_name='TestUser',
        notice_message=f'{notice_message} ♢ {reward_cost}',
        notice_message_parts=[
            ChatMessagePartRequest(
                type='text',
                text=f'{notice_message} ',
            ),
            ChatMessagePartRequest(
                type='gift',
                text=f'cheer{reward_cost}',
                gift=GiftPartRequest(
                    id='cheer-100',
                    name='cheer',
                    type='cheermote',
                    count=reward_cost,
                ),
            ),
        ],
        message=user_input,
        provider_message_id=str(uuid7()),
        provider='twitch',
        provider_channel_id='123',
    )
    await publish_chat_message(
        channel_id=channel_id, event=ChatMessage.model_validate(chat_message)
    )
