import pytest
from uuid6 import uuid7

from tbot2.channel_chat_message import ChatMessageScope, create_chat_message
from tbot2.common import ChatMessageCreate, datetime_now
from tbot2.testbase import AsyncClient, run_file, user_signin


@pytest.mark.asyncio
async def test_chat_messages_routes(client: AsyncClient) -> None:
    user = await user_signin(
        client=client,
        scopes=[ChatMessageScope.READ],
    )
    await create_chat_message(
        data=ChatMessageCreate(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            channel_id=user.channel.id,
            provider_viewer_id='test',
            viewer_name='test',
            viewer_display_name='test',
            message='test',
            provider_message_id='test1',
            provider='twitch',
            provider_channel_id='123',
        )
    )
    await create_chat_message(
        data=ChatMessageCreate(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            channel_id=user.channel.id,
            provider_viewer_id='test2',
            viewer_name='test2',
            viewer_display_name='test2',
            message='test2',
            provider_message_id='test2',
            provider='twitch',
            provider_channel_id='123',
        )
    )

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/chat-messages',
    )
    assert r.status_code == 200
    data = r.json()
    assert data['total'] is None
    assert data['records'][0]['message'] == 'test2'
    assert data['records'][1]['message'] == 'test'

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/chat-messages',
        params={
            'provider': 'twitch',
            'provider_viewer_id': 'test',
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data['total'] is None
    assert data['records'][0]['message'] == 'test'


if __name__ == '__main__':
    run_file(__file__)
