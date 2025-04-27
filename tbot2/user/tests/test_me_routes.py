import pytest
from httpx import AsyncClient

from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_me_routes(
    client: AsyncClient,
) -> None:
    user = await user_signin(client=client, scopes=[])
    response = await client.get(
        '/api/2/me',
    )
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(user.user.id)
    assert 'email' not in data


if __name__ == '__main__':
    run_file(__file__)
