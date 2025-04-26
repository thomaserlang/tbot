from datetime import UTC, datetime

import pytest
from pytest_mock import MockFixture
from twitchAPI.twitch import ChannelFollower, TwitchUser
from uuid6 import uuid7

from tbot2.channel_command import MessageVar, TCommand
from tbot2.channel_command.var_fillers.followage_vars import followage_vars
from tbot2.common import ChatMessage
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_followage_vars(mocker: MockFixture) -> None:
    twitch_channel_follower = mocker.patch(
        'tbot2.channel_command.var_fillers.followage_vars.twitch_channel_follower'
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
        'tbot2.channel_command.var_fillers.followage_vars.datetime_now'
    )
    mock_datetime.return_value = datetime(2024, 5, 24, 22, 15, 8, tzinfo=UTC)

    await followage_vars(
        chat_message=ChatMessage(  # type: ignore
            id=uuid7(),
            type='message',
            created_at=datetime.now(tz=UTC),
            provider='twitch',
            provider_id='1234',
            channel_id=uuid7(),
            provider_viewer_id='1234',
            viewer_name='test',
            viewer_display_name='Test',
            message='!followage',
            msg_id='123',
        ),
        command=TCommand(args=[], name='followage'),
        vars=vars,
    )

    assert vars['followage'].value == '7 years and 2 days'
    assert vars['followage_date'].value == 'May 24 2017'
    assert vars['followage_datetime'].value == '2017-05-24 22:22:08 UTC'

    # Followage of another user
    lookup_twitch_users = mocker.patch(
        'tbot2.channel_command.var_fillers.followage_vars.lookup_twitch_users'
    )
    lookup_twitch_users.return_value = [
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

    await followage_vars(
        chat_message=ChatMessage(  # type: ignore
            id=uuid7(),
            type='message',
            created_at=datetime.now(tz=UTC),
            provider='twitch',
            provider_id='1234',
            channel_id=uuid7(),
            provider_viewer_id='1234',
            viewer_name='test',
            viewer_display_name='Test',
            message='!followage testuser',
            msg_id='123',
        ),
        command=TCommand(args=['testuser'], name='followage'),
        vars=vars,
    )
    assert vars['followage'].value == '7 years and 2 days'
    assert lookup_twitch_users.called
    assert lookup_twitch_users.call_args.kwargs['logins'] == ['testuser']


if __name__ == '__main__':
    run_file(__file__)
