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
    get_channel_bot_provider,
    get_channel_oauth_provider,
    save_channel_oauth_provider,
)
from tbot2.common import Provider
from tbot2.config_settings import config
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage


class ChannelProviderOAuth(Auth):
    def __init__(
        self, token_url: str, client_id: str, client_secret: str, provider: Provider
    ) -> None:
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.provider = provider
        self._async_lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        provider: ChannelOAuthProvider | None = None
        channel_id = UUID(request.headers.pop(TBOT_CHANNEL_ID_HEADER, None))
        if not channel_id:
            raise Exception(f'Missing {TBOT_CHANNEL_ID_HEADER} header')

        async with self._async_lock:
            if not request.headers.get('Authorization'):
                provider = await get_channel_oauth_provider(
                    channel_id=channel_id,
                    provider=self.provider,
                )
                if not provider:
                    raise ErrorMessage(
                        _get_missing_provider_message(
                            channel_uuid=channel_id,
                            provider=self.provider,
                        )
                    )
                request.headers['Authorization'] = f'Bearer {provider.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                if not provider:
                    provider = await get_channel_oauth_provider(
                        channel_id=channel_id,
                        provider=self.provider,
                    )
                    if not provider:
                        raise ErrorMessage(
                            _get_missing_provider_message(
                                channel_uuid=channel_id,
                                provider=self.provider,
                            )
                        )
                access_token = await self._refresh_token(
                    channel_id=channel_id, refresh_token=provider.refresh_token or ''
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
                ErrorMessage(f'{response.status_code} {response.text}')
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
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.provider = provider
        self._async_lock = asyncio.Lock()

    async def async_auth_flow(
        self, request: Request
    ) -> typing.AsyncGenerator[Request, Response]:
        provider: BotProvider | None = None
        channel_id = UUID(request.headers.pop(TBOT_CHANNEL_ID_HEADER, None))
        if not channel_id:
            raise Exception(f'Missing {TBOT_CHANNEL_ID_HEADER} header')

        async with self._async_lock:
            if not request.headers.get('Authorization'):
                provider = await get_channel_bot_provider(
                    channel_id=channel_id,
                    provider=self.provider,
                )
                if not provider:
                    raise ErrorMessage(
                        _get_missing_provider_message(
                            channel_uuid=channel_id,
                            provider=self.provider,
                        )
                    )
                request.headers['Authorization'] = f'Bearer {provider.access_token}'

        response = yield request

        if response.status_code == 401:
            async with self._async_lock:
                if not provider:
                    provider = await get_channel_bot_provider(
                        channel_id=channel_id,
                        provider=self.provider,
                    )
                    if not provider:
                        raise ErrorMessage(
                            _get_missing_provider_message(
                                channel_uuid=channel_id,
                                provider=self.provider,
                            )
                        )
                access_token = await self._refresh_token(
                    provider_user_id=provider.provider_user_id,
                    refresh_token=provider.refresh_token or '',
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
                    refresh_token=data['refresh_token'],
                    expires_in=data['expires_in'],
                ),
            )
            return str(data['access_token'])


def _get_missing_provider_message(channel_uuid: UUID, provider: Provider) -> str:
    return (
        f'{provider} must be added as a provider: '
        f'{config.web.base_url}channels/{channel_uuid}/providers'
    )
