import logging
from datetime import datetime
from tbot.twitch_bot.command import command
from tbot import utils

@command('streamsinarow', alias='siar')
async def streams_in_a_row(bot, nick, channel, channel_id, target, args, **kwargs):
    user = kwargs['display-name']
    user_id = kwargs['user-id']
    if len(args) > 0:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, user)

    r = await bot.db.fetchone(
        'SELECT * FROM user_stats WHERE channel_id=%s AND user_id=%s',
        (
            channel_id,
            user_id,
        )
    )

    if not r:
        msg = 'I have no data on {} yet'.format(user)
        bot.send("PRIVMSG", target=target, message=msg)
        return

    msg = '{} has been here for {} {} in a row'.format(
        user,
        r['streams_row'],
        'streams' if r['streams_row'] != 1 else 'stream',
    )

    if r['streams_row'] < r['streams_row_peak']:
        msg += ' (Peak: {}, {})'.format(
            r['streams_row_peak'],
            r['streams_row_peak_date'].isoformat()
        )

    msg += ' and a total of {} {}'.format(
        r['streams'],
        'streams' if r['streams'] != 1 else 'stream',
    )

    bot.send("PRIVMSG", target=target, message=msg)