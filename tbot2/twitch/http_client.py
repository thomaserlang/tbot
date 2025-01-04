import asyncio
import sys
import typing

from httpx import AsyncClient, Auth, Request, Response
from httpx_auth import OAuth2ClientCredentials
from twitchAPI.twitch import Twitch

from tbot2.config_settings import config

from .actions.user_oauth_actions import (
    get_twitch_oauth_token,
    save_twitch_oauth_token,
)


class TwitchOauth2ClientCredentials(OAuth2ClientCredentials):
    def __init__(self):
        super().__init__(  # type: ignore
            token_url='https://id.twitch.tv/oauth2/token',
            client_id=config.twitch.client_id,
            client_secret=config.twitch.client_secret,
        )
        self.data = {
            'grant_type': 'client_credentials',
            'client_id': config.twitch.client_id,
            'client_secret': config.twitch.client_secret,
        }


class TwitchUserOAuth(Auth):
    def __init__(self):
        self._async_lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        async with self._async_lock:
            broadcaster_id: str = request.url.params.get('broadcaster_id')
            token = await get_twitch_oauth_token(broadcaster_id)
            if not token:
                raise ValueError(
                    f'Channel {broadcaster_id} needs to grant the bot access in the dashboard'
                )
            request.headers['Authorization'] = f'Bearer {token.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                token = await self._refresh_token(
                    broadcaster_id=broadcaster_id, refresh_token=token.refresh_token
                )
                if not token:
                    raise ValueError(
                        f'Channel {broadcaster_id} needs to grant the bot access in the dashboard'
                    )
                request.headers['Authorization'] = f'Bearer {token.access_token}'

            yield request

    async def _fetch_token(self, broadcaster_id: str):
        return await get_twitch_oauth_token(broadcaster_id)

    async def _refresh_token(self, broadcaster_id: str, refresh_token: str):
        async with AsyncClient() as client:
            response = await client.post(
                'https://id.twitch.tv/oauth2/token',
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': config.twitch.client_id,
                    'client_secret': config.twitch.client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()
            await save_twitch_oauth_token(
                broadcaster_id=broadcaster_id,
                access_token=data['access_token'],
                refresh_token=data['refresh_token'],
            )
            return data['access_token']


twitch_app_client = AsyncClient(
    base_url='https://api.twitch.tv/helix',
    headers={
        'Client-ID': config.twitch.client_id,
    },
    auth=TwitchOauth2ClientCredentials() if 'pytest' not in sys.modules else None,
    http2=True,
)

twitch_user_client = AsyncClient(
    base_url='https://api.twitch.tv/helix',
    headers={
        'Client-ID': config.twitch.client_id,
    },
    auth=TwitchUserOAuth() if 'pytest' not in sys.modules else None,
    http2=True,
)

twitch_client = Twitch(
    app_id=config.twitch.client_id, app_secret=config.twitch.client_secret
)


async def get_twitch_pagination(
    response: Response,
):
    data = response.json()
    all_data: list[dict[str, typing.Any]] = data['data']

    pagination = data.get('pagination')
    while pagination:
        response = await twitch_user_client.get(
            response.url.path.replace('/helix', ''),
            params={
                **response.url.params,
                'after': pagination['cursor'],
            },
        )
        data = response.json()
        all_data.extend(data['data'])
        pagination = data.get('pagination')

    return all_data
