from tbot.twitch_bot.tasks.command import command
from tbot import utils, constants
from datetime import datetime

@command('__thebotname', alias='commands')
async def cmd_bot(bot, nick, channel, channel_id, target, args, **kwargs):
    if len(args) == 0:
        return    
    elif args[0].lower() == 'uptime':
        seconds = (datetime.utcnow() - bot.starttime).total_seconds()
        msg = '@{}, I\'ve been up for {}'.format(
            kwargs['display-name'],
            utils.seconds_to_pretty(seconds)
        )
        bot.send("PRIVMSG", target=target, message=msg)

    elif args[0].lower() == 'version':
        msg = '@{}, I\'m running version {}'.format(
            kwargs['display-name'],
            constants.VERSION,
        )
        bot.send("PRIVMSG", target=target, message=msg)

    elif args[0].lower() == 'time':
        msg = '@{}, My time is {}Z'.format(
            kwargs['display-name'],
            datetime.utcnow().replace(microsecond=0).isoformat(),
        )
        bot.send("PRIVMSG", target=target, message=msg)
