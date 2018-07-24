from tbot.irc.command import command
from tbot import utils
from datetime import datetime

@command('streamuptime', alias='sup')
async def stream_uptime(bot, nick, channel, channel_id, target, args, **kwargs):
    if not bot.channels[channel_id]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        bot.send("PRIVMSG", target=target, message=msg)
        return

    if not bot.channels[channel_id]['went_live_at']:
        msg = '@{}, the stream start time is unknown to me'.format(kwargs['display-name'])
        bot.send("PRIVMSG", target=target, message=msg)
        return

    msg = 'This stream has been live for {}'.format(utils.seconds_to_pretty(
        bot.channels[channel_id]['uptime']
    ))
    bot.send("PRIVMSG", target=target, message=msg)