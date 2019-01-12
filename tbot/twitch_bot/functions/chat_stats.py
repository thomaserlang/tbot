from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils
from datetime import datetime, timedelta

@fills_vars('user.chat_stats.stream_msgs', 'user.chat_stats.stream_words')
async def user_stream(bot, channel_id, args, user_id, **kwargs):
    if len(args) > 0:
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))
    r = await bot.db.fetchone(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM twitch_chatlog WHERE 
           channel_id=%s AND 
           user_id=%s AND 
           created_at>=%s AND 
           type=1
           GROUP BY user_id;''',
        (
            channel_id, 
            user_id,
            bot.channels_check[channel_id]['went_live_at'],
        )
    )
    if not r:
        r = {
            'msgs': 0,
            'words': 0,
        }
    return {
        'user.chat_stats.stream_msgs': utils.pluralize(r['msgs'], 'message'),
        'user.chat_stats.stream_words': utils.pluralize(r['words'], 'word'),
    }

@fills_vars('user.chat_stats.month_msgs', 'user.chat_stats.month_words')
async def user_month(bot, channel_id, args, user_id, **kwargs):
    if len(args) > 0:
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))
    from_date = datetime.utcnow().replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    )
    r = await bot.db.fetchone(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM twitch_chatlog WHERE 
           channel_id=%s AND 
           user_id=%s AND 
           created_at>=%s AND 
           type=1
           GROUP BY user_id;''',
        (
            channel_id, 
            user_id,
            from_date,
        )
    )
    if not r:
        r = {
            'msgs': 0,
            'words': 0,
        }
    return {
        'user.chat_stats.month_msgs': utils.pluralize(r['msgs'], 'message'),
        'user.chat_stats.month_words': utils.pluralize(r['words'], 'word'),
    }

@fills_vars('user.chat_stats.last_month_msgs', 'user.chat_stats.last_month_words')
async def user_last_month(bot, channel_id, args, user_id, **kwargs):
    if len(args) > 0:
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))
    to_date = datetime.utcnow().replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    ) - timedelta(seconds=1)
    from_date = to_date.replace(
        day=1, hour=0, minute=0, 
        second=0, microsecond=0,
    )
    r = await bot.db.fetchone(
        '''SELECT count(message) as msgs, sum(word_count) as words 
           FROM twitch_chatlog WHERE 
           channel_id=%s AND 
           user_id=%s AND 
           created_at>=%s AND 
           created_at<=%s AND 
           type=1
           GROUP BY user_id;''',
        (
            channel_id, 
            user_id,
            from_date,
            to_date,
        )
    )
    if not r:
        r = {
            'msgs': 0,
            'words': 0,
        }
    return {
        'user.chat_stats.last_month_msgs': utils.pluralize(r['msgs'], 'message'),
        'user.chat_stats.last_month_words': utils.pluralize(r['words'], 'word'),
    }

@fills_vars('chat_stats.stream_msgs', 'chat_stats.stream_words')
async def stream(bot, channel_id, args, user_id, **kwargs):
    r = await bot.db.fetchone(
        '''SELECT count(message) as msgs, sum(word_count) as words
           FROM twitch_chatlog WHERE 
           channel_id=%s AND 
           created_at>=%s AND 
           type=1;''',
        (
            channel_id, 
            bot.channels_check[channel_id]['went_live_at'],
        )
    )
    if not r:
        r = {
            'msgs': 0,
            'words': 0,
        }
    return {
        'chat_stats.stream_msgs': utils.pluralize(r['msgs'], 'message'),
        'chat_stats.stream_words': utils.pluralize(r['words'], 'word'),
    }