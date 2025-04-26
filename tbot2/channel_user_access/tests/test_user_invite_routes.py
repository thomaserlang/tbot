import pytest
from httpx import AsyncClient

from tbot2.auth_backend import create_token_str
from tbot2.channel_user_access import ChannelUserAccessScope
from tbot2.common import TAccessLevel, TokenData
from tbot2.testbase import run_file, user_signin
from tbot2.user import UserCreate, create_user


@pytest.mark.asyncio
async def test_user_invite_routes(client: AsyncClient) -> None:
    user = await user_signin(
        client=client,
        scopes=[ChannelUserAccessScope.WRITE, ChannelUserAccessScope.READ],
    )

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/user-invites',
        json={
            'access_level': TAccessLevel.ADMIN,
        },
    )
    assert r.status_code == 200, r.text
    invite1 = r.json()
    assert invite1['access_level'] == TAccessLevel.ADMIN
    assert invite1['channel_id'] == str(user.channel.id)

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/user-invites',
        json={
            'access_level': TAccessLevel.MOD,
        },
    )
    assert r.status_code == 200, r.text
    invite2 = r.json()

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/user-invites',
    )
    assert r.status_code == 200, r.text
    invites = r.json()
    assert len(invites['records']) == 2
    assert invites['records'][0]['id'] == invite2['id']
    assert invites['records'][1]['id'] == invite1['id']

    # Check that a user with access already can't accept the invite
    r = await client.post(
        f'/api/2/channel-user-invites/{invite1["id"]}/accept',
    )
    assert r.status_code == 400, r.text

    # Accept the invite
    user2 = await create_user(
        data=UserCreate(
            email='test2@example.net',
            display_name='Test User',
            username='testuser2',
        )
    )
    token_str = await create_token_str(
        token_data=TokenData(
            scopes=[ChannelUserAccessScope.WRITE],
            user_id=user2.id,
        )
    )

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/user-invites',
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 403, r.text

    r = await client.post(
        f'/api/2/channel-user-invites/{invite1["id"]}/accept',
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 200, r.text

    # Make sure the invite was deleted
    r = await client.post(
        f'/api/2/channel-user-invites/{invite1["id"]}/accept',
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 404, r.text

    # Check that the user now has access
    r = await client.get(
        f'/api/2/channels/{user.channel.id}/user-invites',
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 200, r.text

    r = await client.delete(
        f'/api/2/channels/{user.channel.id}/user-invites/{invite2["id"]}',
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 204, r.text

    # Test that the admin can't make a user with equal or higher access level
    r = await client.post(
        f'/api/2/channels/{user.channel.id}/user-invites',
        json={
            'access_level': TAccessLevel.ADMIN,
        },
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 403, r.text

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/user-invites',
        json={
            'access_level': TAccessLevel.OWNER,
        },
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 403, r.text

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/user-invites',
    )
    assert r.status_code == 200, r.text
    invites = r.json()
    assert len(invites['records']) == 0

    users_access = await client.get(
        f'/api/2/channels/{user.channel.id}/users-access',
    )
    assert users_access.status_code == 200, users_access.text
    data = users_access.json()
    assert len(data['records']) == 2

    r = await client.delete(
        f'/api/2/channels/{user.channel.id}/users-access/{data["records"][0]["id"]}',
        headers={'Authorization': f'Bearer {token_str}'},
    )
    assert r.status_code == 403, r.text

    r = await client.delete(
        f'/api/2/channels/{user.channel.id}/users-access/{data["records"][0]["id"]}',
    )
    assert r.status_code == 204, r.text
    r = await client.delete(
        f'/api/2/channels/{user.channel.id}/users-access/{data["records"][0]["id"]}',
    )
    assert r.status_code == 404, r.text


if __name__ == '__main__':
    run_file(__file__)
