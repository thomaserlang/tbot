from tbot import config

def seconds_to_pretty(seconds):
    seconds = round(seconds)
    if seconds < 60:
        return '{} seconds'.format(seconds)

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    ts = []
    if hours == 1:
        ts.append('1 hour')
    elif hours > 1:
        ts.append('{} hours'.format(hours))
    if minutes == 1:
        ts.append('1 min')
    elif minutes > 1:
        ts.append('{} mins'.format(minutes))

    return ' '.join(ts)

async def twitch_request(http_session, url, params=None, headers={}):    
    headers.update({
        'Authorization': 'Bearer {}'.format(config['token'])
    })
    async with http_session.get(url, params=params, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            return data

async def twitch_lookup_usernames(http_session, usernames):
    url = 'https://api.twitch.tv/helix/users'
    params = [('login', name) for name in usernames]
    data = await twitch_request(http_session, url, params)
    if data:
        users = []
        for d in data['data']:
            users.append({'id': d['id'], 'user': d['login']})
        return users

async def twitch_lookup_user_id(http_session, username):
    users = await twitch_lookup_usernames(http_session, [username])
    if not users:
        return
    return users[0]['id']