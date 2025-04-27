import pytest
from httpx import AsyncClient

from tbot2.channel_user_access import ChannelUserAccessScope
from tbot2.common import TAccessLevel
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_user_invite_routes(client: AsyncClient) -> None:
    user = await user_signin(client=client, scopes=[ChannelUserAccessScope.READ])

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/users-access',
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert len(data['records']) == 1
    assert data['records'][0]['access_level'] == TAccessLevel.OWNER
    assert data['records'][0]['channel_id'] == str(user.channel.id)


if __name__ == '__main__':
    run_file(__file__)
