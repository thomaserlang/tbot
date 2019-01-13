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
        return '{} seconds'.format(seconds)

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    ts = []
    if days:
        ts.append(pluralize(days, 'day'))
    if hours:
        ts.append(pluralize(hours, 'hour'))
    if minutes:        
        ts.append(pluralize(minutes, 'min'))
    return ' '.join(ts)

async def twitch_request(ahttp, url, params=None, headers={}):    
    headers.update({
        'Authorization': 'Bearer {}'.format(config['twitch']['token'])
    })
    async with ahttp.get(url, params=params, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            return data
        if r.status == 415:
            w = int(time.time())-int(r.headers['Ratelimit-Reset'])
            if w > 0:
                await asyncio.sleep(w)
            return await twitch_request(ahttp, url, params, headers)
        if r.status >= 400:
            error = await r.text()
            raise Exception('Error: {} - {}'.format(r.status, error))

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
    if not re.match('^[a-z0-9A-Z]+$', cmd):
        raise Exception('The command must only contain: a-z 0-9')
    return True

def validate_cmd_response(response):
    if not (1 <= len(response) <= 500):
        raise Exception('The response must be between 1 and 500 chars')
    if response[0] == '!':
        raise Exception('The response must not start with a !, use alias to trigger another command')
    return True