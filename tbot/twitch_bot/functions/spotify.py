import logging
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils, config

@fills_vars('spotify.song_name', 'spotify.song_artists', 'spotify.song_progress', 'spotify.song_duration')
async def song(bot, channel_id, **kwargs):
    data = await request(bot, channel_id, 'https://api.spotify.com/v1/me/player/currently-playing')
    if data == None:
        raise Send_error('ERROR: Spotify failed to load')
    if not data or not data['is_playing']:
        raise Send_error('Spotify is not playing')
    artists = [r['name'] for r in data['item']['artists']]
    duration = '{}:{:02d}'.format(*divmod(round(data['item']['duration_ms']/1000), 60))
    progress = '{}:{:02d}'.format(*divmod(round(data['progress_ms']/1000), 60))
    return {
        'spotify.song_name': data['item']['name'],
        'spotify.song_artists': ', '.join(artists),
        'spotify.song_progress': progress,
        'spotify.song_duration': duration,
    }

@fills_vars('spotify.playlist_name', 'spotify.playlist_url')
async def playlist(bot, channel_id, **kwargs):
    data = await request(bot, channel_id, 'https://api.spotify.com/v1/me/player/currently-playing')
    if data == None:
        raise Send_error('ERROR: Spotify failed to load')
    if not data or not data['is_playing']:
        raise Send_error('Spotify is not playing')
    
    playlist = await request(bot, channel_id, data['context']['href'])
    playlistname = ''
    if playlist:
        playlistname = playlist['name']
    
    return {
        'spotify.playlist_name': playlistname,
        'spotify.playlist_url': data['context']['external_urls']['spotify'],
    }

@fills_vars('spotify.prev_song_name', 'spotify.prev_song_artists')
async def prev_song(bot, channel_id, args, **kwargs):
    num = utils.find_int(args) or 1
    if num > 10:
        raise Send_error('Only allowed to go back 10 songs')
    data = await request(bot, channel_id, 'https://api.spotify.com/v1/me/player/recently-played?limit={}'.format(num))
    if data == None:
        raise Send_error('ERROR: Spotify failed to load')
    if 'items' not in data or not data['items']:
        raise Send_error('No previous song found')
    if num > len(data['items']):
        raise Send_error('No previous song found')
    data = data['items'][num-1]
    artists = [r['name'] for r in data['track']['artists']]
    return {
        'spotify.prev_song_name': data['track']['name'],
        'spotify.prev_song_artists': ', '.join(artists),
    }

async def request(bot, channel_id, url, params=None, headers={}):    
    t = await bot.db.fetchone('SELECT * FROM twitch_spotify WHERE channel_id=%s;', (channel_id))
    if not t:
        raise Send_error('ERROR: Spotify has not been configured for this channel')
    headers.update({
        'Authorization': 'Bearer {}'.format(t['token'])
    })
    async with bot.ahttp.get(url, params=params, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            return data
        elif r.status == 204:
            return {}
        elif r.status == 401:
            await refresh_token(bot, channel_id, t['refresh_token'])
            return await request(bot, channel_id, url, params, headers)
        error = await r.text()
        raise Send_error('ERROR: Spotify request error {}: {}'.format(
            r.status,
            error,
        ))

async def refresh_token(bot, channel_id, refresh_token):
    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': config['spotify']['client_id'],
        'client_secret': config['spotify']['client_secret'],
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    async with bot.ahttp.post(url, params=body, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            await bot.db.execute(
                'UPDATE twitch_spotify SET token=%s WHERE channel_id=%s;',
                (data['access_token'], channel_id)
            )
            if 'refresh_token' in data:
                await bot.db.execute(
                    'UPDATE twitch_spotify SET refresh_token=%s WHERE channel_id=%s;',
                    (data['refresh_token'], channel_id)
                )
        else:
            raise Send_error('ERROR: Soptify needs to be reauthorized')