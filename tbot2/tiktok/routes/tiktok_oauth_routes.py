from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.auth_backend import create_token_str
from tbot2.channel_provider import (
    ChannelProviderOAuthRequest,
    ChannelProviderRequest,
    ChannelProviderScope,
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
from tbot2.tiktok.schemas.tiktok_user_info_schema import TikTokUserInfoSchema
from tbot2.user import UserCreate, get_or_create_user

router = APIRouter()

client = AsyncClient(
    http2=True,
)


@router.get('/tiktok/sign-in-url')
async def tiktok_sign_in_route(
    request: Request,
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    params = Oauth2AuthorizeParams(
        client_id=config.tiktok.client_id,
        response_type='code',
        redirect_uri=str(request_url_for(request, 'tiktok_auth_route')),
        scope='user.info.basic,user.info.profile',
        state={
            'mode': 'sign_in',
            'redirect_to': redirect_to.redirect_to,
        },
    ).model_dump(exclude_unset=True)
    params['client_key'] = params.pop('client_id')
    return ConnectUrl(
        url=f'https://www.tiktok.com/v2/auth/authorize/?{parse.urlencode(params)}'
    )


@router.get('/channels/{channel_id}/tiktok/connect-url')
async def tiktok_connect_route(
    request: Request,
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelProviderScope.WRITE])
    ],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.ADMIN
    )
    params = Oauth2AuthorizeParams(
        client_id=config.tiktok.client_id,
        response_type='code',
        redirect_uri=str(request_url_for(request, 'tiktok_auth_route')),
        scope=channel_provider_scopes['tiktok'],
        force_verify=True,
        state={
            'channel_id': str(channel_id),
            'mode': 'connect',
            'redirect_to': redirect_to.redirect_to,
        },
    ).model_dump(exclude_unset=True)
    params['client_key'] = params.pop('client_id')
    return ConnectUrl(
        url=f'https://www.tiktok.com/v2/auth/authorize/?{parse.urlencode(params)}'
    )


@router.get('/tiktok/auth', status_code=204)
async def tiktok_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Query()],
) -> RedirectResponse:
    token_params = Oauth2TokenParams(
        client_id=config.tiktok.client_id,
        client_secret=config.tiktok.client_secret,
        redirect_uri=str(request_url_for(request, 'tiktok_auth_route')),
        code=params.code,
    ).model_dump(exclude_unset=True)
    token_params['client_key'] = token_params.pop('client_id')

    response = await client.post(
        url='https://open.tiktokapis.com/v2/oauth/token/',
        params=token_params,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response = Oauth2TokenResponse.model_validate(response.json())

    r = await client.get(
        url='https://open.tiktokapis.com/v2/user/info/',
        params={
            'fields': 'open_id,username,display_name',
        },
        headers={
            'Authorization': f'Bearer {response.access_token}',
        },
    )
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    user_info = TikTokUserInfoSchema.model_validate(r.json())
    match params.state['mode']:
        case 'sign_in':
            result = await get_or_create_user(
                provider='tiktok',
                provider_user_id=user_info.open_id,
                data=UserCreate(
                    username=user_info.username,
                    display_name=user_info.display_name,
                    email=None,
                ),
            )
            if result.created and result.channel:
                channel_provider = await save_channel_provider(
                    channel_id=result.channel.id,
                    provider='tiktok',
                    data=ChannelProviderRequest(
                        scope=params.scope,
                        provider_user_name=user_info.username,
                        provider_user_display_name=user_info.display_name,
                        provider_user_id=user_info.open_id,
                    ),
                )
                await save_channel_provider_oauth(
                    channel_provider_id=channel_provider.id,
                    data=ChannelProviderOAuthRequest(
                        access_token=response.access_token,
                        refresh_token=response.refresh_token or '',
                        expires_in=response.expires_in,
                    ),
                )

            token = await create_token_str(result.token_data)
            return RedirectResponse(
                params.state['redirect_to'] + f'#access_token={token}'
            )

        case 'connect':
            channel_provider = await save_channel_provider(
                channel_id=UUID(params.state['channel_id']),
                provider='tiktok',
                data=ChannelProviderRequest(
                    scope=channel_provider_scopes['tiktok'],
                    provider_user_id=user_info.open_id,
                    provider_user_name=user_info.username,
                    provider_user_display_name=user_info.display_name,
                ),
            )
            await save_channel_provider_oauth(
                channel_provider_id=channel_provider.id,
                data=ChannelProviderOAuthRequest(
                    access_token=response.access_token,
                    refresh_token=response.refresh_token or '',
                    expires_in=response.expires_in,
                ),
            )
        case _:
            raise HTTPException(
                status_code=400,
                detail=f'Invalid state mode: {params.state["mode"]}',
            )
    return RedirectResponse(url=params.state['redirect_to'])
