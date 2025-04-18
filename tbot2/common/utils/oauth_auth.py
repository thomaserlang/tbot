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
    ChannelOAuthProvider,
    ChannelOAuthProviderRequest,
    ChannelProviderNotFound,
    get_channel_bot_provider,
    get_channel_oauth_provider,
    save_channel_oauth_provider,
)
from tbot2.common import Provider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage, InternalHttpError


class ChannelProviderOAuth(Auth):
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
        channel_provider: ChannelOAuthProvider | None = None
        channel_id = request.headers.pop(TBOT_CHANNEL_ID_HEADER, None)
        if not channel_id:
            raise Exception(f'Missing {TBOT_CHANNEL_ID_HEADER} header')
        channel_id = UUID(channel_id)

        async with self._async_lock:
            if not request.headers.get('Authorization'):
                channel_provider = await get_channel_oauth_provider(
                    channel_id=channel_id,
                    provider=self.provider,
                )
                if not channel_provider:
                    raise ChannelProviderNotFound(
                        channel_id=channel_id,
                        provider=self.provider,
                    )
                request.headers['Authorization'] = (
                    f'Bearer {channel_provider.access_token}'
                )

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                if not channel_provider:
                    channel_provider = await get_channel_oauth_provider(
                        channel_id=channel_id,
                        provider=self.provider,
                    )
                    if not channel_provider:
                        raise ChannelProviderNotFound(
                            channel_id=channel_id,
                            provider=self.provider,
                        )
                access_token = await self._refresh_token(
                    channel_id=channel_id,
                    refresh_token=channel_provider.refresh_token or '',
                )
                request.headers['Authorization'] = f'Bearer {access_token}'

            yield request

    async def _refresh_token(self, channel_id: UUID, refresh_token: str) -> str:
        async with AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
            )
            if response.status_code >= 400:
                raise InternalHttpError(response.status_code, response.text)
            data = response.json()

            await save_channel_oauth_provider(
                channel_id=channel_id,
                provider=self.provider,
                data=ChannelOAuthProviderRequest(
                    access_token=data['access_token'],
                    # For e.g. spotify they do not give a new refresh token
                    refresh_token=data['refresh_token']
                    if 'refresh_token' in data
                    else refresh_token,
                    expires_in=data['expires_in'],
                ),
            )
            return str(data['access_token'])


class ChannelProviderBotOAuth(Auth):
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
        bot_provider: BotProvider | None = None
        channel_id = request.headers.pop(TBOT_CHANNEL_ID_HEADER, None)
        if not channel_id:
            raise Exception(f'Missing {TBOT_CHANNEL_ID_HEADER} header')
        channel_id = UUID(channel_id)

        async with self._async_lock:
            if not request.headers.get('Authorization'):
                bot_provider = await get_channel_bot_provider(
                    channel_id=channel_id,
                    provider=self.provider,
                )
                if not bot_provider:
                    raise ErrorMessage(
                        'Missing bot provider for channel '
                        f'{channel_id} {self.provider}'
                    )
                request.headers['Authorization'] = f'Bearer {bot_provider.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                if not bot_provider:
                    bot_provider = await get_channel_bot_provider(
                        channel_id=channel_id,
                        provider=self.provider,
                    )
                    if not bot_provider:
                        raise ErrorMessage(
                            'Missing bot provider for channel '
                            f'{channel_id} {self.provider}'
                        )
                access_token = await self._refresh_token(
                    provider_user_id=bot_provider.provider_user_id,
                    refresh_token=bot_provider.refresh_token or '',
                )
                request.headers['Authorization'] = f'Bearer {access_token}'

            yield request

    async def _refresh_token(self, provider_user_id: str, refresh_token: str) -> str:
        async with AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
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
                    provider_user_id=provider_user_id,
                    access_token=data['access_token'],
                    refresh_token=data['refresh_token']
                    if 'refresh_token' in data
                    else refresh_token,
                    expires_in=data['expires_in'],
                ),
            )
            return str(data['access_token'])
