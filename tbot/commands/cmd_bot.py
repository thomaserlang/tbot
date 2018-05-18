from tbot import utils

async def cmd_bot(client, nick, channel, target, args, **kwargs):
    if len(args) == 0:
        client.send("PRIVMSG", target=target, 
            message='@{}, Commands: !streamwatchtime (!swt), !betteruptime'.format(kwargs['display-name']))
        return

    if args[0].lower() == 'uptime':
        seconds = (datetime.utcnow() - client.starttime).total_seconds()
        msg = 'I\'ve been up for {}'.format(utils.seconds_to_pretty(seconds))
        client.send("PRIVMSG", target=target, message=msg)

