from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import Depends, HTTPException, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.common import (
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
    Oauth2TokenResponse,
    TokenData,
)
from tbot2.config_settings import config
from tbot2.dependecies import authenticated
from tbot2.twitch.router import APIRouter

from ..actions.spotify_oauth_actions import save_spotify_oauth_token

router = APIRouter()

spotify_oauth_client = AsyncClient(
    http2=True,
)


@router.get('/channels/{channel_od}/spotify/connect')
async def spotify_connect_route(
    request: Request, 
    channel_id: UUID,
    token_data: Annotated[TokenData, Security(authenticated)],
):
    return RedirectResponse(
        url='https://accounts.spotify.com/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.spotify.client_id,
                response_type='code',
                redirect_uri=str(request.url_for('spotify_auth_route')),
                scope='playlist-read-private user-read-recently-played user-read-currently-playing',
                state={'channel_id': str(channel_id)},
            ).model_dump()
        )
    )


@router.get('/spotify/auth')
async def spotify_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Depends()],
):
    response = await spotify_oauth_client.post(
        url='https://accounts.spotify.com/api/token',
        params=Oauth2TokenParams(
            client_id=config.twitch.client_id,
            client_secret=config.twitch.client_secret,
            redirect_uri=str(request.url_for('spotify_auth_route')),
            code=params.code,
        ).model_dump(),
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    oauth_response = Oauth2TokenResponse.model_validate(response.json())
    await save_spotify_oauth_token(
        channel_id=request.state.channel_id,
        access_token=oauth_response.access_token,
        refresh_token=oauth_response.refresh_token,
    )
