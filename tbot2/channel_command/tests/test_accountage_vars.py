from datetime import UTC, datetime

import pytest
from pytest_mock import MockFixture
from uuid6 import uuid7

from tbot2.channel_command import MessageVar, TCommand
from tbot2.channel_command.var_fillers.accountage_vars import accountage_vars
from tbot2.common import ChatMessageCreate, datetime_now
from tbot2.testbase import run_file
from tbot2.twitch import TwitchUser


@pytest.mark.asyncio
async def test_accountage_vars(mocker: MockFixture) -> None:
    lookup_twitch_users = mocker.patch(
        'tbot2.channel_command.var_fillers.accountage_vars.lookup_twitch_users'
    )
    lookup_twitch_users.return_value = [
        TwitchUser(
            id='1234',
            login='test',
            display_name='Test',
            type='',
            broadcaster_type='',
            description='',
            profile_image_url='',
            offline_image_url='',
            view_count=0,
            created_at=datetime(2017, 5, 24, 22, 22, 8, tzinfo=UTC),
        )
    ]

    vars = {
        'accountage': MessageVar(name='accountage', match_raw='accountage', args=[]),
        'accountage_date': MessageVar(
            name='accountage_date', match_raw='accountage_date', args=[]
        ),
        'accountage_datetime': MessageVar(
            name='accountage_datetime', match_raw='accountage_datetime', args=[]
        ),
    }

    mock_datetime = mocker.patch(
        'tbot2.channel_command.var_fillers.accountage_vars.datetime_now'
    )
    mock_datetime.return_value = datetime(2024, 5, 24, 22, 22, 8, tzinfo=UTC)

    channel_id = uuid7()

    await accountage_vars(
        chat_message=ChatMessageCreate(  # type: ignore
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            provider='twitch',
            provider_channel_id='1234',
            channel_id=channel_id,
            provider_viewer_id='1234',
            viewer_name='test',
            viewer_display_name='Test',
            message='!accountage',
            provider_message_id='123',
        ),
        command=TCommand(args=[], name='accountage'),
        vars=vars,
    )

    assert vars['accountage'].value == '7 years and 2 days ago'
    assert vars['accountage_date'].value == 'May 24 2017'
    assert vars['accountage_datetime'].value == '2017-05-24 22:22:08 UTC'

    # Accountage of another user
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
            created_at=datetime(2017, 5, 24, 22, 22, 8, tzinfo=UTC),
        )
    ]

    await accountage_vars(
        chat_message=ChatMessageCreate(  # type: ignore
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            provider='twitch',
            provider_channel_id='1234',
            channel_id=channel_id,
            provider_viewer_id='1234',
            viewer_name='test',
            viewer_display_name='Test',
            message='!accountage testuser',
            provider_message_id='123',
        ),
        command=TCommand(args=['testuser'], name='accountage'),
        vars=vars,
    )

    assert vars['accountage'].value == '7 years and 2 days ago'
    assert vars['accountage_date'].value == 'May 24 2017'
    assert vars['accountage_datetime'].value == '2017-05-24 22:22:08 UTC'
    assert lookup_twitch_users.await_count == 2
    lookup_twitch_users.assert_has_calls(
        calls=[
            mocker.call(channel_id=channel_id, logins=[], user_ids=['1234']),
            mocker.call(channel_id=channel_id, logins=['testuser'], user_ids=[]),
        ],  # type: ignore
    )


if __name__ == '__main__':
    run_file(__file__)
