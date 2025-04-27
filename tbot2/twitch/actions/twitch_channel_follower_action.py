from uuid import UUID

from twitchAPI.twitch import ChannelFollower

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import TwitchException
from ..twitch_http_client import twitch_user_client


async def twitch_channel_follower(
    channel_id: UUID, user_id: str, broadcaster_id: str
) -> ChannelFollower | None:
    response = await twitch_user_client.get(
        '/channels/followers',
        params={
            'broadcaster_id': broadcaster_id,
            'user_id': user_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    data = response.json()
    if not data['data']:
        return
    return ChannelFollower(**data['data'][0])
