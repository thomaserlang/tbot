from twitchAPI.twitch import TwitchUser

from tbot2.common.utils.text_utils import safe_username

from ..http_client import twitch_app_client


async def twitch_lookup_users(logins: list[str] = [], user_ids: list[str] = []):
    request = await twitch_app_client.get(
        '/users',
        params={
            'login': [safe_username(login) for login in logins],
            'id': user_ids,
        },
    )
    request.raise_for_status()
    data = request.json()
    if not data['data']:
        return
    return [TwitchUser(**user) for user in data['data']]
