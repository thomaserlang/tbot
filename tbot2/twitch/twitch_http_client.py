import asyncio
import sys
import typing
from uuid import UUID

from httpx import AsyncClient, Auth, Request, Response
from httpx_auth import OAuth2ClientCredentials
from pydantic import BaseModel
from twitchAPI.object.base import TwitchObject
from twitchAPI.twitch import Twitch

from tbot2.channel_oauth_provider import (
    ChannelOAuthProviderRequest,
    get_channel_oauth_provider,
    save_channel_oauth_provider,
)
from tbot2.common import TProvider
from tbot2.config_settings import config
from tbot2.constants import TBOT_CHANNEL_ID_HEADER


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
            channel_id: UUID = UUID(request.headers.get(TBOT_CHANNEL_ID_HEADER))
            if not channel_id:
                raise ValueError(f'Missing {TBOT_CHANNEL_ID_HEADER} header')
            provider = await get_channel_oauth_provider(
                channel_id=channel_id,
                provider=TProvider.twitch,
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
            await save_channel_oauth_provider(
                channel_id=channel_id,
                provider=TProvider.twitch,
                data=ChannelOAuthProviderRequest(
                    access_token=data['access_token'],
                    refresh_token=data['refresh_token'],
                    expires_in=data['expires_in'],
                ),
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


T = typing.TypeVar('T')


async def get_twitch_pagination(
    response: Response,
    schema: type[T],
) -> list[T]:
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
        response.raise_for_status()
        data = response.json()
        all_data.extend(data['data'])
        pagination = data.get('pagination')

    if issubclass(schema, TwitchObject):
        return [schema(**item) for item in all_data]
    elif issubclass(schema, BaseModel):
        return [schema.model_validate(item) for item in all_data]
    else:
        raise ValueError(
            f'Invalid schema type: {schema}. Must be either BaseModel or TwitchObject.'
        )
