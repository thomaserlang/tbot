from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.channel import (
    ChannelProviderOAuthRequest,
    ChannelProviderRequest,
    ChannelScope,
    save_channel_provider,
    save_channel_provider_oauth,
)
from tbot2.common import (
    ConnectUrl,
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
    Oauth2TokenResponse,
    TAccessLevel,
    TokenData,
    channel_provider_scopes,
)
from tbot2.common.schemas.connect_url_schema import RedirectUrl
from tbot2.common.utils.request_url_for import request_url_for
from tbot2.config_settings import config
from tbot2.dependecies import authenticated

router = APIRouter()

client = AsyncClient(
    http2=True,
)

channel_provider_scopes['spotify'] = ' '.join(
    {
        'playlist-read-private',
        'user-read-recently-played',
        'user-read-currently-playing',
    }
)


@router.get('/channels/{channel_id}/spotify/connect-url')
async def spotify_connect_route(
    request: Request,
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_WRITE])
    ],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.ADMIN
    )
    return ConnectUrl(
        url='https://accounts.spotify.com/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.spotify.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'spotify_auth_route')),
                scope=channel_provider_scopes['spotify'],
                force_verify=True,
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump()
        )
    )


@router.get('/spotify/auth', status_code=204)
async def spotify_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Query()],
) -> RedirectResponse:
    response = await client.post(
        url='https://accounts.spotify.com/api/token',
        params=Oauth2TokenParams(
            client_id=config.spotify.client_id,
            client_secret=config.spotify.client_secret,
            redirect_uri=str(request_url_for(request, 'spotify_auth_route')),
            code=params.code,
        ).model_dump(),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response = Oauth2TokenResponse.model_validate(response.json())

    r = await client.get(
        url='https://api.spotify.com/v1/me',
        headers={
            'Authorization': f'Bearer {response.access_token}',
        },
    )
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    user_info = r.json()

    channel_provider = await save_channel_provider(
        channel_id=UUID(params.state['channel_id']),
        provider='spotify',
        data=ChannelProviderRequest(
            scope=channel_provider_scopes['spotify'],
            provider_user_id=user_info['id'],
            provider_user_name=user_info['id'],
            provider_user_display_name=user_info['display_name'],
        ),
    )
    await save_channel_provider_oauth(
        channel_provider_id=channel_provider.id,
        data=ChannelProviderOAuthRequest(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            expires_in=response.expires_in,
        ),
    )

    return RedirectResponse(url=params.state['redirect_to'])
