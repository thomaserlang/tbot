from collections.abc import AsyncGenerator
from uuid import UUID

from twitchAPI.twitch import Chatter

from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage

from ..actions.twitch_channel_follower_action import twitch_user_client
from ..twitch_http_client import get_twitch_pagination_yield


async def get_twitch_chatters(
    channel_id: UUID, broadcaster_id: str
) -> AsyncGenerator[list[Chatter]]:
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
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    return get_twitch_pagination_yield(response, schema=Chatter)
