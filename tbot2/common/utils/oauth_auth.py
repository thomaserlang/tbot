import asyncio
import typing
from uuid import UUID

from httpx import AsyncClient, Auth, Request, Response

from tbot2.bot_providers import (
    BotProvider,
    BotProviderRequest,
    save_bot_provider,
)
from tbot2.channel import (
    ChannelProviderNotFound,
    ChannelProviderOAuth,
    ChannelProviderOAuthRequest,
    get_channel_bot_provider,
    get_channel_provider_oauth,
    save_channel_provider_oauth,
)
from tbot2.common import Provider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage, InternalHttpError


class ChannelProviderOAuthHelper(Auth):
    def __init__(
        self, token_url: str, client_id: str, client_secret: str, provider: Provider
    ) -> None:
        self.token_url: str = token_url
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.provider: Provider = provider
        self._async_lock: asyncio.Lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        channel_id = request.headers.pop(TBOT_CHANNEL_ID_HEADER, None)
        if not channel_id:
            raise Exception(f'Missing {TBOT_CHANNEL_ID_HEADER} header')
        channel_id = UUID(channel_id)

        async with self._async_lock:
            channel_provider_oauth = await get_channel_provider_oauth(
                channel_id=channel_id,
                provider=self.provider,
            )
            if not channel_provider_oauth:
                raise ChannelProviderNotFound(
                    channel_id=channel_id,
                    provider=self.provider,
                )
            request.headers['Authorization'] = (
                f'Bearer {channel_provider_oauth.access_token}'
            )

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                access_token = await self._refresh_token(channel_provider_oauth)
                request.headers['Authorization'] = f'Bearer {access_token}'

            yield request

    async def _refresh_token(self, channel_provider_oauth: ChannelProviderOAuth) -> str:
        async with AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': channel_provider_oauth.refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
            )
            if response.status_code >= 400:
                raise InternalHttpError(response.status_code, response.text)
            data = response.json()

            await save_channel_provider_oauth(
                channel_provider_id=channel_provider_oauth.channel_provider_id,
                data=ChannelProviderOAuthRequest(
                    access_token=data['access_token'],
                    refresh_token=data['refresh_token']
                    if 'refresh_token' in data
                    else channel_provider_oauth.refresh_token,
                    expires_in=data['expires_in'],
                ),
            )
            return str(data['access_token'])


class ChannelProviderBotOAuthHelper(Auth):
    def __init__(
        self, token_url: str, client_id: str, client_secret: str, provider: Provider
    ) -> None:
        self.token_url: str = token_url
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.provider: Provider = provider
        self._async_lock: asyncio.Lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        channel_id = request.headers.pop(TBOT_CHANNEL_ID_HEADER, None)
        if not channel_id:
            raise Exception(f'Missing {TBOT_CHANNEL_ID_HEADER} header')
        channel_id = UUID(channel_id)

        async with self._async_lock:
            bot_provider = await get_channel_bot_provider(
                channel_id=channel_id,
                provider=self.provider,
            )
            if not bot_provider:
                raise ErrorMessage(
                    f'Missing bot provider for channel {channel_id} {self.provider}'
                )
            request.headers['Authorization'] = f'Bearer {bot_provider.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                access_token = await self._refresh_token(bot_provider=bot_provider)
                request.headers['Authorization'] = f'Bearer {access_token}'

            yield request

    async def _refresh_token(self, bot_provider: BotProvider) -> str:
        async with AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': bot_provider.refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
            )
            if response.status_code >= 400:
                ErrorMessage(f'{response.status_code} {response.text}')
            data = response.json()
            await save_bot_provider(
                data=BotProviderRequest(
                    provider=self.provider,
                    provider_user_id=bot_provider.provider_user_id,
                    access_token=data['access_token'],
                    refresh_token=data['refresh_token']
                    if 'refresh_token' in data
                    else bot_provider.refresh_token,
                    expires_in=data['expires_in'],
                ),
            )
            return str(data['access_token'])
