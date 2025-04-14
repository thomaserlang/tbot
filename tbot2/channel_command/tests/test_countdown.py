from datetime import UTC, datetime

import pytest
from pytest_mock import MockFixture
from uuid6 import uuid7

from tbot2.channel_command import TCommand
from tbot2.channel_command.fill_message import fill_message
from tbot2.common import ChatMessage
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_countdown(mocker: MockFixture) -> None:
    mock_datetime = mocker.patch(
        'tbot2.channel_command.var_fillers.countdown_vars.datetime_now'
    )
    mock_datetime.return_value = datetime(2024, 5, 24, 22, 22, 8, tzinfo=UTC)

    text = await fill_message(
        response_message='Countdown: {countdown "2024-05-20T20:00:00+02:00"} since',
        chat_message=ChatMessage(
            id=uuid7(),
            type='message',
            created_at=datetime.now(tz=UTC),
            message='!countdown',
            channel_id=uuid7(),
            chatter_id=str(uuid7()),
            chatter_name='test_user',
            chatter_display_name='Test User',
            provider='twitch',
            provider_id='123',
            msg_id='123',
        ),
        command=TCommand(name='countdown', args=[]),
    )
    assert text == 'Countdown: 4 days, 4 hours, 22 minutes and 8 seconds since'

    text = await fill_message(
        response_message='Countdown until: {countdown "2024-05-30T20:00:00+02:00"}',
        chat_message=ChatMessage(
            id=uuid7(),
            type='message',
            created_at=datetime.now(tz=UTC),
            message='!countdown',
            channel_id=uuid7(),
            chatter_id=str(uuid7()),
            chatter_name='test_user',
            chatter_display_name='Test User',
            provider='twitch',
            provider_id='123',
            msg_id='123',
        ),
        command=TCommand(name='countdown', args=[]),
    )
    assert text == 'Countdown until: 5 days, 19 hours, 37 minutes and 52 seconds'


if __name__ == '__main__':
    run_file(__file__)
