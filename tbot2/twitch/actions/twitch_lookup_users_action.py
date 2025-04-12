from uuid import UUID

from twitchAPI.twitch import TwitchUser

from tbot2.common import safe_username
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage

from ..twitch_http_client import twitch_app_client


async def lookup_twitch_users(
    *,
    channel_id: UUID,
    logins: list[str] | None = None,
    user_ids: list[str] | None = None,
) -> list[TwitchUser]:
    if not logins:
        logins = []
    if not user_ids:
        user_ids = []

    response = await twitch_app_client.get(
        '/users',
        params={
            'login': [safe_username(login) for login in logins],
            'id': user_ids,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    data = response.json()
    if not data['data']:
        return []
    return [TwitchUser(**user) for user in data['data']]


async def lookup_twitch_user(
    *,
    channel_id: UUID,
    login: str | None = None,
    user_id: str | None = None,
) -> TwitchUser | None:
    if not login and not user_id:
        raise Exception('login or user_id must be provided')
    if login and user_id:
        raise Exception('login and user_id cannot both be provided')
    data = await lookup_twitch_users(
        channel_id=channel_id,
        logins=[login] if login else [],
        user_ids=[user_id] if user_id else [],
    )
    if not data:
        return
    return data[0]
