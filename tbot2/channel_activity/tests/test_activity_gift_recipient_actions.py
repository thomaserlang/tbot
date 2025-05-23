import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_activity import (
    ActivityCreate,
    add_gift_recipient,
    create_activity,
    get_activity,
    start_collect_gift_recipients,
)
from tbot2.common import MentionPartRequest
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_activity_gift_recipient_actions(db: None) -> None:
    channel = await create_channel(
        data=ChannelCreate(
            display_name='Test Channel',
        )
    )
    activity_request = ActivityCreate(
        channel_id=channel.id,
        type='community_sub_gift',
        sub_type='1000',
        provider='twitch',
        provider_message_id='123',
        provider_user_id='123',
        provider_viewer_id='123',
        viewer_name='testuser',
        viewer_display_name='Test User',
        count=2,
        count_decimal_place=0,
        system_message='testuser gifted subs subs',
    )
    await create_activity(data=activity_request)
    await start_collect_gift_recipients(
        activity_id=activity_request.id,
        gift_id='some-id',
        total=2,
    )

    await add_gift_recipient(
        gift_id='some-id',
        recipient=MentionPartRequest(
            user_id='a1',
            display_name='Test User 1',
            username='testuser1',
        ),
    )
    await add_gift_recipient(
        gift_id='some-id',
        recipient=MentionPartRequest(
            user_id='a2',
            display_name='Test User 2',
            username='testuser2',
        ),
    )

    activity = await get_activity(activity_id=activity_request.id)
    assert activity
    assert activity.gifted_viewers
    assert len(activity.gifted_viewers) == 2
    assert activity.gifted_viewers[0].user_id == 'a1'
    assert activity.gifted_viewers[1].user_id == 'a2'


if __name__ == '__main__':
    run_file(__file__)
