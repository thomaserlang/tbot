from typing import Annotated
from urllib import parse

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from twitchAPI.twitch import TwitchUser

from tbot2.auth_backend import create_token_str
from tbot2.common import Oauth2TokenResponse, TProvider
from tbot2.common.schemas.oauth2_client_schemas import (
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
)
from tbot2.common.utils.request_url_for import request_url_for
from tbot2.config_settings import config
from tbot2.user import UserCreate
from tbot2.user.actions.oauth_provider_actions import get_or_create_user

twitch_oauth_client = AsyncClient(
    http2=True,
)

router = APIRouter()


@router.get('/twitch/connect-bot')
async def twitch_connect_bot(request: Request):
    return RedirectResponse(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request.url_for('twitch_auth_bot_route')),
                scope='user:bot user:read:chat user:write:chat',
                state={
                    'mode': 'connect_bot',
                },
            ).model_dump()
        )
    )


@router.get('/twitch/sign-in')
async def twitch_sign_in(request: Request):
    return RedirectResponse(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope='openid user:read:email',
                state={
                    'mode': 'sign_in',
                },
            ).model_dump()
        )
    )


@router.get('/twitch/auth')
async def twitch_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Query()],
):
    r = await twitch_oauth_client.post(
        url='https://id.twitch.tv/oauth2/token',
        params=Oauth2TokenParams(
            client_id=config.twitch.client_id,
            client_secret=config.twitch.client_secret,
            redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
            code=params.code,
        ).model_dump(),
    )

    # TODO: Add the bot to some list so we know it's registered for the channel

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    response = Oauth2TokenResponse.model_validate(r.json())

    if params.state['mode'] == 'sign_in':
        r = await twitch_oauth_client.get(
            url='https://api.twitch.tv/helix/users',
            headers={
                'Client-ID': config.twitch.client_id,
                'Authorization': f'Bearer {response.access_token}',
            },
        )
        twitch_user = TwitchUser(**r.json()['data'][0])
        token_data = await get_or_create_user(
            provider=TProvider.twitch,
            provider_user_id=twitch_user.id,
            data=UserCreate(
                username=twitch_user.login,
                display_name=twitch_user.display_name,
                email=twitch_user.email,
            ),
        )

        token = await create_token_str(token_data)
        return RedirectResponse(f'/sign-in/success#{token}')
    else:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid state mode: {params.state["mode"]}',
        )
