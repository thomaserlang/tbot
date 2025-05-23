from datetime import UTC, datetime

import pytest
from uuid6 import uuid7

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_command import TCommand
from tbot2.channel_command.fill_message import fill_message
from tbot2.common import ChatMessageCreate
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_gambling_stats_vars(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    message = await fill_message(
        response_message=('{quote.add}'),
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
            message='!qadd test quote',
            provider_message_id='123',
        ),
        command=TCommand(args=['test', 'quote'], name='qadd'),
    )
    assert message == 'Quote created with number: 1'

    message = await fill_message(
        response_message=('{quote.edit}'),
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
            message='!qedit 1 test quote edited',
            provider_message_id='123',
        ),
        command=TCommand(args=['1', 'test', 'quote', 'edited'], name='qedit'),
    )
    assert message == 'Quote updated with number: 1'

    message = await fill_message(
        response_message=('{quote.message} ({quote.number})'),
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
            message='!q',
            provider_message_id='123',
        ),
        command=TCommand(args=[], name='q'),
    )
    assert message == 'test quote edited (1)'

    message = await fill_message(
        response_message=('{quote.delete}'),
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
            message='!qdelete 1',
            provider_message_id='123',
        ),
        command=TCommand(args=['1'], name='qdelete'),
    )
    assert message == 'Quote deleted with number: 1'


if __name__ == '__main__':
    run_file(__file__)
