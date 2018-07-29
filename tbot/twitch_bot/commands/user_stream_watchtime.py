import logging
from datetime import datetime
from tbot.twitch_bot.command import command
from tbot import utils

@command('streamwatchtime', alias='swt')
async def user_stream_watchtime(bot, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    user_id = kwargs['user-id']
    if len(args) > 0:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, user)

    if not bot.channels[channel_id]['is_live']:
        msg = '@{}, the stream is offline'.format(kwargs['display-name'])
        bot.send("PRIVMSG", target=target, message=msg)            
        return

    r = await bot.db.fetchone(
        'SELECT time FROM stream_watchtime WHERE channel_id=%s AND stream_id=%s AND user_id=%s',
        (
            channel_id,
            bot.channels[channel_id]['stream_id'], 
            user_id,
        )
    )

    if not r or (r['time'] == 0):    
        msg = 'I have no data on {} yet'.format(user)
        bot.send("PRIVMSG", target=target, message=msg)
        return

    total_live_seconds = bot.channels[channel_id]['uptime']
    usertime = r['time']
    
    if (usertime > total_live_seconds) or ((total_live_seconds - usertime) <= 60):
        usertime = total_live_seconds

    p = usertime / total_live_seconds
    msg = '{} has been here for {} this stream ({:.0%})'.format(
        user, 
        utils.seconds_to_pretty(usertime),
        p
    )
    bot.send("PRIVMSG", target=target, message=msg)
