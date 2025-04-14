import pytest
from uuid6 import uuid7

from tbot2.chatlog import create_chatlog
from tbot2.common import ChatMessage, datetime_now
from tbot2.testbase import AsyncClient, run_file, user_signin


@pytest.mark.asyncio
async def test_create_chatlog(client: AsyncClient) -> None:
    user = await user_signin(
        client,
        scopes=[],
    )
    t = await create_chatlog(
        data=ChatMessage(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            channel_id=user.channel.id,
            chatter_id='test',
            chatter_name='test',
            chatter_display_name='test',
            message='test',
            msg_id='test',
            provider='twitch',
            provider_id='123',
        )
    )
    assert t is True


if __name__ == '__main__':
    run_file(__file__)
