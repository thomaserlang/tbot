import pytest
from httpx import AsyncClient

from tbot2.channel import ChannelScope
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_channel_routes(
    client: AsyncClient,
) -> None:
    await user_signin(client, scopes=ChannelScope.get_all_scopes())

    r = await client.post(
        '/api/2/channels',
        json={
            'display_name': 'Test channel 2',
        },
    )
    assert r.status_code == 201, r.text
    channel = r.json()
    assert channel['display_name'] == 'Test channel 2'

    r = await client.put(
        f'/api/2/channels/{channel["id"]}',
        json={
            'display_name': 'Test channel 3',
        },
    )
    assert r.status_code == 200, r.text
    channel = r.json()
    assert channel['display_name'] == 'Test channel 3'

    r = await client.delete(
        f'/api/2/channels/{channel["id"]}',
        params={
            'channel_name': 'wrong name',
        },
    )
    assert r.status_code == 400, r.text

    r = await client.delete(
        f'/api/2/channels/{channel["id"]}',
        params={
            'channel_name': channel['display_name'],
        },
    )
    assert r.status_code == 204, r.text

    r = await client.get(
        f'/api/2/channels/{channel["id"]}',
    )
    assert r.status_code == 404, r.text

    r = await client.get(
        '/api/2/channels',
    )
    assert r.status_code == 200, r.text
    channels = r.json()
    assert len(channels['records']) == 1


if __name__ == '__main__':
    run_file(__file__)
