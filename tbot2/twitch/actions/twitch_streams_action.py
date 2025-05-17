from ..exceptions import TwitchException
from ..schemas.twitch_stream_schema import TwitchStream
from ..twitch_http_client import twitch_app_client


async def get_twitch_streams(
    *,
    user_ids: list[str],
) -> list[TwitchStream]:
    response = await twitch_app_client.get(
        '/streams',
        params={
            'user_id': user_ids,
        },
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    data = response.json()
    if data['data']:
        return [TwitchStream.model_validate(user) for user in data['data']]
    return []
