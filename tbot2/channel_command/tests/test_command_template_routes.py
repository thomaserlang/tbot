import pytest

from tbot2.channel_command import CommandCreate, CommandScope
from tbot2.config_settings import config
from tbot2.testbase import AsyncClient, run_file, user_signin


@pytest.mark.asyncio
async def test_command_routes(client: AsyncClient) -> None:
    user = await user_signin(
        client=client, scopes=[CommandScope.READ, CommandScope.WRITE]
    )
    config.global_admins = {user.user.id}

    r = await client.post(
        '/api/2/command-templates',
        json={
            'title': 'test',
            'commands': [
                CommandCreate(
                    cmds=['test'],
                    response='test response',
                ).model_dump()
            ],
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert 'test' in data['commands'][0]['cmds']

    r = await client.get(
        f'/api/2/command-templates/{data["id"]}',
    )
    assert r.status_code == 200
    data = r.json()
    assert 'test' in data['commands'][0]['cmds']
    assert data['title'] == 'test'

    r = await client.get('/api/2/command-templates')
    assert r.status_code == 200
    data = r.json()
    assert len(data['records']) == 1
    assert 'test' in data['records'][0]['commands'][0]['cmds']
    assert data['records'][0]['title'] == 'test'

    r = await client.put(
        f'/api/2/command-templates/{data["records"][0]["id"]}',
        json={
            'title': 'test2',
            'commands': [
                CommandCreate(
                    cmds=['test2'],
                    response='test response2',
                ).model_dump(),
                CommandCreate(
                    cmds=['test3'],
                    response='test response3',
                ).model_dump(),
            ],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert 'test2' in data['commands'][0]['cmds']
    assert 'test3' in data['commands'][1]['cmds']
    assert data['title'] == 'test2'

    r = await client.delete(
        f'/api/2/command-templates/{data["id"]}',
    )
    assert r.status_code == 204

    r = await client.get(
        f'/api/2/command-templates/{data["id"]}',
    )
    assert r.status_code == 404

    r = await client.get('/api/2/command-templates')
    assert r.status_code == 200
    data = r.json()
    assert len(data['records']) == 0


if __name__ == '__main__':
    run_file(__file__)
