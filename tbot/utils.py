import logging
import re, json, datetime
from tbot import config

def safe_username(user):
    return re.sub('[^a-zA-Z0-9_]', '', user)[:25]

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

_cached_user_ids = {}
async def twitch_lookup_usernames(ahttp, usernames):
    global _cached_user_ids
    url = 'https://api.twitch.tv/helix/users'
    users = []
    lookup_usernames = list(usernames)
    for u in usernames:
        ul = u.lower()
        if ul in _cached_user_ids:
            lookup_usernames.remove(u)
            users.append({
                'id': _cached_user_ids[ul],
                'user': ul, 
            })
    if lookup_usernames:
        for unames in chunks(lookup_usernames, 100):
            params = [('login', name) for name in unames]
            data = await twitch_request(ahttp, url, params)
            if data:
                for d in data['data']:
                    _cached_user_ids[d['login'].lower()] = d['id']
                    users.append({'id': d['id'], 'user': d['login']})
    return users

async def twitch_lookup_user_id(ahttp, username):
    users = await twitch_lookup_usernames(ahttp, [username])
    if not users:
        return
    return users[0]['id']

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