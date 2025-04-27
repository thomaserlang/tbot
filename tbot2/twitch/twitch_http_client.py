import sys
import typing

from httpx import AsyncClient, Response
from httpx_auth import OAuth2ClientCredentials
from pydantic import BaseModel
from twitchAPI.object.base import TwitchObject
from twitchAPI.twitch import Twitch

from tbot2.common.exceptions import ErrorMessage
from tbot2.common.utils.httpx_retry import retry_transport
from tbot2.common.utils.oauth_auth import (
    ChannelProviderBotOAuthHelper,
    ChannelProviderOAuthHelper,
)
from tbot2.config_settings import config


class TwitchOauth2ClientCredentials(OAuth2ClientCredentials):
    def __init__(self) -> None:
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
    transport=retry_transport,
)

twitch_user_client = AsyncClient(
    base_url='https://api.twitch.tv/helix',
    headers={
        'Client-ID': config.twitch.client_id,
    },
    auth=ChannelProviderOAuthHelper(
        provider='twitch',
        token_url='https://id.twitch.tv/oauth2/token',
        client_id=config.twitch.client_id,
        client_secret=config.twitch.client_secret,
    )
    if 'pytest' not in sys.modules
    else None,
    http2=True,
    transport=retry_transport,
)

twitch_bot_client = AsyncClient(
    base_url='https://api.twitch.tv/helix',
    headers={
        'Client-ID': config.twitch.client_id,
    },
    auth=ChannelProviderBotOAuthHelper(
        provider='twitch',
        token_url='https://id.twitch.tv/oauth2/token',
        client_id=config.twitch.client_id,
        client_secret=config.twitch.client_secret,
    )
    if 'pytest' not in sys.modules
    else None,
    http2=True,
    transport=retry_transport,
)

twitch_client = Twitch(
    app_id=config.twitch.client_id, app_secret=config.twitch.client_secret
)


T = typing.TypeVar('T')


async def get_twitch_pagination_yield(
    response: Response,
    schema: type[T],
) -> typing.AsyncGenerator[list[T]]:
    data = response.json()
    if issubclass(schema, TwitchObject):
        yield [schema(**item) for item in data['data']]
    elif issubclass(schema, BaseModel):
        yield [schema.model_validate(item) for item in data['data']]
    else:
        raise Exception(
            f'Invalid schema type: {schema}. Must be either BaseModel or TwitchObject.'
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
            raise ErrorMessage(f'{response.status_code} {response.text}')
        data = response.json()
        if issubclass(schema, TwitchObject):
            yield [schema(**item) for item in data['data']]
        elif issubclass(schema, BaseModel):  # type: ignore
            yield [schema.model_validate(item) for item in data['data']]
        else:
            raise Exception(
                f'Invalid schema type: {schema}. Must be either '
                'BaseModel or TwitchObject.'
            )

        pagination = data.get('pagination')
