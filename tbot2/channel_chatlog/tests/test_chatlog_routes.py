import pytest
from uuid6 import uuid7

from tbot2.channel_chatlog import ChatlogsScope, create_chatlog
from tbot2.common import ChatMessageRequest, datetime_now
from tbot2.testbase import AsyncClient, run_file, user_signin


@pytest.mark.asyncio
async def test_create_chatlog(client: AsyncClient) -> None:
    user = await user_signin(
        client=client,
        scopes=[ChatlogsScope.READ],
    )
    await create_chatlog(
        data=ChatMessageRequest(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            channel_id=user.channel.id,
            provider_viewer_id='test',
            viewer_name='test',
            viewer_display_name='test',
            message='test',
            msg_id='test1',
            provider='twitch',
            provider_id='123',
        )
    )
    await create_chatlog(
        data=ChatMessageRequest(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            channel_id=user.channel.id,
            provider_viewer_id='test2',
            viewer_name='test2',
            viewer_display_name='test2',
            message='test2',
            msg_id='test2',
            provider='twitch',
            provider_id='123',
        )
    )

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/chatlogs',
    )
    assert r.status_code == 200
    data = r.json()
    assert data['total'] is None
    assert data['records'][0]['message'] == 'test2'
    assert data['records'][1]['message'] == 'test'

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/chatlogs',
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
