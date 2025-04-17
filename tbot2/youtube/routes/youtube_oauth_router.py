from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.bot_providers import BotProviderRequest, save_bot_provider
from tbot2.channel import (
    ChannelOAuthProviderRequest,
    ChannelScope,
    save_channel_oauth_provider,
)
from tbot2.common import (
    ConnectUrl,
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
    Oauth2TokenResponse,
    TAccessLevel,
    TokenData,
    bot_provider_scopes,
    channel_provider_scopes,
)
from tbot2.common.schemas.connect_url_schema import RedirectUrl
from tbot2.common.utils.request_url_for import request_url_for
from tbot2.config_settings import config
from tbot2.dependecies import authenticated
from tbot2.youtube.schemas.youtube_channel_schema import YoutubeChannel, YoutubeItems

router = APIRouter()

client = AsyncClient(
    http2=True,
)

bot_provider_scopes['youtube'] = ' '.join(
    {
        'https://www.googleapis.com/auth/youtube',
    }
)

channel_provider_scopes['youtube'] = ' '.join(
    {
        'https://www.googleapis.com/auth/youtube',
    }
)


@router.get('/channels/{channel_id}/youtube/connect-url')
async def youtube_connect_route(
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
        url='https://accounts.google.com/o/oauth2/v2/auth?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.youtube.client_id,
                access_type='offline',
                prompt='consent',
                response_type='code',
                redirect_uri=str(request_url_for(request, 'youtube_auth_route')),
                scope=channel_provider_scopes['youtube'],
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump(exclude_unset=True)
        )
    )


@router.get('/channels/{channel_id}/youtube/connect-bot-url')
async def get_youtube_connect_bot_url_route(
    channel_id: UUID,
    request: Request,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_WRITE])
    ],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.OWNER
    )
    return ConnectUrl(
        url='https://accounts.google.com/o/oauth2/v2/auth?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.youtube.client_id,
                access_type='offline',
                prompt='consent',
                response_type='code',
                redirect_uri=str(request_url_for(request, 'youtube_auth_route')),
                scope=bot_provider_scopes['youtube'],
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect_bot',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump(exclude_unset=True)
        )
    )


@router.get('/youtube/system-provider-bot-connect-url')
async def get_youtube_system_provider_bot_connect_url_route(
    request: Request,
    token_data: Annotated[TokenData, Security(authenticated, scopes=[])],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    if not await token_data.is_global_admin():
        raise HTTPException(
            status_code=403,
            detail='Access denied',
        )
    return ConnectUrl(
        url='https://accounts.google.com/o/oauth2/v2/auth?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.youtube.client_id,
                access_type='offline',
                prompt='consent',
                response_type='code',
                redirect_uri=str(request_url_for(request, 'youtube_auth_route')),
                scope=bot_provider_scopes['youtube'],
                state={
                    'mode': 'connect_system_provider_bot',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump(exclude_unset=True)
        )
    )


@router.get('/youtube/auth', status_code=204)
async def youtube_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Query()],
) -> RedirectResponse:
    response = await client.post(
        url='https://oauth2.googleapis.com/token',
        params=Oauth2TokenParams(
            client_id=config.youtube.client_id,
            client_secret=config.youtube.client_secret,
            redirect_uri=str(request_url_for(request, 'youtube_auth_route')),
            code=params.code,
            grant_type='authorization_code',
        ).model_dump(exclude_unset=True),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response = Oauth2TokenResponse.model_validate(response.json())

    match params.state['mode']:
        case 'connect':
            r = await client.get(
                url='https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true',
                headers={
                    'Authorization': f'Bearer {response.access_token}',
                },
            )
            if r.status_code >= 400:
                raise HTTPException(status_code=r.status_code, detail=r.text)

            channels = YoutubeItems[YoutubeChannel].model_validate(r.json())
            if not channels.items:
                raise HTTPException(
                    status_code=400,
                    detail='No channels found',
                )
            channel = channels.items[0]
            await save_channel_oauth_provider(
                channel_id=UUID(params.state['channel_id']),
                provider='youtube',
                data=ChannelOAuthProviderRequest(
                    provider_user_id=channel.id,
                    access_token=response.access_token,
                    refresh_token=response.refresh_token,
                    expires_in=response.expires_in,
                    scope=params.scope,
                    name=channel.snippet.title,
                ),
            )

        case 'connect_system_provider_bot':
            r = await client.get(
                url='https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true',
                headers={
                    'Authorization': f'Bearer {response.access_token}',
                },
            )
            if r.status_code >= 400:
                raise HTTPException(status_code=r.status_code, detail=r.text)
            channels = YoutubeItems[YoutubeChannel].model_validate(r.json())
            if not channels.items:
                raise HTTPException(
                    status_code=400,
                    detail='No channels found',
                )
            channel = channels.items[0]

            await save_bot_provider(
                data=BotProviderRequest(
                    provider='youtube',
                    provider_user_id=channel.id,
                    access_token=response.access_token,
                    refresh_token=response.refresh_token,
                    expires_in=response.expires_in,
                    scope=params.scope,
                    name=channel.snippet.title,
                    system_default=True,
                ),
            )

        case _:
            raise HTTPException(
                status_code=400,
                detail='Invalid mode',
            )

    return RedirectResponse(url=params.state['redirect_to'])
