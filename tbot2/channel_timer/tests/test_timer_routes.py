import pytest
from httpx import AsyncClient

from tbot2.channel_timer import TimerScope
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_timer_routes(
    client: AsyncClient,
):
    user = await user_signin(client, scopes=TimerScope.get_all_scopes())

    response = await client.post(
        f'/api/2/channels/{user.channel.id}/timers',
        json={
            'name': 'Test timer',
            'messages': ['Test message'],
        },
    )
    assert response.status_code == 201, response.text
    created_timer = response.json()
    assert created_timer['name'] == 'Test timer'
    assert created_timer['messages'] == ['Test message']
    assert created_timer['next_run'] is not None

    # Test getting all timers for a channel
    response = await client.get(f'/api/2/channels/{user.channel.id}/timers')
    assert response.status_code == 200
    timers = response.json()
    assert len(timers['records']) > 0

    # Test getting a specific timer
    response = await client.get(
        f'/api/2/channels/{user.channel.id}/timers/{created_timer["id"]}'
    )
    assert response.status_code == 200
    timer = response.json()
    assert timer['id'] == created_timer['id']

    # Test updating a timer
    response = await client.put(
        f'/api/2/channels/{user.channel.id}/timers/{created_timer["id"]}',
        json={
            'name': 'Updated timer',
            'interval': 5,
            'messages': ['Updated message'],
        },
    )
    assert response.status_code == 200, response.text
    updated_timer = response.json()
    assert updated_timer['name'] == 'Updated timer'
    assert updated_timer['interval'] == 5
    assert updated_timer['messages'] == ['Updated message']
    assert updated_timer['id'] == created_timer['id']
    assert updated_timer['next_run'] != created_timer['next_run']

    # Test deleting a timer
    response = await client.delete(
        f'/api/2/channels/{user.channel.id}/timers/{created_timer["id"]}'
    )
    assert response.status_code == 204

    # Verify the timer is deleted
    response = await client.get(
        f'/api/2/channels/{user.channel.id}/timers/{created_timer["id"]}'
    )
    assert response.status_code == 404


if __name__ == '__main__':
    run_file(__file__)
