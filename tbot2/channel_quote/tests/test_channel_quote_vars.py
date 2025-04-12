from datetime import UTC, datetime

import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_command import TCommand
from tbot2.channel_command.fill_message import fill_message
from tbot2.channel_quote import cmd_var_fillers as cmd_var_fillers
from tbot2.common import ChatMessage, TProvider
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_gambling_stats_vars(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    message = await fill_message(
        response_message=('{quote.add}'),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=UTC),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!qadd test quote',
            msg_id='123',
        ),
        command=TCommand(args=['test', 'quote'], name='qadd'),
    )
    assert message == 'Quote created with number: 1'

    message = await fill_message(
        response_message=('{quote.edit}'),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=UTC),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!qedit 1 test quote edited',
            msg_id='123',
        ),
        command=TCommand(args=['1', 'test', 'quote', 'edited'], name='qedit'),
    )
    assert message == 'Quote updated with number: 1'

    message = await fill_message(
        response_message=('{quote.message} ({quote.number})'),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=UTC),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!q',
            msg_id='123',
        ),
        command=TCommand(args=[], name='q'),
    )
    assert message == 'test quote edited (1)'

    message = await fill_message(
        response_message=('{quote.delete}'),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=UTC),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!qdelete 1',
            msg_id='123',
        ),
        command=TCommand(args=['1'], name='qdelete'),
    )
    assert message == 'Quote deleted with number: 1'


if __name__ == '__main__':
    run_file(__file__)
