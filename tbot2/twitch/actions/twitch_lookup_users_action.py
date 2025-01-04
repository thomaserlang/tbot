from twitchAPI.twitch import TwitchUser

from tbot2.common import safe_username

from ..http_client import twitch_app_client


async def lookup_twitch_users(
    *, logins: list[str] = [], user_ids: list[str] = []
) -> list[TwitchUser]:
    response = await twitch_app_client.get(
        '/users',
        params={
            'login': [safe_username(login) for login in logins],
            'id': user_ids,
        },
    )
    response.raise_for_status()
    data = response.json()
    if not data['data']:
        return []
    return [TwitchUser(**user) for user in data['data']]


async def lookup_twitch_user(*, login: str | None = None, user_id: str | None = None):
    if not login and not user_id:
        raise ValueError('login or user_id must be provided')
    if login and user_id:
        raise ValueError('login and user_id cannot both be provided')
    data = await lookup_twitch_users(
        logins=[login] if login else [], user_ids=[user_id] if user_id else []
    )
    if not data:
        return
    return data[0]
