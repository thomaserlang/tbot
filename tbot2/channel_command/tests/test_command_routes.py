import pytest

from tbot2.channel_command import TCommandScope
from tbot2.testbase import AsyncClient, run_file, user_signin


@pytest.mark.asyncio
async def test_command_routes(client: AsyncClient) -> None:
    user = await user_signin(
        client=client, scopes=[TCommandScope.READ, TCommandScope.WRITE]
    )

    r = await client.post(
        f'/api/2/channels/{user.channel.id}/commands',
        json={
            'cmds': ['test'],
            'response': 'test response',
        },
    )
    assert r.status_code == 201
    assert 'test' in r.json()['cmds']
    assert r.json()['response'] == 'test response'


if __name__ == '__main__':
    run_file(__file__)
