from datetime import datetime, timezone

import pytest
from uuid6 import uuid7

from tbot2.channel_command.types import TCommand, TMessageVars
from tbot2.channel_command.var_filler import fill_message, fills_vars
from tbot2.common import TProvider
from tbot2.common.schemas.chat_message_schema import ChatMessage
from tbot2.testbase import run_file


@fills_vars(provider='all', vars=('test', 'test2', 'test3'))
async def fill_test_var(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    vars['test'].value = vars['test'].args[0]
    vars['test2'].value = 'bla bla bla 123'
    vars['test3'].value = 'test_value2'


@pytest.mark.asyncio
async def test_var_filler():
    text = await fill_message(
        response_message='Test: {test "Test value"} - {test2}',
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            message='!test',
            channel_id=uuid7(),
            chatter_id=str(uuid7()),
            chatter_name='test_user',
            chatter_display_name='Test User',
            provider=TProvider.twitch,
            provider_id='123',
            msg_id='123',
        ),
        command=TCommand(name='test', args=[]),
    )
    assert text == 'Test: Test value - bla bla bla 123'


if __name__ == '__main__':
    run_file(__file__)
