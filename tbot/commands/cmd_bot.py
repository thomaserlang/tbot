import logging
from tbot.command import command, cmds
from tbot import utils
from datetime import datetime

@command('__thebotname')
async def cmd_bot(client, nick, channel, target, args, **kwargs):
    if len(args) == 0:
        m = []
        for c in cmds:
            if c['cmd'].startswith('_'):
                continue
            a = '!{}'.format(c['cmd'])
            if c['alias']:
                a += ' (!{})'.format(c['alias'])
            m.append(a)
        client.send("PRIVMSG", target=target, 
            message='@{}, Commands: {}'.format(
                kwargs['display-name'], ', '.join(m)
            )
        )
        return
        
    if args[0].lower() == 'uptime':
        seconds = (datetime.utcnow() - client.starttime).total_seconds()
        msg = 'I\'ve been up for {}'.format(utils.seconds_to_pretty(seconds))
        client.send("PRIVMSG", target=target, message=msg)

