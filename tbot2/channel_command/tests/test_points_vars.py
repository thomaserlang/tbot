from datetime import UTC, datetime

import pytest
from pytest_mock import MockFixture
from uuid6 import uuid7

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_command import TCommand
from tbot2.channel_command.fill_message import fill_message
from tbot2.channel_points import inc_points
from tbot2.common import ChatMessageCreate
from tbot2.testbase import run_file
from tbot2.twitch import TwitchUser


@pytest.mark.asyncio
async def test_points_vars(db: None, mocker: MockFixture) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    lookup_twitch_users = mocker.patch(
        'tbot2.channel_command.var_fillers.points_vars.lookup_twitch_user'
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
            created_at=datetime(2017, 5, 24, 22, 22, 8, tzinfo=UTC),
        ),
    ]

    await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='test_chatter',
        points=100,
    )

    await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='test_chatter2',
        points=200,
    )

    await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='test_chatter3',
        points=300,
    )

    message = await fill_message(
        response_message='Points: {points} rank {points_rank}',
        chat_message=ChatMessageCreate(
            id=uuid7(),
            type='message',
            created_at=datetime.now(tz=UTC),
            provider='twitch',
            provider_channel_id='1234',
            channel_id=channel.id,
            provider_viewer_id='test_chatter',
            viewer_name='test',
            viewer_display_name='Test',
            message='!points',
            provider_message_id='123',
        ),
        command=TCommand(args=[], name='points'),
    )

    assert message == 'Points: 100 rank 3'


if __name__ == '__main__':
    run_file(__file__)
