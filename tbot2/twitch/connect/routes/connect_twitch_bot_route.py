from typing import Annotated
from urllib import parse

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.common.schemas.oauth2_client_schemas import (
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
)
from tbot2.config_settings import config

twitch_client = AsyncClient(
    http2=True,
)

router = APIRouter()


@router.get('/connect-bot')
async def connect_twitch_bot_route():
    return RedirectResponse(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=parse.urljoin(
                    config.web.base_url, '/twitch/connect-bot/response'
                ),
                scope='user:bot user:read:chat user:write:chat',
            ).model_dump()
        )
    )


@router.get('/connect-bot/response')
async def connect_twitch_bot_response_route(
    params: Annotated[Oauth2AuthorizeResponse, Depends()],
):
    response = await twitch_client.post(
        url='https://id.twitch.tv/oauth2/token',
        params=Oauth2TokenParams(
            client_id=config.twitch.client_id,
            client_secret=config.twitch.client_secret,
            redirect_uri=parse.urljoin(
                config.web.base_url, '/twitch/connect-bot/response'
            ),
            code=params.code,
        ).model_dump(),
    )

    # TODO: Add the bot to some list so we know it's registered for the channel

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return 'Bot connected.'
