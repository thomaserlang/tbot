import asyncio, re
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

async def fill_message(text, **kwargs):
    parsed = parse(text)
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
    return format_response(text, parsed)

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

class Send_error(Exception):
    pass

class Send(Exception):
    pass

class Send_break(Exception):
    pass