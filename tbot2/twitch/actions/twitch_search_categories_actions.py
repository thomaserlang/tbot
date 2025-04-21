from tbot2.exceptions import InternalHttpError

from ..schemas.twitch_game_schema import Game, SearchCategoryResult
from ..twitch_http_client import twitch_app_client


async def get_twitch_game(
    name: str,
) -> Game | None:
    response = await twitch_app_client.get(
        url='/games',
        params={
            'name': name,
        },
    )
    if response.status_code >= 400:
        raise InternalHttpError(
            status_code=response.status_code,
            body=f'{response.text}',
        )
    data = response.json()
    if not data['data']:
        return None
    return Game.model_validate(data['data'][0])


async def search_twitch_categories(
    query: str,
) -> list[SearchCategoryResult]:
    response = await twitch_app_client.get(
        url='/search/categories',
        params={
            'query': query,
        },
    )
    if response.status_code >= 400:
        raise InternalHttpError(
            status_code=response.status_code,
            body=f'{response.text}',
        )
    data = response.json()
    return [SearchCategoryResult.model_validate(item) for item in data['data']]
