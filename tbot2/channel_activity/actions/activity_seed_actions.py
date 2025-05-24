import asyncio
from uuid import UUID

from uuid6 import uuid7

from tbot2.common import MentionPartRequest

from ..schemas.activity_schemas import ISO4217, ActivityCreate, ActivityId
from .activity_actions import create_activity


async def seed_activity(
    *, channel_id: UUID, num_activities: int = 15, wait_after_activity: float = 0.1
) -> None:
    if num_activities <= 0:
        return
    activities: list[ActivityCreate] = [
        ActivityCreate(
            channel_id=channel_id,
            type='sub',
            sub_type='1000',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='FrostyPixel42',
            viewer_display_name='FrostyPixel42',
            count=2,
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='sub',
            sub_type='3000',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='LunaWhisper',
            viewer_display_name='LunaWhisper',
            count=3,
            message='WOOOOP',
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='bits',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='EchoTigerX',
            viewer_display_name='EchoTigerX',
            count=1337,
            count_decimal_place=0,
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='resub',
            sub_type='1000',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='BlazeNova99',
            viewer_display_name='BlazeNova99',
            count=11,
            count_decimal_place=0,
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='gift_sub',
            sub_type='1000',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='ChillStorm7',
            viewer_display_name='ChillStorm7',
            count=1,
            count_decimal_place=0,
            gifted_viewers=[
                MentionPartRequest(
                    user_id='a1',
                    display_name='MidnightTaco',
                    username='MidnightTaco',
                )
            ],
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='community_sub_gift',
            sub_type='3000',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='QuantumFox',
            viewer_display_name='QuantumFox',
            count=10,
            count_decimal_place=0,
            gifted_viewers=[
                MentionPartRequest(
                    user_id=f'user_{i}',
                    display_name=f'TurboYeti{i}',
                    username=f'TurboYeti{i}',
                )
                for i in range(1, 11)
            ],
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='raid',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='NeonFalcon',
            viewer_display_name='NeonFalcon',
            count=1123,
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='charity_donation',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='CharityHero',
            viewer_display_name='CharityHero',
            count=1000,
            count_decimal_place=2,
            count_currency=ISO4217('USD'),
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='follow',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='CharityHero123',
            viewer_display_name='CharityHero123',
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='points',
            provider='twitch',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='LOOOL',
            viewer_display_name='LOOOL',
            count=100,
            message=(
                'Some long message that is not too long but not too short '
                'either and is just right for testing purposes and is not too '
                'long but not too short either and is just right for testing '
                'purposes and is not too long but not too short either and is just '
                'right for testing purposes'
            ),
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='newSponsorEvent',
            sub_type='Membership Tier 1',
            provider='youtube',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='CactusWizard',
            viewer_display_name='CactusWizard',
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='superChatEvent',
            provider='youtube',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='JellyBeanSamurai',
            viewer_display_name='JellyBeanSamurai',
            count=1000000,
            count_decimal_place=6,
            count_currency=ISO4217('USD'),
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='superStickerEvent',
            provider='youtube',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='CrypticMoose',
            viewer_display_name='CrypticMoose',
            count=2000000,
            count_decimal_place=6,
            count_currency=ISO4217('USD'),
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='membershipGiftingEvent',
            sub_type='Membership Tier 1',
            provider='youtube',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='SolarWaffle',
            viewer_display_name='SolarWaffle',
            count=10,
            gifted_viewers=[
                MentionPartRequest(
                    user_id=f'user_{i}',
                    display_name=f'VelvetRogue{i}',
                    username=f'VelvetRogue{i}',
                )
                for i in range(1, 11)
            ],
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='memberMilestoneChatEvent',
            sub_type='Membership Tier 1',
            provider='youtube',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='CactusWizard',
            viewer_display_name='CactusWizard',
            message='YOOO',
            count=12,
        ),
        ActivityCreate(
            channel_id=channel_id,
            type='gift',
            sub_type='Rocket',
            provider='tiktok',
            provider_message_id=str(uuid7()),
            provider_channel_id='123',
            provider_viewer_id='123',
            viewer_name='StaticPenguin',
            viewer_display_name='StaticPenguin',
            count=50,
        ),
    ]

    sent = 0
    for _ in range(1, 10):
        for activity in activities:
            if sent >= num_activities:
                return
            sent += 1
            activity.id = ActivityId(uuid7())
            activity.provider_message_id = str(uuid7())
            await create_activity(data=activity)
            if wait_after_activity:
                await asyncio.sleep(wait_after_activity)
