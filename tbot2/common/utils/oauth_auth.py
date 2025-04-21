import asyncio
import typing
from datetime import UTC
from uuid import UUID

from httpx import AsyncClient, Auth, Request, Response
from loguru import logger

from tbot2.bot_providers import (
    BotProviderRequest,
    save_bot_provider,
)
from tbot2.channel import (
    ChannelProviderNotFound,
    ChannelProviderOAuthRequest,
    get_channel_bot_provider,
    get_channel_provider_oauth,
    save_channel_provider_oauth,
)
from tbot2.common import Provider, datetime_now
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.database import database
from tbot2.exceptions import InternalHttpError


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

        request.headers['Authorization'] = (
            f'Bearer {await self.get_access_token(channel_id=channel_id)}'
        )

        response = yield request

        if response.status_code == 401:
            access_token = await self.refresh_token(channel_id)
            request.headers['Authorization'] = f'Bearer {access_token}'

            yield request

    async def get_access_token(self, channel_id: UUID) -> str:
        access_token = await database.redis.get(
            f'channel_provider_oauth:{self.provider}:{channel_id}',
        )
        if access_token:
            return access_token

        channel_provider_oauth = await get_channel_provider_oauth(
            channel_id=channel_id,
            provider=self.provider,
        )
        if not channel_provider_oauth:
            raise ChannelProviderNotFound(channel_id=channel_id, provider=self.provider)

        expires_in = (
            channel_provider_oauth.expires_at.astimezone(tz=UTC) - datetime_now()
        ).total_seconds()
        if expires_in < 10:
            return await self.refresh_token(channel_id=channel_id)

        await self.cache_access_token(
            channel_id=channel_id,
            access_token=channel_provider_oauth.access_token,
            expires_in=expires_in,
        )
        return channel_provider_oauth.access_token

    async def cache_access_token(
        self, channel_id: UUID, access_token: str, expires_in: float
    ) -> None:
        await database.redis.set(
            f'channel_provider_oauth:{self.provider}:{channel_id}',
            access_token,
            ex=int(expires_in),
        )

    async def refresh_token(self, channel_id: UUID) -> str:
        logger.debug('Refreshing token', channel_id=channel_id, provider=self.provider)
        async with database.redis.lock(
            f'lock_channel_provider_oauth:{self.provider}:{channel_id}',
            timeout=2.0,
        ) as lock:
            if await lock.owned():
                return await self._refresh_token(channel_id=channel_id)
            else:
                await lock.acquire()
                return await self.get_access_token(
                    channel_id=channel_id,
                )

    async def _refresh_token(self, channel_id: UUID) -> str:
        channel_provider_oauth = await get_channel_provider_oauth(
            channel_id=channel_id,
            provider=self.provider,
        )
        if not channel_provider_oauth:
            raise ChannelProviderNotFound(channel_id=channel_id, provider=self.provider)
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
            await self.cache_access_token(
                channel_id=channel_id,
                access_token=data['access_token'],
                expires_in=data['expires_in'],
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

        request.headers['Authorization'] = (
            f'Bearer {await self.get_access_token(channel_id=channel_id)}'
        )

        response = yield request

        if response.status_code == 401:
            access_token = await self.refresh_token(channel_id)
            request.headers['Authorization'] = f'Bearer {access_token}'

            yield request

    async def get_access_token(self, channel_id: UUID) -> str:
        access_token = await database.redis.get(
            f'channel_provider_bot_oauth:{self.provider}:{channel_id}',
        )
        if access_token:
            return access_token

        channel_provider_oauth = await get_channel_provider_oauth(
            channel_id=channel_id,
            provider=self.provider,
        )
        if not channel_provider_oauth:
            raise ChannelProviderNotFound(channel_id=channel_id, provider=self.provider)

        expires_in = (
            channel_provider_oauth.expires_at.astimezone(tz=UTC) - datetime_now()
        ).total_seconds()
        if expires_in < 10:
            return await self.refresh_token(channel_id=channel_id)

        await self.cache_access_token(
            channel_id=channel_id,
            access_token=channel_provider_oauth.access_token,
            expires_in=expires_in,
        )
        return channel_provider_oauth.access_token

    async def cache_access_token(
        self, channel_id: UUID, access_token: str, expires_in: float
    ) -> None:
        await database.redis.set(
            f'channel_provider_bot_oauth:{self.provider}:{channel_id}',
            access_token,
            ex=int(expires_in),
        )

    async def refresh_token(self, channel_id: UUID) -> str:
        logger.debug('Refreshing token', channel_id=channel_id, provider=self.provider)
        async with database.redis.lock(
            f'lock_channel_provider_bot_oauth:{self.provider}:{channel_id}',
            timeout=2.0,
        ) as lock:
            if await lock.owned():
                return await self._refresh_token(channel_id=channel_id)
            else:
                await lock.acquire()
                return await self.get_access_token(
                    channel_id=channel_id,
                )

    async def _refresh_token(self, channel_id: UUID) -> str:
        bot_provider = await get_channel_bot_provider(
            channel_id=channel_id,
            provider=self.provider,
        )
        if not bot_provider:
            raise ChannelProviderNotFound(channel_id=channel_id, provider=self.provider)
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
                raise InternalHttpError(response.status_code, response.text)
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
            await self.cache_access_token(
                channel_id=channel_id,
                access_token=data['access_token'],
                expires_in=data['expires_in'],
            )
            return str(data['access_token'])
