import sys
import typing

from httpx import AsyncClient, Response
from httpx_auth import OAuth2ClientCredentials
from pydantic import BaseModel
from twitchAPI.object.base import TwitchObject
from twitchAPI.twitch import Twitch

from tbot2.common import TProvider
from tbot2.common.utils.oauth_auth import (
    ChannelProviderBotOAuth,
    ChannelProviderOAuth,
)
from tbot2.config_settings import config


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
    auth=ChannelProviderOAuth(
        provider=TProvider.twitch,
        token_url='https://id.twitch.tv/oauth2/token',
        client_id=config.twitch.client_id,
        client_secret=config.twitch.client_secret,
    )
    if 'pytest' not in sys.modules
    else None,
    http2=True,
)

twitch_bot_client = AsyncClient(
    base_url='https://api.twitch.tv/helix',
    headers={
        'Client-ID': config.twitch.client_id,
    },
    auth=ChannelProviderBotOAuth(
        provider=TProvider.twitch,
        token_url='https://id.twitch.tv/oauth2/token',
        client_id=config.twitch.client_id,
        client_secret=config.twitch.client_secret,
    )
    if 'pytest' not in sys.modules
    else None,
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
        if response.status_code >= 400:
            ValueError(f'{response.status_code} {response.text}')
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


async def get_twitch_pagination_yield(
    response: Response,
    schema: type[T],
) -> typing.AsyncGenerator[T]:
    data = response.json()
    for item in data['data']:
        if issubclass(schema, TwitchObject):
            yield schema(**item)
        elif issubclass(schema, BaseModel):
            yield schema.model_validate(item)
        else:
            raise ValueError(
                f'Invalid schema type: {schema}. Must be either BaseModel or '
                'TwitchObject.'
            )

    pagination = data.get('pagination')
    while pagination:
        response = await twitch_user_client.get(
            response.url.path.replace('/helix', ''),
            params={
                **response.url.params,
                'after': pagination['cursor'],
            },
        )
        if response.status_code >= 400:
            raise ValueError(f'{response.status_code} {response.text}')
        data = response.json()
        for item in data['data']:
            if issubclass(schema, TwitchObject):
                yield schema(**item)
            elif issubclass(schema, BaseModel):
                yield schema.model_validate(item)
            else:
                raise ValueError(
                    f'Invalid schema type: {schema}. Must be either BaseModel or '
                    'TwitchObject.'
                )

        pagination = data.get('pagination')
