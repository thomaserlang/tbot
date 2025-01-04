from datetime import datetime, timezone

import pytest
from pytest_mock import MockFixture

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_points import inc_points
from tbot2.command import Command, fill_message
from tbot2.common import ChatMessage, TProvider
from tbot2.testbase import run_file
from tbot2.twitch import TwitchUser
from tbot2.twitch import cmd_var_fillers as cmd_var_fillers


@pytest.mark.asyncio
async def test_points_ranking_vars(db: None, mocker: MockFixture):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    lookup_twitch_users = mocker.patch(
        'tbot2.twitch.cmd_var_fillers.points_ranking_vars.lookup_twitch_users'
    )
    lookup_twitch_users.return_value = [
        TwitchUser(
            id='test_chatter5',
            login='test_chatter5',
            display_name='Test Chatter5',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at='2017-05-24T22:22:08Z',
        ),
        TwitchUser(
            id='test_chatter4',
            login='test_chatter4',
            display_name='Test Chatter4',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at='2017-05-24T22:22:08Z',
        ),
        TwitchUser(
            id='test_chatter3',
            login='test_chatter3',
            display_name='Test Chatter3',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at='2017-05-24T22:22:08Z',
        ),
        TwitchUser(
            id='test_chatter2',
            login='test_chatter2',
            display_name='Test Chatter2',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at='2017-05-24T22:22:08Z',
        ),
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

    await inc_points(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter4',
        points=400,
    )

    await inc_points(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter5',
        points=500,
    )

    message = await fill_message(
        response_message=('Points ranking: {points_ranking}'),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!points_ranking',
            msg_id='123',
        ),
        command=Command(args=[], name='points_ranking'),
    )

    assert message == (
        'Points ranking: 1. Test Chatter5 (500), 2. Test Chatter4 (400), 3. Test Chatter3 (300), '
        '4. Test Chatter2 (200), 5. Test Chatter (100)'
    )

if __name__ == '__main__':
    run_file(__file__)
