from uuid import UUID

from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage
from tbot2.spotify.schemas.spotify_schema import (
    SpotifyCurrentlyPlaying,
    SpotifyCursorPaging,
    SpotifyPlaylist,
)

from ..spotify_http_client import spotify_client


async def get_spotify_currently_playing(
    *,
    channel_id: UUID,
):
    response = await spotify_client.get(
        '/me/player/currently-playing',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')

    data = SpotifyCurrentlyPlaying.model_validate(response.json())
    return data


async def get_spotify_recently_played(
    *,
    channel_id: UUID,
):
    response = await spotify_client.get(
        '/me/player/recently-played',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')

    data = SpotifyCursorPaging.model_validate(response.json())
    return data.items


async def get_spotify_playlist(*, channel_id: UUID, playlist_url: str):
    response = await spotify_client.get(
        f'{playlist_url}',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    data = SpotifyPlaylist.model_validate(response.json())
    return data
