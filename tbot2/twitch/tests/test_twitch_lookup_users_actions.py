import pytest
from pytest_httpx import HTTPXMock

from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_twitch_lookup_users(db: None, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url='https://api.twitch.tv/helix/users?login=twitchdev',
        json={
            'data': [
                {
                    'id': '141981764',
                    'login': 'twitchdev',
                    'display_name': 'TwitchDev',
                    'type': '',
                    'broadcaster_type': 'partner',
                    'description': 'Supporting third-party developers building Twitch integrations from chatbots to game integrations.',
                    'profile_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png',
                    'offline_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png',
                    'view_count': 5980557,
                    'email': 'not-real@email.com',
                    'created_at': '2016-12-14T20:32:28Z',
                }
            ]
        },
    )
    from tbot2.twitch.actions.twitch_lookup_users_action import twitch_lookup_users

    users = await twitch_lookup_users(logins=['twitchdev'])
    assert users
    assert users[0].login == 'twitchdev'
    assert users[0].id == '141981764'


if __name__ == '__main__':
    run_file(__file__)
