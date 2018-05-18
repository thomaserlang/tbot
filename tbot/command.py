import asyncio
import functools
from tbot import config

cmds = []
_cmd_lookup = {}

def command(cmd, alias=None, arg_desc=None):
    def wrapper(f):
        wrapped = f
        if not asyncio.iscoroutinefunction(wrapped):
            wrapped = asyncio.coroutine(wrapped)
        d = {
            'func': wrapped,
            'cmd': cmd,
            'alias': alias,
            'arg_desc': arg_desc,
        }
        cmds.append(d)
        _cmd_lookup[cmd] = d
        if alias:
            _cmd_lookup[alias] = d
    return wrapper

def handle_command(client, nick, target, message, **kwargs):
    if not message.startswith('!'):
        return    
    args = message.split(' ')
    cmd = args.pop(0).lower().strip('!')
    if cmd == config['user'].lower():
        cmd = '__thebotname'
    if cmd in _cmd_lookup:
        f = _cmd_lookup[cmd]['func']
        client.loop.create_task(f(
            client=client,
            nick=nick,
            channel=target.strip('#'), 
            target=target,
            message=message,
            args=args,
            **kwargs
        ))