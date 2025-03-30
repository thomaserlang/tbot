import asyncio
import typing
from uuid import UUID

from httpx import AsyncClient, Auth, Request, Response

from tbot2.channel import (
    ChannelOAuthProviderRequest,
    get_channel_oauth_provider,
    save_channel_oauth_provider,
)
from tbot2.common import TProvider
from tbot2.config_settings import config
from tbot2.constants import TBOT_CHANNEL_ID_HEADER


class SpotifyOAuth(Auth):
    def __init__(self):
        self._async_lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        async with self._async_lock:
            channel_id: UUID = UUID(request.headers.get(TBOT_CHANNEL_ID_HEADER))
            if not channel_id:
                raise ValueError(f'Missing {TBOT_CHANNEL_ID_HEADER} header')
            provider = await get_channel_oauth_provider(
                channel_id=channel_id,
                provider=TProvider.spotify,
            )
            if not provider:
                raise ValueError(
                    f'Channel {channel_id} needs to grant the bot access in the dashboard'
                )
            request.headers['Authorization'] = f'Bearer {provider.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                provider = await self._refresh_token(
                    channel_id=channel_id, refresh_token=provider.refresh_token or ''
                )
                if not provider:
                    raise ValueError(
                        f'Channel {channel_id} needs to grant the bot access in the dashboard'
                    )
                request.headers['Authorization'] = f'Bearer {provider.access_token}'

            yield request

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
            await save_channel_oauth_provider(
                channel_id=channel_id,
                provider=TProvider.spotify,
                data=ChannelOAuthProviderRequest(
                    access_token=data['access_token'],
                    refresh_token=data['refresh_token'],
                    expires_in=data['expires_in'],
                ),
            )
            return data['access_token']


spotify_client = AsyncClient(
    base_url='https://api.spotify.com/v1',
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
)
