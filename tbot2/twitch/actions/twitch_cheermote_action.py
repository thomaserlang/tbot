from datetime import timedelta

from memoize.configuration import DefaultInMemoryCacheConfiguration  # type: ignore
from memoize.wrapper import memoize  # type: ignore

from ..exceptions import TwitchException
from ..schemas.twitch_cheermote_schema import (
    Cheermote,
    CheermoteResponse,
    CheermoteTier,
)
from ..twitch_http_client import twitch_app_client


@memoize(
    configuration=DefaultInMemoryCacheConfiguration(
        capacity=4096,
        method_timeout=timedelta(minutes=2),
        update_after=timedelta(minutes=60),
        expire_after=timedelta(minutes=120),
    )
)  # type: ignore
async def twitch_cheermotes_cached(
    broadcaster_id: str | None = None,
) -> dict[str, CheermoteTier]:
    cheermotes = await twitch_cheermotes(broadcaster_id)
    result: dict[str, CheermoteTier] = {}
    for c in cheermotes:
        for tier in c.tiers:
            result[f'{c.prefix}-{tier.id}'] = tier
    return result


async def twitch_cheermotes(broadcaster_id: str | None = None) -> list[Cheermote]:
    response = await twitch_app_client.get(
        '/bits/cheermotes',
        params={
            'broadcaster_id': broadcaster_id,
        },
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    data = CheermoteResponse.model_validate(response.json())
    return data.data
