from typing import Annotated
from urllib import parse
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, Security
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from twitchAPI.twitch import TwitchUser

from tbot2.auth_backend import create_token_str
from tbot2.channel import (
    ChannelOAuthProviderRequest,
    ChannelScope,
    save_channel_oauth_provider,
)
from tbot2.common import (
    Oauth2TokenResponse,
    TAccessLevel,
    TokenData,
    TProvider,
    provider_scopes,
)
from tbot2.common.schemas.oauth2_client_schemas import (
    Oauth2AuthorizeParams,
    Oauth2AuthorizeResponse,
    Oauth2TokenParams,
)
from tbot2.common.utils.request_url_for import request_url_for
from tbot2.config_settings import config
from tbot2.dependecies import authenticated
from tbot2.user import UserCreate, get_or_create_user

from ..actions.eventsub_actions import register_eventsubs

twitch_oauth_client = AsyncClient(
    http2=True,
)

router = APIRouter()

SCOPE_OPENID = 'openid user:read:email'
CONNECT_BOT = {
    'user:bot',
    'moderator:manage:automod',
    'moderator:manage:announcements',
    'moderator:manage:chat_messages',
    'moderator:manage:banned_users',
    'channel:moderate',
}
provider_scopes[TProvider.twitch] = ' '.join(
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
    }
)


@router.get('/twitch/sign-in')
async def twitch_sign_in_route(request: Request):
    return RedirectResponse(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope=SCOPE_OPENID,
                state={
                    'mode': 'sign_in',
                },
            ).model_dump()
        )
    )


@router.get('/channels/{channel_id}/twitch/connect-url')
async def get_twitch_connect_url(
    channel_id: UUID,
    request: Request,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelScope.PROVIDERS_WRITE])
    ],
):
    await token_data.channel_has_access(
        channel_id=channel_id, access_level=TAccessLevel.OWNER
    )
    return dict(
        url='https://id.twitch.tv/oauth2/authorize?'
        + parse.urlencode(
            Oauth2AuthorizeParams(
                client_id=config.twitch.client_id,
                response_type='code',
                redirect_uri=str(request_url_for(request, 'twitch_auth_route')),
                scope=provider_scopes[TProvider.twitch],
                state={
                    'channel_id': str(channel_id),
                    'mode': 'connect',
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

    r = await twitch_oauth_client.get(
        url='https://api.twitch.tv/helix/users',
        headers={
            'Client-ID': config.twitch.client_id,
            'Authorization': f'Bearer {response.access_token}',
        },
    )
    twitch_user = TwitchUser(**r.json()['data'][0])

    if params.state['mode'] == 'sign_in':
        result = await get_or_create_user(
            provider=TProvider.twitch,
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
                provider=TProvider.twitch,
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
        return RedirectResponse(f'/sign-in/success#{token}')

    if params.state['mode'] == 'connect':
        channel_id = UUID(params.state['channel_id'])
        await save_channel_oauth_provider(
            channel_id=channel_id,
            provider=TProvider.twitch,
            data=ChannelOAuthProviderRequest(
                access_token=response.access_token,
                refresh_token=response.refresh_token,
                expires_in=response.expires_in,
                scope=provider_scopes[TProvider.twitch],
                name=twitch_user.display_name,
                provider_user_id=twitch_user.id,
            ),
        )
        await register_eventsubs(
            channel_id=channel_id,
        )
        return RedirectResponse(f'/channels/{params.state["channel_id"]}/providers')

    else:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid state mode: {params.state["mode"]}',
        )
