from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils

@fills_vars('user.stream_watchtime', 'user.stream_watchtime_percent')
async def stream_watchtime(bot, channel_id, user_id, args, **kwargs):
    if len(args) > 0:
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))

    r = await bot.db.fetchone(
        'SELECT time FROM twitch_stream_watchtime WHERE channel_id=%s AND stream_id=%s AND user_id=%s',
        (
            channel_id,
            bot.channels_check[channel_id]['stream_id'], 
            user_id,
        )
    )
    time = 0
    if r:
        time = r['time']

    total_live_seconds = bot.channels_check[channel_id]['uptime']
    usertime = time
    
    if (usertime > total_live_seconds) or ((total_live_seconds - usertime) <= 60):
        usertime = total_live_seconds

    p = 0
    if total_live_seconds > 0:
        p = usertime / total_live_seconds

    return {
        'user.stream_watchtime': utils.seconds_to_pretty(usertime),
        'user.stream_watchtime_percent': '{:.0%}'.format(p),
    }


@fills_vars('user.channel_watchtime', 'user.channel_watchtime_since')
async def channel_watchtime(bot, channel_id, user_id, args, **kwargs):
    if len(args) > 0:
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))

    r = await bot.db.fetchone('''
        SELECT sum(tw.time) as time, min(ts.started_at) as date FROM 
        twitch_stream_watchtime tw, twitch_streams ts 
        WHERE tw.channel_id=%s AND tw.user_id=%s AND tw.stream_id=ts.stream_id
        ''',
        (
            channel_id,
            user_id,
        )
    )

    return {
        'user.channel_watchtime': utils.seconds_to_pretty(r['time'] if r else 0),
        'user.channel_watchtime_since': r['date'].strftime('%Y-%m-%d') if r else 'Unknown',
    }