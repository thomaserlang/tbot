import pytest
from uuid6 import uuid7

from tbot2.channel_command import MessageVars, TCommand, fills_vars
from tbot2.channel_command.fill_message import fill_message
from tbot2.common import datetime_now
from tbot2.common.schemas.chat_message_request_schemas import ChatMessageCreate
from tbot2.testbase import run_file


@fills_vars(provider='all', vars=('test', 'test2', 'test3'))
async def fill_test_var(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
) -> None:
    vars['test'].value = vars['test'].args[0]
    vars['test2'].value = 'bla bla bla 123'
    vars['test3'].value = 'test_value2'


@pytest.mark.asyncio
async def test_var_filler() -> None:
    text = await fill_message(
        response_message='Test: {test "Test value"} - {test2}',
        chat_message=ChatMessageCreate(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            message='!test',
            channel_id=uuid7(),
            provider_viewer_id=str(uuid7()),
            viewer_name='test_user',
            viewer_display_name='Test User',
            provider='twitch',
            provider_channel_id='123',
            provider_message_id='123',
        ),
        command=TCommand(name='test', args=[]),
    )
    assert text == 'Test: Test value - bla bla bla 123'


if __name__ == '__main__':
    run_file(__file__)
