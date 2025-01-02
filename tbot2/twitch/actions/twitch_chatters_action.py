from twitchAPI.twitch import Chatter

from ..actions.twitch_channel_follower_action import twitch_user_client
from ..http_client import get_twitch_pagination


async def get_twitch_chatters(broadcaster_id: str):
    response = await twitch_user_client.get(
        '/chat/chatters',
        params={
            'broadcaster_id': broadcaster_id,
            'moderator_id': broadcaster_id,
            'first': 1000,
        },
    )
    response.raise_for_status()

    results = await get_twitch_pagination(response)

    return [Chatter(**chatter) for chatter in results]
