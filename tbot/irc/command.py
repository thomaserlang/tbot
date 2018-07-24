import logging
import asyncio
import functools
from tbot import config
from tbot.irc import bot

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

@bot.on('PRIVMSG')
def handle_command(nick, target, message, **kwargs):
    if not message.startswith('!'):
        return    
    args = message.split(' ')
    cmd = args.pop(0).lower().strip('!')
    if cmd == config['user'].lower():
        cmd = '__thebotname'
    if cmd in _cmd_lookup:
        f = _cmd_lookup[cmd]['func']
        bot.loop.create_task(f(
            bot=bot,
            nick=nick,
            channel=target.strip('#'),
            channel_id=int(kwargs['room-id']),
            target=target,
            message=message,
            args=args,
            **kwargs
        ))