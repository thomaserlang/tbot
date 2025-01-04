from uuid import UUID

from tbot2.spotify.schemas.spotify_schema import (
    SpotifyCurrentlyPlaying,
    SpotifyCursorPaging,
    SpotifyPlaylist,
)

from ..http_client import spotify_client


async def get_spotify_currently_playing(
    *,
    channel_id: UUID,
):
    repsonse = await spotify_client.get(
        '/me/player/currently-playing',
        headers={
            'X-Channel-Id': str(channel_id),
        },
    )
    repsonse.raise_for_status()

    data = SpotifyCurrentlyPlaying.model_validate(repsonse.json())
    return data


async def get_spotify_recently_played(
    *,
    channel_id: UUID,
):
    repsonse = await spotify_client.get(
        '/me/player/recently-played',
        headers={
            'X-Channel-Id': str(channel_id),
        },
    )
    repsonse.raise_for_status()
    data = SpotifyCursorPaging.model_validate(repsonse.json())
    return data.items


async def get_spotify_playlist(*, channel_id: UUID, playlist_url: str):
    response = await spotify_client.get(
        f'{playlist_url}',
        headers={
            'X-Channel-Id': str(channel_id),
        },
    )
    response.raise_for_status()
    data = SpotifyPlaylist.model_validate(response.json())
    return data
