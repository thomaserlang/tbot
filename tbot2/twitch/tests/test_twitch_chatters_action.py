import pytest
from pytest_httpx import HTTPXMock
from uuid6 import uuid7

from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_get_twitch_chatters(db: None, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url='https://api.twitch.tv/helix/chat/chatters?broadcaster_id=123&moderator_id=123&first=1000',
        json={
            'data': [
                {
                    'user_id': '1',
                    'user_login': 'smittysmithers',
                    'user_name': 'smittysmithers',
                }
            ],
            'pagination': {'cursor': 'c123'},
        },
    )
    httpx_mock.add_response(
        url='https://api.twitch.tv/helix/chat/chatters?broadcaster_id=123&moderator_id=123&first=1000&after=c123',
        json={
            'data': [
                {
                    'user_id': '2',
                    'user_login': 'smittysmithers2',
                    'user_name': 'smittysmithers2',
                }
            ],
            'pagination': {},
        },
    )
    from tbot2.twitch.actions.twitch_chatters_action import get_twitch_chatters

    i = 0
    async for chatters in await get_twitch_chatters(
        channel_id=uuid7(),
        broadcaster_id='123',
    ):
        assert chatters
        if i == 0:
            assert chatters[0].user_login == 'smittysmithers'
            assert chatters[0].user_id == '1'
            assert chatters[0].user_name == 'smittysmithers'
        else:
            assert chatters[0].user_login == 'smittysmithers2'
            assert chatters[0].user_id == '2'
            assert chatters[0].user_name == 'smittysmithers2'
        i += 1


if __name__ == '__main__':
    run_file(__file__)
