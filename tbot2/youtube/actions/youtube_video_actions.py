from ..exceptions import YouTubeException
from ..http_client import youtube_api_key_client
from ..schemas.youtube_page_schema import YoutubePage
from ..schemas.youtube_video_schema import YoutubeVideo

PART = {'liveStreamingDetails'}


async def get_youtube_videos(video_ids: list[str]) -> list[YoutubeVideo]:
    response = await youtube_api_key_client.get(
        '/videos',
        params={
            'part': ','.join(PART),
            'id': ','.join(video_ids),
            'maxResults': 50,
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)
    page = YoutubePage[YoutubeVideo].model_validate(response.json())
    return page.items
