import pytest
from httpx import AsyncClient

from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_me_settings_routes(
    client: AsyncClient,
) -> None:
    await user_signin(client=client, scopes=[])
    response = await client.get(
        '/api/2/me/settings',
    )
    assert response.status_code == 200
    data = response.json()
    assert data['activity_feed_not_types'] == []

    response = await client.put(
        '/api/2/me/settings',
        json={
            'activity_feed_not_types': ['test'],
        },
    )
    assert response.status_code == 204
    response = await client.get(
        '/api/2/me/settings',
    )
    assert response.status_code == 200
    data = response.json()
    assert data['activity_feed_not_types'] == ['test']


if __name__ == '__main__':
    run_file(__file__)
