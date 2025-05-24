import asyncio
from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from tbot2.auth_backend import create_token_str
from tbot2.bot_providers import (
    BotProviderRequest,
    get_system_bot_provider,
    save_bot_provider,
)
from tbot2.channel_provider import (
    ChannelProviderOAuthRequest,
    ChannelProviderRequest,
    ChannelProviderScope,
    create_or_update_channel_provider,
    get_channel_provider,
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
    bot_provider_scopes,
    channel_provider_scopes,
)
from tbot2.common.schemas.connect_url_schema import RedirectUrl
from tbot2.common.utils.request_url_for import request_url_for
from tbot2.config_settings import config
from tbot2.dependecies import authenticated
from tbot2.twitch import TwitchUser
from tbot2.user import UserCreate, get_or_create_user

from ..actions.twitch_eventsub_actions import (
    sync_all_eventsubs,
    sync_channel_eventsubs,
)
from ..actions.twitch_mod_user_actions import twitch_add_channel_moderator

client = AsyncClient(
    http2=True,
)

router = APIRouter()

SCOPE_OPENID = 'openid user:read:email'


@router.get('/twitch/sign-in-url')
async def twitch_sign_in_route(
    request: Request,
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    return ConnectUrl(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope=SCOPE_OPENID,
                state={
                    'mode': 'sign_in',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump()
        )
    )


@router.get('/channels/{channel_id}/twitch/connect-url')
async def get_twitch_connect_url_route(
    channel_id: UUID,
    request: Request,
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChannelProviderScope.WRITE]),
    ],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.ADMIN
    )
    return ConnectUrl(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope=channel_provider_scopes['twitch'],
                force_verify=True,
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump(exclude_unset=True)
        )
    )


@router.get('/channels/{channel_id}/twitch/connect-bot-url')
async def get_twitch_connect_bot_url_route(
    channel_id: UUID,
    request: Request,
    token_data: Annotated[
        TokenData,
        Security(authenticated, scopes=[ChannelProviderScope.WRITE]),
    ],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.ADMIN
    )
    return ConnectUrl(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope=bot_provider_scopes['twitch'],
                force_verify=True,
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect_bot',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump(exclude_unset=True)
        )
    )


@router.get('/twitch/system-provider-bot-connect-url')
async def get_twitch_system_provider_bot_connect_url_route(
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
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope=bot_provider_scopes['twitch'],
                force_verify=True,
                state={
                    'mode': 'connect_system_provider_bot',
                    'redirect_to': redirect_to.redirect_to,
                },
            ).model_dump(exclude_unset=True)
        )
    )


@router.get('/twitch/auth')
async def twitch_auth_route(
    request: Request,
    params: Annotated[Oauth2AuthorizeResponse, Query()],
) -> RedirectResponse:
    r = await client.post(
        url='https://id.twitch.tv/oauth2/token',
        params=Oauth2TokenParams(
            client_id=config.twitch.client_id,
            client_secret=config.twitch.client_secret,
            redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
            code=params.code,
        ).model_dump(),
    )

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    response = Oauth2TokenResponse.model_validate(r.json())

    r = await client.get(
        url='https://api.twitch.tv/helix/users',
        headers={
            'Client-ID': config.twitch.client_id,
            'Authorization': f'Bearer {response.access_token}',
        },
    )
    twitch_user = TwitchUser.model_validate(r.json()['data'][0])

    match params.state['mode']:
        case 'sign_in':
            result = await get_or_create_user(
                provider='twitch',
                provider_channel_id=twitch_user.id,
                data=UserCreate(
                    username=twitch_user.login,
                    display_name=twitch_user.display_name,
                    email=twitch_user.email,
                ),
            )
            if result.created and result.channel:
                channel_provider = await create_or_update_channel_provider(
                    channel_id=result.channel.id,
                    provider='twitch',
                    data=ChannelProviderRequest(
                        scope=params.scope,
                        provider_channel_name=twitch_user.login,
                        provider_channel_display_name=twitch_user.display_name,
                        provider_channel_id=twitch_user.id,
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
            channel_id = UUID(params.state['channel_id'])
            channel_provider = await create_or_update_channel_provider(
                channel_id=channel_id,
                provider='twitch',
                data=ChannelProviderRequest(
                    scope=params.scope,
                    provider_channel_name=twitch_user.login,
                    provider_channel_display_name=twitch_user.display_name,
                    provider_channel_id=twitch_user.id,
                    live_stream_id=twitch_user.login,
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

            if bot_provider := await get_system_bot_provider(provider='twitch'):
                asyncio.create_task(
                    twitch_add_channel_moderator(
                        channel_id=channel_id,
                        twitch_user_id=bot_provider.provider_channel_id,
                        broadcaster_id=twitch_user.id,
                    )
                )  # TODO: Move to task queue

            asyncio.create_task(
                sync_channel_eventsubs(channel_provider=channel_provider)
            )  # TODO: Move to task queue

        case 'connect_bot':
            channel_id = UUID(params.state['channel_id'])
            bot_provider = await save_bot_provider(
                data=BotProviderRequest(
                    provider='twitch',
                    provider_channel_id=twitch_user.id,
                    access_token=response.access_token,
                    refresh_token=response.refresh_token,
                    expires_in=response.expires_in,
                    scope=params.scope,
                    name=twitch_user.display_name,
                ),
            )
            await create_or_update_channel_provider(
                channel_id=channel_id,
                provider='twitch',
                data=ChannelProviderRequest(
                    bot_provider_id=bot_provider.id,
                ),
            )
            channel_provider = await get_channel_provider(
                channel_id=channel_id,
                provider_channel_id=twitch_user.id,
                provider='twitch',
            )
            if channel_provider:
                asyncio.create_task(
                    twitch_add_channel_moderator(
                        channel_id=channel_id,
                        twitch_user_id=twitch_user.id,
                        broadcaster_id=channel_provider.provider_channel_id or '',
                    )
                )
                asyncio.create_task(
                    sync_channel_eventsubs(channel_provider=channel_provider)
                )  # TODO: Move to task queue

        case 'connect_system_provider_bot':
            await save_bot_provider(
                data=BotProviderRequest(
                    provider='twitch',
                    provider_channel_id=twitch_user.id,
                    access_token=response.access_token,
                    refresh_token=response.refresh_token,
                    expires_in=response.expires_in,
                    scope=params.scope,
                    name=twitch_user.display_name,
                    system_default=True,
                ),
            )
            asyncio.create_task(sync_all_eventsubs())  # TODO: Move to task queue

        case _:
            raise HTTPException(
                status_code=400,
                detail=f'Invalid state mode: {params.state["mode"]}',
            )

    return RedirectResponse(params.state['redirect_to'])
