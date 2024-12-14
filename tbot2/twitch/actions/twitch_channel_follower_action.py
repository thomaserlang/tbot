from twitchAPI.twitch import ChannelFollower

from ..http_client import twitch_user_client


async def twitch_channel_follower(user_id: str, broadcaster_id: str):
    response = await twitch_user_client.get(
        '/channels/followers',
        params={
            'broadcaster_id': broadcaster_id,
            'user_id': user_id,
        },
    )
    response.raise_for_status()
    data = response.json()
    if not data['data']:
        return
    return ChannelFollower(**data['data'][0])
