from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from twitchAPI.twitch import TwitchUser

from tbot2.auth_backend import create_token_str
from tbot2.bot_providers import (
    BotProviderRequest,
    get_system_bot_provider,
    save_bot_provider,
)
from tbot2.channel import (
    ChannelOAuthProviderRequest,
    ChannelScope,
    get_channel_oauth_provider,
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
from tbot2.user import UserCreate, get_or_create_user

from ..actions.eventsub_actions import (
    refresh_all_eventsubs,
    refresh_channel_eventsubs,
)
from ..actions.twitch_mod_user_actions import twitch_add_channel_moderator

client = AsyncClient(
    http2=True,
)

router = APIRouter()

SCOPE_OPENID = 'openid user:read:email'
bot_provider_scopes['twitch'] = ' '.join(
    {
        'user:bot',
        'user:write:chat',
        'user:read:chat',
        'moderator:manage:automod',
        'moderator:manage:announcements',
        'moderator:manage:chat_messages',
        'moderator:manage:banned_users',
        'moderator:manage:warnings',
        'channel:moderate',
    }
)
channel_provider_scopes['twitch'] = ' '.join(
    {
        'channel:moderate',
        'channel:edit:commercial',
        'channel:manage:polls',
        'channel:manage:predictions',
        'channel:manage:redemptions',
        'channel:manage:broadcast',
        'channel:read:goals',
        'channel:read:hype_train',
        'channel:read:polls',
        'channel:read:predictions',
        'channel:read:redemptions',
        'channel:read:subscriptions',
        'moderator:manage:banned_users',
        'moderator:read:chatters',
        'moderator:manage:chat_messages',
        'moderator:manage:chat_settings',
        'moderation:read',
        'moderator:read:followers',
        'bits:read',
        'channel:bot',
        'channel:manage:moderators',
    }
)


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
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_WRITE])
    ],
    redirect_to: Annotated[RedirectUrl, Depends()],
) -> ConnectUrl:
    await token_data.channel_require_access(
        channel_id=channel_id, access_level=TAccessLevel.OWNER
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
            ).model_dump()
        )
    )


@router.get('/channels/{channel_id}/twitch/connect-bot-url')
async def get_twitch_connect_bot_url_route(
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
            ).model_dump()
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
            ).model_dump()
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

    # TODO: Add the bot to some list so we know it's registered for the channel

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
    twitch_user = TwitchUser(**r.json()['data'][0])

    if params.state['mode'] == 'sign_in':
        result = await get_or_create_user(
            provider='twitch',
            provider_user_id=twitch_user.id,
            data=UserCreate(
                username=twitch_user.login,
                display_name=twitch_user.display_name,
                email=twitch_user.email,
            ),
        )
        if result.created and result.channel:
            await save_channel_oauth_provider(
                channel_id=result.channel.id,
                provider='twitch',
                data=ChannelOAuthProviderRequest(
                    access_token=response.access_token,
                    refresh_token=response.refresh_token,
                    expires_in=response.expires_in,
                    scope=SCOPE_OPENID,
                    name=twitch_user.display_name,
                    provider_user_id=twitch_user.id,
                ),
            )

        token = await create_token_str(result.token_data)
        return RedirectResponse(params.state['redirect_to'] + f'#access_token={token}')

    elif params.state['mode'] == 'connect':
        channel_id = UUID(params.state['channel_id'])
        await save_channel_oauth_provider(
            channel_id=channel_id,
            provider='twitch',
            data=ChannelOAuthProviderRequest(
                access_token=response.access_token,
                refresh_token=response.refresh_token,
                expires_in=response.expires_in,
                scope=channel_provider_scopes['twitch'],
                name=twitch_user.display_name,
                provider_user_id=twitch_user.id,
            ),
        )

        if provider := await get_system_bot_provider(
            provider='twitch',
        ):
            await twitch_add_channel_moderator(
                channel_id=channel_id,
                twitch_user_id=provider.provider_user_id,
                broadcaster_id=twitch_user.id,
            )

        await refresh_channel_eventsubs(
            channel_id=channel_id,
        )

    elif params.state['mode'] == 'connect_bot':
        channel_id = UUID(params.state['channel_id'])
        bot_provider = await save_bot_provider(
            data=BotProviderRequest(
                provider='twitch',
                provider_user_id=twitch_user.id,
                access_token=response.access_token,
                refresh_token=response.refresh_token,
                expires_in=response.expires_in,
                scope=bot_provider_scopes['twitch'],
                name=twitch_user.display_name,
            ),
        )
        await save_channel_oauth_provider(
            channel_id=channel_id,
            provider='twitch',
            data=ChannelOAuthProviderRequest(
                bot_provider_id=bot_provider.id,
            ),
        )
        provider = await get_channel_oauth_provider(
            channel_id=channel_id,
            provider='twitch',
        )
        if provider:
            await twitch_add_channel_moderator(
                channel_id=channel_id,
                twitch_user_id=twitch_user.id,
                broadcaster_id=provider.provider_user_id or '',
            )
        await refresh_channel_eventsubs(
            channel_id=channel_id, event_type='channel.chat.message'
        )

    elif params.state['mode'] == 'connect_system_provider_bot':
        await save_bot_provider(
            data=BotProviderRequest(
                provider='twitch',
                provider_user_id=twitch_user.id,
                access_token=response.access_token,
                refresh_token=response.refresh_token,
                expires_in=response.expires_in,
                scope=bot_provider_scopes['twitch'],
                name=twitch_user.display_name,
                system_default=True,
            ),
        )
        await refresh_all_eventsubs(event_type='channel.chat.message')

    else:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid state mode: {params.state["mode"]}',
        )

    return RedirectResponse(params.state['redirect_to'])
