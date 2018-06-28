from tbot.command import command, cmds
from tbot import utils, constants
from datetime import datetime

@command('__thebotname')
async def cmd_bot(client, nick, channel, channel_id, target, args, **kwargs):
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
    
    elif args[0].lower() == 'uptime':
        seconds = (datetime.utcnow() - client.starttime).total_seconds()
        msg = '@{}, I\'ve been up for {}'.format(
            kwargs['display-name'],
            utils.seconds_to_pretty(seconds)
        )
        client.send("PRIVMSG", target=target, message=msg)

    elif args[0].lower() == 'version':
        msg = '@{}, I\'m running version {}'.format(
            kwargs['display-name'],
            constants.VERSION,
        )
        client.send("PRIVMSG", target=target, message=msg)

    elif args[0].lower() == 'time':
        msg = '@{}, My time is {}Z'.format(
            kwargs['display-name'],
            datetime.utcnow().replace(microsecond=0).isoformat(),
        )
        client.send("PRIVMSG", target=target, message=msg)
