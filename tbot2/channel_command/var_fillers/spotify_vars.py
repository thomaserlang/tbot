from tbot2.common import ChatMessage
from tbot2.exceptions import ErrorMessage
from tbot2.spotify import (
    get_spotify_currently_playing,
    get_spotify_playlist,
    get_spotify_recently_played,
)

from ..exceptions import CommandError
from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=(
        'spotify.song_name',
        'spotify.song_artists',
        'spotify.song_progress',
        'spotify.song_duration',
    ),
)
async def spotify_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    try:
        playing = await get_spotify_currently_playing(
            channel_id=chat_message.channel_id,
        )
    except ErrorMessage as e:
        raise CommandError(e) from e

    if not playing or not playing.is_playing or not playing.item:
        raise CommandError('Spotify is not playing')

    vars['spotify.song_name'].value = playing.item.name
    vars['spotify.song_artists'].value = ', '.join(a.name for a in playing.item.artists)
    vars['spotify.song_progress'].value = '{}:{:02d}'.format(
        *divmod(round((playing.progress_ms or 0) / 1000), 60)
    )
    vars['spotify.song_duration'].value = '{}:{:02d}'.format(
        *divmod(round(playing.item.duration_ms / 1000), 60)
    )


@fills_vars(
    provider='all',
    vars=(
        'spotify.playlist_name',
        'spotify.playlist_url',
    ),
)
async def spotify_playlist_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    try:
        playing = await get_spotify_currently_playing(
            channel_id=chat_message.channel_id,
        )
    except ValueError as e:
        raise ErrorMessage(e) from e

    if not playing or not playing.is_playing:
        raise CommandError('Spotify is not playing')

    if not playing.context:
        raise CommandError('No playlist found')

    if not playing.context.href:
        raise CommandError('No playlist found')

    if not playing.context.type == 'playlist':
        raise CommandError('Is currently not playing a playlist')

    try:
        playlist = await get_spotify_playlist(
            channel_id=chat_message.channel_id,
            playlist_url=playing.context.href,
        )
    except ErrorMessage as e:
        raise CommandError(e) from e

    vars['spotify.playlist_name'].value = playlist.name
    vars['spotify.playlist_url'].value = playlist.external_urls.spotify


@fills_vars(
    provider='all',
    vars=(
        'spotify.prev_song_name',
        'spotify.prev_song_artists',
    ),
)
async def spotify_prev_song_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    try:
        played = await get_spotify_recently_played(
            channel_id=chat_message.channel_id,
        )
    except ErrorMessage as e:
        raise CommandError('Spotify is unavailable') from e

    if not played:
        raise CommandError('No previous song found')

    num = int(command.args[0]) if command.args and command.args[0].isdigit() else 1
    if num > 10:
        raise CommandError('Only allowed to go back 10 songs')

    if len(played) < num:
        raise CommandError('No previous song found')

    prev_song = played[num - 1]
    vars['spotify.prev_song_name'].value = prev_song.track.name
    vars['spotify.prev_song_artists'].value = ', '.join(
        a.name for a in prev_song.track.artists
    )
