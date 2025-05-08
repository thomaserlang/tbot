import pytest
from httpx import AsyncClient

from tbot2.channel_queue import (
    ChannelQueueScope,
    QueueCreate,
    create_queue,
)
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_queue_viewer_routes(client: AsyncClient) -> None:
    user = await user_signin(
        client,
        scopes=[ChannelQueueScope.READ, ChannelQueueScope.WRITE],
    )

    queue = await create_queue(
        channel_id=user.channel.id,
        data=QueueCreate(
            name='Test queue',
        ),
    )

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/queues/{queue.id}/viewers',
        json={
            'provider': 'twitch',
            'provider_viewer_id': 'test1',
            'display_name': 'test1',
        },
    )
    assert r.status_code == 201
    viewer1 = r.json()
    assert viewer1['position'] == 1

    # Test adding the same viewer again
    r = await client.post(
        f'/api/2/channels/{user.channel.id}/queues/{queue.id}/viewers',
        json={
            'provider': 'twitch',
            'provider_viewer_id': 'test1',
            'display_name': 'test1',
        },
    )
    assert r.status_code == 409

    # Test adding a different viewer
    r = await client.post(
        f'/api/2/channels/{user.channel.id}/queues/{queue.id}/viewers',
        json={
            'provider': 'twitch',
            'provider_viewer_id': 'test2',
            'display_name': 'test2',
        },
    )
    assert r.status_code == 201
    viewer2 = r.json()
    assert viewer2['position'] == 2

    # Move viewer to top
    r = await client.put(
        f'/api/2/channels/{user.channel.id}/queues/{queue.id}/move-to-top',
        json={
            'channel_queue_viewer_id': viewer2['id'],
        },
    )
    assert r.status_code == 204

    # Check viewer positions
    r = await client.get(
        f'/api/2/channels/{user.channel.id}/queues/{queue.id}/viewers',
    )
    assert r.status_code == 200
    viewers = r.json()
    assert len(viewers['records']) == 2
    assert viewers['records'][0]['id'] == viewer2['id']
    assert viewers['records'][0]['position'] == 1
    assert viewers['records'][1]['id'] == viewer1['id']
    assert viewers['records'][1]['position'] == 2


if __name__ == '__main__':
    run_file(__file__)
