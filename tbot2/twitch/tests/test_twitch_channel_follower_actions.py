from datetime import datetime, timezone

import pytest
from pytest_httpx import HTTPXMock

from tbot2.testbase import run_file
from tbot2.twitch.actions.twitch_channel_follower_action import twitch_channel_follower


@pytest.mark.asyncio
async def test_twitch_channel_follower(db: None, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url='https://api.twitch.tv/helix/channels/followers?broadcaster_id=141981764&user_id=11111',
        json={
            'total': 1,
            'data': [
                {
                    'user_id': '11111',
                    'user_name': 'UserDisplayName',
                    'user_login': 'userloginname',
                    'followed_at': '2022-05-24T22:22:08Z',
                },
            ],
            'pagination': {'cursor': 'asd'},
        },
    )

    following = await twitch_channel_follower(
        user_id='11111', broadcaster_id='141981764'
    )
    assert following
    assert following.user_id == '11111'
    assert following.user_name == 'UserDisplayName'
    assert following.user_login == 'userloginname'
    assert following.followed_at == datetime(
        2022,
        5,
        24,
        22,
        22,
        8,
        tzinfo=timezone.utc,
    )


if __name__ == '__main__':
    run_file(__file__)
