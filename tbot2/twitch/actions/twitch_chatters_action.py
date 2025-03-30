from uuid import UUID

from twitchAPI.twitch import Chatter

from tbot2.constants import TBOT_CHANNEL_ID_HEADER

from ..actions.twitch_channel_follower_action import twitch_user_client
from ..twitch_http_client import get_twitch_pagination


async def get_twitch_chatters(channel_id: UUID, broadcaster_id: str):
    response = await twitch_user_client.get(
        '/chat/chatters',
        params={
            'broadcaster_id': broadcaster_id,
            'moderator_id': broadcaster_id,
            'first': 1000,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    response.raise_for_status()

    return await get_twitch_pagination(response, schema=Chatter)
