import asyncio
import typing
from uuid import UUID

from httpx import AsyncClient, Auth, Request, Response

from tbot2.config_settings import config

from .actions.spotify_oauth_actions import (
    get_spotify_oauth_token,
    save_spotify_oauth_token,
)


class TwitchUserOAuth(Auth):
    def __init__(self):
        self._async_lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        async with self._async_lock:
            channel_id: UUID = UUID(request.headers.get('X-Channel-Id'))
            if not channel_id:
                raise ValueError('Missing X-Channel-Id header')
            token = await get_spotify_oauth_token(channel_id)
            if not token:
                raise ValueError(
                    f'Channel {channel_id} needs to grant the bot access in the dashboard'
                )
            request.headers['Authorization'] = f'Bearer {token.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                token = await self._refresh_token(
                    channel_id=channel_id, refresh_token=token.refresh_token
                )
                if not token:
                    raise ValueError(
                        f'Channel {channel_id} needs to grant the bot access in the dashboard'
                    )
                request.headers['Authorization'] = f'Bearer {token.access_token}'

            yield request

    async def _fetch_token(self, channel_id: UUID):
        return await get_spotify_oauth_token(channel_id)

    async def _refresh_token(self, channel_id: UUID, refresh_token: str):
        async with AsyncClient() as client:
            response = await client.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': config.twitch.client_id,
                    'client_secret': config.twitch.client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()
            await save_spotify_oauth_token(
                channel_id=channel_id,
                access_token=data['access_token'],
                refresh_token=data['refresh_token'],
            )
            return data['access_token']


spotify_client = AsyncClient(
    base_url='https://api.spotify.com/v1',
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
)
