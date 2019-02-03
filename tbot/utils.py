import logging
import re, json, datetime, time, asyncio
from typing import List, Optional
from tbot import config

def safe_username(user):
    return re.sub('[^a-zA-Z0-9_]', '', user)[:25]

def find_int(l: List[str]) -> Optional[int]:
    for a in l:
        try:
            return int(a)
        except ValueError:
            pass
    return None

def seconds_to_pretty(seconds):
    seconds = round(seconds)
    if seconds < 60:
        return pluralize(seconds, 'sec')

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)

    ts = []
    if years:
        ts.append(pluralize(years, 'year'))
    if months:
        ts.append(pluralize(months, 'month'))
    if days:
        ts.append(pluralize(days, 'day'))
    if hours:
        ts.append(pluralize(hours, 'hour'))
    if minutes:        
        ts.append(pluralize(minutes, 'min'))
    if seconds:        
        ts.append(pluralize(seconds, 'sec'))
    if len(ts) > 2 and seconds:
        ts.pop(len(ts)-1)
    if len(ts) > 4 and minutes:
        ts.pop(len(ts)-1)
    return ' '.join(ts)

class Twitch_request_error(Exception):

    def __init__(self, message, status_code):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

async def twitch_request(ahttp, url, params=None, headers={}, 
    method='GET', data=None, json=None, token=None):
    if not token:
        token = config['twitch']['token']
    if '/kraken/' in url:
        headers.update({
            'Client-ID': config['twitch']['client_id'],
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': 'OAuth {}'.format(token)
        })
        if data:
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
            })
    else:
        headers.update({
            'Authorization': 'Bearer {}'.format(token)
        })
    async with ahttp.request(method, url, params=params, 
        headers=headers, data=data, json=json) as r:
        if r.status == 415:
            w = int(time.time())-int(r.headers['Ratelimit-Reset'])
            if w > 0:
                await asyncio.sleep(w)
            return await twitch_request(ahttp, url, params, headers, method, data, json)
        if r.status >= 400:
            error = await r.text()
            raise Twitch_request_error('{}: {}'.format(r.status, error), r.status)
        if 'Content-Type' in r.headers:
            if r.headers['Content-Type'] == 'application/json':
                return await r.json()
        return await r.text()

async def twitch_channel_token_request(bot, channel_id, url, method='GET', 
    params=None, headers={}, data=None, json=None):
    channel = await bot.db.fetchone(
        'SELECT twitch_token, twitch_refresh_token FROM twitch_channels WHERE channel_id=%s',
        (channel_id,)
    )
    if not channel:
        raise Exception('Unknown channel {}'.format(channel_id))
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
        'client_id': config['twitch']['client_id'],
        'client_secret': config['twitch']['client_secret'],
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
    users = []
    now = datetime.datetime.utcnow()
    m1 = now + datetime.timedelta(days=30)
    usernames = [s.lower() for s in usernames]
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

async def twitch_current_user(ahttp):
    data = await twitch_request(ahttp, 'https://api.twitch.tv/helix/users')
    return data['data'][0]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def pluralize(num, word):
    if num != 1:
        word += 's'
    return '{} {}'.format(num, word)


def isoformat(dt):
    r = dt.isoformat()
    if isinstance(dt, datetime.datetime) and not dt.tzinfo:
        r += 'Z'
    return r

class JsonEncoder(json.JSONEncoder):
    def default(self, value):
        """Convert more Python data types to ES-understandable JSON."""
        if isinstance(value, (datetime.datetime, datetime.time)):
            return isoformat(value)
        elif isinstance(value, datetime.date):
            return value.isoformat()
        if isinstance(value, set):
            return list(value)
        if isinstance(value, bytes):
            return value.decode('utf-8')
        return super().default(value)

def json_dumps(obj, **kwargs):
    return json.dumps(
        obj,
        cls=JsonEncoder,
        **kwargs
    ).replace("</", "<\\/")

def json_loads(s, charset='utf-8'):
    if isinstance(s, bytes):
        s = s.decode(charset)
    return json.loads(s)

def validate_cmd(cmd):
    if not (1 <= len(cmd) <= 20):
        raise Exception('The command must be between 1 and 20 chars')
    if not re.match('^[a-z0-9A-Z_]+$', cmd):
        raise Exception('The command must only contain: a-z, 0-9 and _')
    return True

def validate_cmd_response(response):
    if not (1 <= len(response) <= 500):
        raise Exception('The response must be between 1 and 500 chars')
    if response[0] == '!':
        raise Exception('The response must not start with a !, use alias to trigger another command')
    return True