import sys
import typing

from httpx import AsyncClient, Response
from httpx_auth import OAuth2ClientCredentials
from pydantic import BaseModel

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

T = typing.TypeVar('T', bound=BaseModel)


async def get_twitch_pagination_yield(
    *,
    client: AsyncClient,
    response: Response,
    response_model: type[T],
) -> typing.AsyncGenerator[list[T]]:
    data = response.json()

    yield [response_model.model_validate(item) for item in data['data']]

    pagination = data.get('pagination')
    while pagination:
        response = await client.get(
            response.url.path.replace('/helix', ''),
            params={
                **response.url.params,
                'after': pagination['cursor'],
            },
            headers=response.request.headers,
        )
        if response.status_code >= 400:
            raise ErrorMessage(f'{response.status_code} {response.text}')
        data = response.json()
        yield [response_model.model_validate(item) for item in data['data']]
        pagination = data.get('pagination')
