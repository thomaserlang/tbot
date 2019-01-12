from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils

@fills_vars('user.streams_row', 'user.streams_total', 'user.streams_row_peak', 
    'user.streams_row_peak_date', 'user.streams_row_text')
async def handler(bot, channel_id, user_id, args, display_name, **kwargs):
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)

    r = await bot.db.fetchone(
        'SELECT * FROM twitch_user_stats WHERE channel_id=%s AND user_id=%s',
        (
            channel_id,
            user_id,
        )
    )

    if not r:
        return {
            'user.streams_row': 0,
            'user.streams_total': 0,
            'user.streams_row_peak': 0,
            'user.streams_row_peak_date': 'unknown date',
            'user.streams_row_text': '{} has been here for 0 streams in a row'.format(
                user,
            )
        }

    msg = '{} has been here for {} in a row'.format(
        user,
        utils.pluralize(r['streams_row'], 'stream')
    )
    if r['streams_row'] < r['streams_row_peak']:
        msg += ' (Peak: {}, {})'.format(
            r['streams_row_peak'],
            r['streams_row_peak_date'].isoformat()
        )
    if r['streams'] != r['streams_row']:
        msg += ' and a total of {}'.format(
            utils.pluralize(r['streams'], 'stream')
        )
    return {
        'user.streams_row': utils.pluralize(r['streams_row'], 'stream'),
        'user.streams_total': utils.pluralize(r['streams'], 'stream'),
        'user.streams_row_peak': utils.pluralize(r['streams_row_peak'], 'stream'),
        'user.streams_row_peak_date': r['streams_row_peak_date'].isoformat(),
        'user.streams_row_text': msg,
    }