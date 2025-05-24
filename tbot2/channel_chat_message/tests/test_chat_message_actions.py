import pytest
from uuid6 import uuid7

from tbot2.channel_chat_message import create_chat_message
from tbot2.common import ChatMessageCreate, datetime_now
from tbot2.testbase import AsyncClient, run_file, user_signin


@pytest.mark.asyncio
async def test_create_chat_message(client: AsyncClient) -> None:
    user = await user_signin(
        client,
        scopes=[],
    )
    t = await create_chat_message(
        data=ChatMessageCreate(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            channel_id=user.channel.id,
            provider_viewer_id='test',
            viewer_name='test',
            viewer_display_name='test',
            message='test',
            provider_message_id='test',
            provider='twitch',
            provider_channel_id='123',
        )
    )
    assert t.id is not None
    assert t.type == 'message'


if __name__ == '__main__':
    run_file(__file__)
