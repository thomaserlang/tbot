from datetime import datetime, timezone

import pytest
from pytest_mock import MockFixture

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_command import TCommand, fill_message
from tbot2.channel_points import inc_points
from tbot2.common import ChatMessage, TProvider
from tbot2.testbase import run_file
from tbot2.twitch import TwitchUser
from tbot2.twitch import cmd_var_fillers as cmd_var_fillers


@pytest.mark.asyncio
async def test_points_vars(db: None, mocker: MockFixture):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    lookup_twitch_users = mocker.patch(
        'tbot2.twitch.cmd_var_fillers.points_vars.lookup_twitch_user'
    )
    lookup_twitch_users.return_value = [
        TwitchUser(
            id='test_chatter',
            login='test_chatter',
            display_name='Test Chatter',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at='2017-05-24T22:22:08Z',
        ),
    ]

    await inc_points(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter',
        points=100,
    )

    await inc_points(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter2',
        points=200,
    )

    await inc_points(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter3',
        points=300,
    )

    message = await fill_message(
        response_message='Points: {points} rank {points_rank}',
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!points',
            msg_id='123',
        ),
        command=TCommand(args=[], name='points'),
    )

    assert message == 'Points: 100 rank 3'


if __name__ == '__main__':
    run_file(__file__)
