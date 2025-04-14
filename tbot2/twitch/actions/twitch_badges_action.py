from tbot2.exceptions import ErrorMessage
from tbot2.twitch.schemas.twitch_chat_badge_schema import ChatBadge

from ..twitch_http_client import twitch_app_client


async def twitch_channel_badges(broadcaster_id: str) -> list[ChatBadge] | None:
    response = await twitch_app_client.get(
        '/chat/badges',
        params={
            'broadcaster_id': broadcaster_id,
        },
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    data = response.json()
    if not data['data']:
        return
    return [ChatBadge.model_validate(badge) for badge in data['data']]


async def twitch_global_badges() -> list[ChatBadge] | None:
    response = await twitch_app_client.get(
        '/chat/badges/global',
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    data = response.json()
    if not data['data']:
        return 
    return [ChatBadge.model_validate(badge) for badge in data['data']]
