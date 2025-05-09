from typing import Any, Literal
from uuid import UUID

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..actions.youtube_live_chat_message_actions import youtube_bot_client
from ..exceptions import YouTubeException


async def live_chat_ban(
    channel_id: UUID,
    live_chat_id: str,
    type: Literal['permanent', 'temporary'],
    banned_youtube_user_channel_id: str,
    ban_duration_seconds: int | None = None,
) -> bool:
    data: dict[str, Any] = {
        'snippet': {
            'liveChatId': live_chat_id,
            'bannedUserDetails': {
                'channelId': banned_youtube_user_channel_id,
            },
            'type': type,
        }
    }
    if type == 'temporary' and ban_duration_seconds:
        data['snippet']['banDurationSeconds'] = ban_duration_seconds

    response = await youtube_bot_client.post(
        url='/liveChat/bans',
        params={
            'part': 'snippet',
        },
        json=data,
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)
    return True
