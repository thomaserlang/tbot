import logging
import asyncio
import re
from tbot import config, utils

var_fillers = {}

def fills_vars(*vars):
    def wrapper(f):
        if not asyncio.iscoroutinefunction(f):
            raise Exception('The method must be async')
        for var in vars:
            var_fillers[var] = f
        return f
    return wrapper

async def fill_message(message, **kwargs):
    parsed = parse(message)
    grouped = {}
    for p in parsed:
        if p['var'] in var_fillers:
            l = grouped.setdefault(var_fillers[p['var']], [])
            l.append(p)
    for f in grouped:
        var_args = {p['var']: p['args'] for p in grouped[f]}
        r = await f(var_args=var_args, **kwargs)
        if r:
            for p in grouped[f]:
                if p['var'] in r:
                    p['value'] = r[p['var']]
    return format_response(message, parsed)

def parse(s):
    matched = re.findall(r'\{([a-z0-9]+[ ]?.*?)\}', s, flags=re.IGNORECASE)
    l = []
    for m in matched:
        b = m.split(' ', 1)
        var = b[0]
        args = utils.split(b[1]) if len(b) > 1 else []
        l.append({
            'matched': m,
            'var': var,
            'args': args,
            'value': None,
        })
    return l

def format_response(s, values):
    for v in values:
        if v['value'] != None:
            s = s.replace('{'+v['matched']+'}', str(v['value']))
    return s

def fill_from_dict(s, d):
    for k in d:
        s = s.replace('{'+k+'}', str(d[k]))
    return s

class Send_error(Exception):

    def __init__(self, message, user=None):
        self.user = user
        super().__init__(message)

class Send(Exception):
    def __init__(self, message, user=None):
        self.user = user
        super().__init__(message)

class Send_break(Exception):
    pass