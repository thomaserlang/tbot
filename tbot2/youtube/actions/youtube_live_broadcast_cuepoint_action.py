from uuid import UUID

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..actions.youtube_live_chat_message_actions import (
    youtube_user_client,
)
from ..exceptions import YouTubeException
from ..schemas.youtube_live_broadcast_schema import LiveBroadcastCuepoint


async def insert_live_broadcast_cuepoint(
    channel_id: UUID,
    live_broadcast_id: str,
    duration_secs: int,
) -> LiveBroadcastCuepoint:
    response = await youtube_user_client.post(
        url='/liveBroadcasts/cuepoint',
        params={
            'id': live_broadcast_id,
            'cueType': 'cueTypeAd',
        },
        json={
            'durationSecs': duration_secs,
            'cueType': 'cueTypeAd',
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)
    return LiveBroadcastCuepoint.model_validate(response.json())
