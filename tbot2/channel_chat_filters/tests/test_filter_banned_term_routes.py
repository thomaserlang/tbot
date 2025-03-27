import pytest
from httpx import AsyncClient

from tbot2.channel_chat_filters import TChatFilterScope
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_filter_routes(
    client: AsyncClient,
):
    user = await user_signin(
        client, scopes=[TChatFilterScope.READ, TChatFilterScope.WRITE]
    )

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/chat-filters',
        json={
            'type': 'banned_terms',
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data['type'] == 'banned_terms'
    filter_id = data['id']
    assert data['warning_enabled'] is False

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms',
        json={
            'type': 'regex',
            'text': 'test',
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['type'] == 'regex'
    assert data['text'] == 'test'

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms',
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert len(data['records']) == 1
    term_id = data['records'][0]['id']
    assert data['records'][0]['type'] == 'regex'
    assert data['records'][0]['text'] == 'test'

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms/{term_id}',
    )
    assert r.status_code == 200, r.text
    data = r.json()

    r = await client.put(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms/{term_id}',
        json={
            'type': 'phrase',
            'text': 'test2',
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['type'] == 'phrase'
    assert data['text'] == 'test2'

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms/test',
        json={
            'message': 'test',
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['matched'] is False

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms/test',
        json={
            'message': 'test2',
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['matched'] is True
    assert data['sub_id'] == term_id

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms',
        json={
            'type': 'regex',
            'text': '[0-9]+',
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    term_id = data['id']

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms/test',
        json={
            'message': '123',
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['matched'] is True
    assert data['sub_id'] == term_id

    r = await client.delete(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms/{term_id}',
    )
    assert r.status_code == 204, r.text

    r = await client.get(
        f'/api/2/channels/{user.channel.id}/filters/{filter_id}/banned-terms',
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert len(data['records']) == 1


if __name__ == '__main__':
    run_file(__file__)
