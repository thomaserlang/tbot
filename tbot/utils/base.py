import logging
import re, json, datetime, time
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
        return pluralize(seconds, 'second')

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
        ts.append(pluralize(minutes, 'minute'))
    if seconds:        
        ts.append(pluralize(seconds, 'second'))
    if len(ts) > 2 and seconds:
        ts.pop(len(ts)-1)
    ts = ts[:3]
    logging.info(ts)
    if len(ts) >= 2:
        last = ts.pop(len(ts)-1)
        s = ', '.join(ts)
        s += ' and {}'.format(last)
        return s
    return ts[0]

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