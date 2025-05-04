from datetime import timedelta

from memoize.configuration import DefaultInMemoryCacheConfiguration  # type: ignore
from memoize.wrapper import memoize  # type: ignore

from tbot2.twitch.schemas.twitch_chat_badge_schema import ChatBadge, ChatBadgeVersion

from ..exceptions import TwitchException
from ..twitch_http_client import twitch_app_client


@memoize(
    configuration=DefaultInMemoryCacheConfiguration(
        capacity=4096,
        method_timeout=timedelta(minutes=2),
        update_after=timedelta(minutes=1),
        expire_after=timedelta(minutes=60),
    )
)  # type: ignore
async def twitch_channel_badges_cached(
    broadcaster_id: str,
) -> dict[str, ChatBadgeVersion]:
    badges = await twitch_channel_badges(broadcaster_id)
    result: dict[str, ChatBadgeVersion] = {}
    if badges:
        for b in badges:
            for v in b.versions:
                result[f'{b.set_id}/{v.id}'] = v
    return result


@memoize(
    configuration=DefaultInMemoryCacheConfiguration(
        capacity=4096,
        method_timeout=timedelta(minutes=2),
        update_after=timedelta(minutes=60),
        expire_after=timedelta(minutes=120),
    )
)  # type: ignore
async def twitch_global_badges_cached() -> dict[str, ChatBadgeVersion]:
    badges = await twitch_global_badges()
    result: dict[str, ChatBadgeVersion] = {}
    if badges:
        for b in badges:
            for v in b.versions:
                result[f'{b.set_id}/{v.id}'] = v
    return result


async def twitch_channel_badges(broadcaster_id: str) -> list[ChatBadge] | None:
    response = await twitch_app_client.get(
        '/chat/badges',
        params={
            'broadcaster_id': broadcaster_id,
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
    return [ChatBadge.model_validate(badge) for badge in data['data']]


async def twitch_global_badges() -> list[ChatBadge] | None:
    response = await twitch_app_client.get(
        '/chat/badges/global',
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    data = response.json()
    if not data['data']:
        return
    return [ChatBadge.model_validate(badge) for badge in data['data']]
