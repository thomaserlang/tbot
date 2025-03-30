from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import Depends, HTTPException, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.channel_oauth_provider import (
    ChannelOAuthProviderRequest,
    save_channel_oauth_provider,
)
from tbot2.common import (
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
    Oauth2TokenResponse,
    TAccessLevel,
    TokenData,
    TProvider,
)
from tbot2.common.utils.request_url_for import request_url_for
from tbot2.config_settings import config
from tbot2.dependecies import authenticated
from tbot2.twitch.router import APIRouter

router = APIRouter()

spotify_oauth_client = AsyncClient(
    http2=True,
)

SCOPE = 'playlist-read-private user-read-recently-played user-read-currently-playing'


@router.get('/channels/{channel_id}/spotify/connect')
async def spotify_connect_route(
    request: Request,
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.ADMIN
    )
    return RedirectResponse(
        url='https://accounts.spotify.com/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.spotify.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'spotify_auth_route')),
                scope=SCOPE,
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect',
                },
            ).model_dump()
        )
    )


@router.get('/spotify/auth', status_code=204)
async def spotify_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Depends()],
):
    response = await spotify_oauth_client.post(
        url='https://accounts.spotify.com/api/token',
        params=Oauth2TokenParams(
            client_id=config.twitch.client_id,
            client_secret=config.twitch.client_secret,
            redirect_uri=str(request_url_for(request, 'spotify_auth_route')),
            code=params.code,
        ).model_dump(),
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    oauth_response = Oauth2TokenResponse.model_validate(response.json())

    await save_channel_oauth_provider(
        channel_id=UUID(params.state['channel_id']),
        provider=TProvider.spotify,
        data=ChannelOAuthProviderRequest(
            access_token=oauth_response.access_token,
            refresh_token=oauth_response.refresh_token,
            expires_in=oauth_response.expires_in,
            scope=SCOPE,
        ),
    )
