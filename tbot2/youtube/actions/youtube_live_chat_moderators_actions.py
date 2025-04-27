from uuid import UUID

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import YouTubeException
from ..http_client import youtube_user_client


async def add_live_chat_moderator(
    channel_id: UUID,
    moderator_channel_id: str,
    live_chat_id: str,
) -> bool:
    response = await youtube_user_client.post(
        url='/liveChat/moderators',
        params={
            'part': 'snippet',
        },
        json={
            'snippet': {
                'liveChatId': live_chat_id,
                'moderatorDetails': {
                    'channelId': moderator_channel_id,
                },
            }
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)
    return True
