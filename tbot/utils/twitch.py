import datetime, time, asyncio, re
from tbot import config, logger
from .base import chunks

twitch_app_token = None

class Twitch_request_error(Exception):

    def __init__(self, message, status_code):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

async def twitch_request(ahttp, url, params=None, headers={}, 
    method='GET', data=None, json=None, token=None, raise_exception=True):
    if not token:
        token = await twitch_get_app_token(ahttp)
    headers.update({
        'Client-ID': config.data.twitch.client_id,
        'Authorization': 'Bearer {}'.format(token)
    })
    async with ahttp.request(method, url, params=params, 
        headers=headers, data=data, json=json) as r:
        if r.status == 415:
            w = int(time.time())-int(r.headers['Ratelimit-Reset'])
            if w > 0:
                await asyncio.sleep(w)
            return await twitch_request(ahttp, url, params, headers, method, data, json)
        if r.status == 401:
            if 'WWW-Authenticate' in r.headers:
                if 'invalid_token' in r.headers['WWW-Authenticate']:
                    reset_app_token()
                    return await twitch_request(ahttp, url, params, headers, method, data, json)
            d = await r.json()
            if raise_exception:
                raise Twitch_request_error(d['message'], r.status)
            else:
                logger.error(d)
        if r.status >= 400:
            error = await r.json()
            if raise_exception:
                raise Twitch_request_error(error['message'], r.status)
            else:
                logger.error(error)
        if 'Content-Type' in r.headers:
            if 'application/json' in r.headers['Content-Type']:
                return await r.json()
        return await r.text()

async def twitch_get_app_token(ahttp):
    global twitch_app_token
    if twitch_app_token:
        return twitch_app_token
    params = {
        'client_id': config.data.twitch.client_id,
        'client_secret': config.data.twitch.client_secret,
        'grant_type': 'client_credentials',
    }
    async with ahttp.request('POST', 'https://id.twitch.tv/oauth2/token', params=params) as r:
        if r.status >= 400:
            error = await r.text()
            raise Twitch_request_error('{}: {}'.format(r.status, error), r.status)
        d = await r.json()
        twitch_app_token = d['access_token']
        return d['access_token']

async def reset_app_token():
    global twitch_app_token
    twitch_app_token = None

async def twitch_channel_token_request(bot, channel_id, url, method='GET', 
    params=None, headers={}, data=None, json=None):
    channel = await bot.db.fetchone(
        'SELECT twitch_token, twitch_refresh_token FROM twitch_channels WHERE channel_id=%s',
        (channel_id,)
    )
    if not channel:
        raise Exception(f'Unknown channel {channel_id}')
    if not channel['twitch_token'] or not channel['twitch_refresh_token']:
        raise Twitch_request_error(
            'Extra authorization is needed, please sign in to the dashboard and '
            'grant the bot extra authorization',
            400
        )
    try:
        d = await twitch_request(
            bot.ahttp, url=url, params=params, headers=headers,
            method=method, data=data, json=json, token=channel['twitch_token'],
        )
        return d
    except Twitch_request_error as e:
        if e.status_code == 401:
            token = await twitch_refresh_token(
                bot, 
                channel_id, 
                channel['twitch_refresh_token'],
            )
            d = await twitch_request(
                bot.ahttp, url=url, params=params, headers=headers,
                method=method, data=data, json=json, token=token,
            )
            return d
        else:
            raise

async def twitch_refresh_token(bot, channel_id, refresh_token):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': config.data.twitch.client_id,
        'client_secret': config.data.twitch.client_secret,
    }
    async with bot.ahttp.post(url, params=params) as r:
        if r.status == 200:
            data = await r.json()
            await bot.db.execute(
                'UPDATE twitch_channels SET twitch_token=%s, twitch_refresh_token=%s WHERE channel_id=%s;',
                (data['access_token'], data['refresh_token'], channel_id)
            )
            return data['access_token']
        else:
            if r.status == 400:
                await bot.db.execute(
                    'UPDATE twitch_channels SET twitch_token=null, twitch_refresh_token=null WHERE channel_id=%s;',
                    (channel_id,)
                )
                raise Twitch_request_error(
                    'Extra authorization is needed, please sign in to the dashboard and '
                    'grant the bot extra authorization',
                    400
                )
            error = await r.text()
            raise Twitch_request_error('{}: {}'.format(
                r.status,
                error,
            ), r.status)

