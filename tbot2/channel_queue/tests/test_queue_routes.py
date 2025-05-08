import pytest
from httpx import AsyncClient

from tbot2.channel_queue import ChannelQueueScope
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_queue_routes(client: AsyncClient) -> None:
    user = await user_signin(
        client,
        scopes=[ChannelQueueScope.READ, ChannelQueueScope.WRITE],
    )

    response = await client.get(f'/api/2/channels/{user.channel.id}/queues')
    assert response.status_code == 200
    queues = response.json()
    assert len(queues['records']) == 0

    # Create a queue
    response = await client.post(
        f'/api/2/channels/{user.channel.id}/queues',
        json={
            'name': 'Test queue',
        },
    )
    assert response.status_code == 201
    queue = response.json()
    assert queue['name'] == 'Test queue'

    # Get the queue by ID
    response = await client.get(
        f'/api/2/channels/{user.channel.id}/queues/{queue["id"]}',
    )
    assert response.status_code == 200
    queue_data = response.json()
    assert queue_data['name'] == 'Test queue'

    # Update the queue
    response = await client.put(
        f'/api/2/channels/{user.channel.id}/queues/{queue["id"]}',
        json={
            'name': 'Updated queue',
        },
    )
    assert response.status_code == 200, response.text
    updated_queue = response.json()
    assert updated_queue['name'] == 'Updated queue'

    # Get queues
    response = await client.get(f'/api/2/channels/{user.channel.id}/queues')
    assert response.status_code == 200
    queues = response.json()
    assert len(queues['records']) == 1

    # Delete the queue
    response = await client.delete(
        f'/api/2/channels/{user.channel.id}/queues/{queue["id"]}',
    )
    assert response.status_code == 204
    response = await client.get(f'/api/2/channels/{user.channel.id}/queues')
    assert response.status_code == 200
    queues = response.json()
    assert len(queues['records']) == 0


if __name__ == '__main__':
    run_file(__file__)
