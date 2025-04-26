from tbot2.channel_provider import ChannelProvider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import YouTubeError, YouTubeException
from ..schemas.youtube_live_stream_schema import LiveStream, LiveStreamInsert
from ..schemas.youtube_page_schema import YoutubePage
from .youtube_live_broadcast_actions import youtube_user_client

PART = {'id', 'snippet', 'status', 'cdn', 'contentDetails'}


async def get_live_streams(
    channel_provider: ChannelProvider,
    mine: bool | None = None,
    id: str | None = None,
) -> list[LiveStream]:
    params = {
        'part': ','.join(PART),
    }
    if mine is not None:
        params['mine'] = 'true' if mine else 'false'
    if id:
        params['id'] = id
    r = await youtube_user_client.get(
        '/liveStreams',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params=params,
    )
    if r.status_code >= 400:
        raise YouTubeException(YouTubeError.model_validate(r.json()))
    page = YoutubePage[LiveStream].model_validate(r.json())
    return page.items


async def create_live_stream(
    channel_provider: ChannelProvider, data: LiveStreamInsert
) -> LiveStream:
    r = await youtube_user_client.post(
        '/liveStreams',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params={
            'part': ','.join(PART),
        },
        json=data.model_dump(exclude_unset=True, exclude_none=True, mode='json'),
    )
    if r.status_code >= 400:
        raise YouTubeException(YouTubeError.model_validate(r.json()))
    return LiveStream.model_validate(r.json())
