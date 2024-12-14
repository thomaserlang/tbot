from datetime import datetime, timezone

import pytest
from pytest_mock import MockFixture
from twitchAPI.twitch import ChannelFollower, TwitchUser
from uuid6 import uuid7

from tbot2.command import Command, MessageVar
from tbot2.common import ChatMessage
from tbot2.testbase import run_file
from tbot2.twitch.command_var_fillers import followage


@pytest.mark.asyncio
async def test_followage(mocker: MockFixture):
    twitch_channel_follower = mocker.patch(
        'tbot2.twitch.command_var_fillers.followage.twitch_channel_follower'
    )
    twitch_channel_follower.return_value = ChannelFollower(
        from_id='1234',
        from_name='test',
        to_id='1234',
        to_name='test',
        followed_at='2017-05-24T22:22:08Z',
    )

    vars = {
        'followage': MessageVar(name='followage', match_raw='followage', args=[]),
        'followage_date': MessageVar(
            name='followage_date', match_raw='followage_date', args=[]
        ),
        'followage_datetime': MessageVar(
            name='followage_datetime', match_raw='followage_datetime', args=[]
        ),
    }

    mock_datetime = mocker.patch(
        'tbot2.twitch.command_var_fillers.followage.datetime_now'
    )
    mock_datetime.return_value = datetime(2024, 5, 24, 22, 22, 8, tzinfo=timezone.utc)

    await followage(
        chat_message=ChatMessage(  # type: ignore
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            provider='twitch',
            provider_id='1234',
            channel_id=uuid7(),
            chatter_id='1234',
            chatter_name='test',
            chatter_display_name='Test',
            message='!followage',
            msg_id='123',
        ),
        command=Command(args=[], name='followage'),
        vars=vars,
    )

    assert vars['followage'].value == '7 years and 2 days ago'
    assert vars['followage_date'].value == 'May 24 2017'
    assert vars['followage_datetime'].value == '2017-05-24 22:22:08 UTC'

    # Followage of another user
    twitch_lookup_users = mocker.patch(
        'tbot2.twitch.command_var_fillers.followage.twitch_lookup_users'
    )
    twitch_lookup_users.return_value = [
        TwitchUser(
            id='1234',
            login='testuser',
            display_name='testuser',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at='2017-05-24T22:22:08Z',
        )
    ]

    await followage.followage(
        chat_message=ChatMessage(  # type: ignore
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            provider='twitch',
            provider_id='1234',
            channel_id=uuid7(),
            chatter_id='1234',
            chatter_name='test',
            chatter_display_name='Test',
            message='!followage testuser',
            msg_id='123',
        ),
        command=Command(args=['testuser'], name='followage'),
        vars=vars,
    )
    assert vars['followage'].value == '7 years and 2 days ago'
    assert twitch_lookup_users.called
    assert twitch_lookup_users.call_args.kwargs['logins'] == ['testuser']


if __name__ == '__main__':
    run_file(__file__)
