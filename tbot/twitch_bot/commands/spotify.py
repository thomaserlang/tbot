import logging
from tbot.twitch_bot.command import command
from tbot import config, utils

@command('spotifysong', alias='ssong')
async def spotify_song(bot, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    if len(args) > 0:
        user = utils.safe_username(args[0])

    if not bot.channels[channel_id]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        bot.send("PRIVMSG", target=target, message=msg)
        return

    data = await request(bot, channel_id, 'https://api.spotify.com/v1/me/player/currently-playing')
    if data == None:
        return
    if not data or not data['is_playing']:
        msg = '{}, Spotify is currently not playing'.format(user)
        bot.send("PRIVMSG", target=target, message=msg)
        return
    artists = [r['name'] for r in data['item']['artists']]
    duration = '{}:{}'.format(*divmod(round(data['item']['duration_ms']/1000), 60))
    progress = '{}:{}'.format(*divmod(round(data['progress_ms']/1000), 60))
    msg = '{}, Playing: {} by {} ({}/{})'.format(
        user,
        data['item']['name'],
        ', '.join(artists),
        progress,
        duration,
    )
    bot.send("PRIVMSG", target=target, message=msg)

@command('spotifyplaylist', alias='splaylist')
async def spotify_playlist(bot, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    if len(args) > 0:
        user = utils.safe_username(args[0])

    if not bot.channels[channel_id]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        bot.send("PRIVMSG", target=target, message=msg)
        return

    data = await request(bot, channel_id, 'https://api.spotify.com/v1/me/player/currently-playing')
    if data == None:
        return
    if not data or not data['is_playing']:
        msg = '{}, Spotify is currently not playing'.format(user)
        bot.send("PRIVMSG", target=target, message=msg)
        return
    
    playlist = await request(bot, channel_id, data['context']['href'])
    playlistname = ''
    if playlist:
        playlistname = playlist['name']
    
    msg = '{}, Current playlist: {} - {}'.format(
        user,
        playlistname,
        data['context']['external_urls']['spotify'],
    )
    bot.send("PRIVMSG", target=target, message=msg)

@command('spotifyprevsong', alias='sprevsong')
async def spotify_prev_song(bot, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    if len(args) > 0:
        user = utils.safe_username(args[0])

    if not bot.channels[channel_id]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        bot.send("PRIVMSG", target=target, message=msg)
        return
    
    data = await request(bot, channel_id, 'https://api.spotify.com/v1/me/player/recently-played?limit=1')
    if data == None:
        return
    if not data or not data['items']:
        msg = '{}, No previous songs played on Spotify'.format(user)
        bot.send("PRIVMSG", target=target, message=msg)
        return
    data = data['items'][0]
    artists = [r['name'] for r in data['track']['artists']]
    msg = '{}, Previous song: {} by {}'.format(
        user,
        data['track']['name'],
        ', '.join(artists),
    )
    bot.send("PRIVMSG", target=target, message=msg)

async def request(bot, channel_id, url, params=None, headers={}):    
    t = await bot.db.fetchone('SELECT * FROM spotify WHERE channel_id=%s;', (channel_id))
    if not t:
        return
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
        raise Exception('Spotify request error {}: {}'.format(
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
            logging.info(data)
            await bot.db.execute(
                'UPDATE spotify SET token=%s WHERE channel_id=%s;',
                (data['access_token'], channel_id)
            )
            if 'refresh_token' in data:
                await bot.db.execute(
                    'UPDATE spotify SET refresh_token=%s WHERE channel_id=%s;',
                    (data['refresh_token'], channel_id)
                )
        else:
            error = await r.text()
            raise Exception('Failed to refresh token for channel_id: {} - Error: {}: {}'.format(
                channel_id,
                r.status,
                error,
            ))