async def twitch_lookup_usernames(ahttp, db, usernames):
    '''
    :returns: List[Dict[{'user': str, 'id': str}]]
    '''
    users = []
    now = datetime.datetime.utcnow()
    m1 = now + datetime.timedelta(days=30)
    usernames = [s.lower() for s in set(usernames)]
    for unames in chunks(list(usernames), 5000):
        rs = await db.fetchall(
            'SELECT user_id as id, user FROM twitch_usernames WHERE expires > %s AND user IN ({})'.format(
                ','.join(['%s'] * len(unames))),
            (now, *unames)
        )
        for r in rs:
            usernames.remove(r['user'])
            users.append(r)

    url = 'https://api.twitch.tv/helix/users'
    if usernames:
        users_to_save = []
        for unames in chunks(usernames, 100):
            params = [('login', name) for name in unames]
            params.append(('first', '100'))
            data = await twitch_request(ahttp, url, params)
            if data:
                for d in data['data']:
                    users.append({'id': d['id'], 'user': d['login']})
                    users_to_save.append((d['id'], d['login'], m1))
        await db.executemany('''
            INSERT INTO twitch_usernames (user_id, user, expires) 
            VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE user=VALUES(user), expires=VALUES(expires)
        ''', users_to_save)
    return users

async def twitch_lookup_user_id(ahttp, db, username):
    if not re.match('^[a-z0-9A-Z_]{4,25}$', username):
        return
    users = await twitch_lookup_usernames(ahttp, db, [username])
    if not users:
        return
    return users[0]['id']


async def twitch_lookup_from_user_id(ahttp, db, userids):
    '''
    :returns: List[Dict[{'user': str, 'id': str}]]
    '''
    users = []
    now = datetime.datetime.utcnow()
    m1 = now + datetime.timedelta(days=30)
    userids = [s for s in set(userids)]
    for uids in chunks(list(userids), 5000):
        rs = await db.fetchall(
            'SELECT user_id as id, user FROM twitch_usernames WHERE expires > %s AND user_id IN ({})'.format(
                ','.join(['%s'] * len(uids))),
            (now, *uids)
        )
        for r in rs:
            userids.remove(r['id'])
            users.append(r)

    url = 'https://api.twitch.tv/helix/users'
    if userids:
        users_to_save = []
        for uids in chunks(userids, 100):
            params = [('id', id_) for id_ in uids]
            params.append(('first', '100'))
            data = await twitch_request(ahttp, url, params)
            if data:
                for d in data['data']:
                    users.append({'id': d['id'], 'user': d['login']})
                    users_to_save.append((d['id'], d['login'], m1))
        await db.executemany('''
            INSERT INTO twitch_usernames (user_id, user, expires) 
            VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE user=VALUES(user), expires=VALUES(expires)
        ''', users_to_save)
    return users

async def twitch_current_user(ahttp, token=None):
    data = await twitch_request(
        ahttp, 
        f'https://api.twitch.tv/helix/users?login={config.data.twitch.username}', 
        token=token,
    )
    return data['data'][0]

def twitch_remove_emotes(message, emotes):
    if not emotes:
        return message
    l = []
    for emote in emotes.split('/'):
        for pos in emote.split(':')[1].split(','):
            p = pos.split('-')
            l.append((int(p[0]), int(p[1])+1))
    i = 0
    l = sorted(l, key=lambda x: x[0])
    for e in l:
        o = len(message)
        message = message[:e[0]-i] + message[e[1]-i:].strip()
        i += o - len(message)
    return message.strip()


async def twitch_save_mods(bot, channel_id):
    after = ''
    user_ids = []
    try:
        while True:
            r = await twitch_channel_token_request(
                bot=bot,
                channel_id=channel_id,
                url='https://api.twitch.tv/helix/moderation/moderators',
                params={
                    'broadcaster_id': channel_id,
                    'first': 100,
                    'after': after,
                }
            )
            if r.get('data'):
                for user in r['data']:
                    if user['user_id'] in user_ids:
                        continue
                    user_ids.append(user['user_id'])
            else:
                break
            if not r.get('pagination'):
                break
            after = r['pagination']['cursor']

        mods = await bot.db.fetchall('SELECT user_id FROM twitch_channel_mods WHERE channel_id=%s', (channel_id,))
        for mod in mods:
            if mod['user_id'] in user_ids:
                user_ids.remove(mod['user_id'])
            else:
                await bot.db.execute('DELETE FROM twitch_channel_mods where channel_id=%s and user_id=%s ', 
                    (channel_id, mod['user_id'],)
                )
        if user_ids:
            await bot.db.executemany(
                'INSERT IGNORE INTO twitch_channel_mods (channel_id, user_id) VALUES (%s, %s);', 
                [(channel_id, user_id) for user_id in user_ids]
            )
    except Twitch_request_error as e:
        if e.status_code >= 500:
            logger.exception('save_mods')
        else:
            logger.debug(e.message)
    except Exception:
        logger.exception('save_mods')