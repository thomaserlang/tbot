import pytest
from httpx import AsyncClient

from tbot2.channel_chat_filters import TChatFilterScope
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_filter_routes(
    client: AsyncClient,
) -> None:
    user = await user_signin(
        client, scopes=[TChatFilterScope.READ, TChatFilterScope.WRITE]
    )

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/chat-filters',
        json={
            'type': 'caps',
            'settings': {
                'max_percent': 5,
                'min_length': 2,
            },
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()['type'] == 'caps'

    filter_id = r.json()['id']
    r = await client.get(
        f'/api/2/channels/{user.channel.id}/chat-filters/{filter_id}',
    )
    assert r.status_code == 200, r.text
    assert r.json()['settings']['max_percent'] == 5
    assert r.json()['settings']['min_length'] == 2

    r = await client.put(
        f'/api/2/channels/{user.channel.id}/chat-filters/{filter_id}',
        json={
            'type': 'caps',
            'warning_enabled': True,
            'settings': {
                'max_percent': 10,
            },
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()['type'] == 'caps'
    assert r.json()['warning_enabled'] is True
    assert r.json()['settings']['max_percent'] == 10
    assert r.json()['settings']['min_length'] == 2

    r = await client.delete(
        f'/api/2/channels/{user.channel.id}/chat-filters/{filter_id}',
    )
    assert r.status_code == 204, r.text

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/chat-filters/{filter_id}',
    )
    assert r.status_code == 404, r.text


if __name__ == '__main__':
    run_file(__file__)
