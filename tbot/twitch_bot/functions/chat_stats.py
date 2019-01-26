from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils
from datetime import datetime, timedelta

@fills_vars('user.chat_stats.stream_msgs', 'user.chat_stats.stream_msgs_num', 
    'user.chat_stats.stream_words', 'user.chat_stats.stream_words_num')
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
        'user.chat_stats.stream_msgs_num': r['msgs'],
        'user.chat_stats.stream_words': utils.pluralize(r['words'], 'word'),
        'user.chat_stats.stream_words_num': r['words'],
    }

@fills_vars('user.chat_stats.month_msgs', 'user.chat_stats.month_msgs_num', 
    'user.chat_stats.month_words', 'user.chat_stats.month_words_num')
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
        'user.chat_stats.month_msgs_num': r['msgs'],
        'user.chat_stats.month_words': utils.pluralize(r['words'], 'word'),
        'user.chat_stats.month_words_num': r['words'],
    }

@fills_vars('user.chat_stats.last_month_msgs', 'user.chat_stats.last_month_msgs_num', 
    'user.chat_stats.last_month_words', 'user.chat_stats.last_month_words_num')
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
        'user.chat_stats.last_month_msgs_num': r['msgs'],
        'user.chat_stats.last_month_words': utils.pluralize(r['words'], 'word'),
        'user.chat_stats.last_month_words_num': r['words'],
    }

@fills_vars('chat_stats.stream_msgs', 'chat_stats.stream_msgs_num', 
    'chat_stats.stream_words', 'chat_stats.stream_words_num')
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
        'chat_stats.stream_msgs_num': r['msgs'],
        'chat_stats.stream_words': utils.pluralize(r['words'], 'word'),
        'chat_stats.stream_words_num': r['words'],
    }

@fills_vars('user.chat_stats.total_msgs', 'user.chat_stats.total_msgs_num', 
    'user.chat_stats.bans', 'user.chat_stats.bans_num', 
    'user.chat_stats.timeouts', 'user.chat_stats.timeouts_num', 
    'user.chat_stats.deletes', 'user.chat_stats.deletes_num', 
    'user.chat_stats.purges', 'user.chat_stats.purges_num')
async def user_chat_stats(bot, channel_id, user_id, args, **kwargs):
    if len(args) > 0:
        uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))
        if uid:
            user_id = uid
    r = await bot.db.fetchone(
        'SELECT * FROM twitch_user_chat_stats WHERE channel_id=%s AND user_id=%s',
        (channel_id, user_id,)
    )
    if not r:
        r = {
            'chat_messages': 0,
            'bans': 0,
            'timeouts': 0,
            'deletes': 0,
            'purges': 0,
        }
    return {
        'user.chat_stats.total_msgs': utils.pluralize(r['chat_messages'], 'message'),
        'user.chat_stats.total_msgs_num': r['chat_messages'],
        'user.chat_stats.bans': utils.pluralize(r['bans'], 'time'),
        'user.chat_stats.bans_num': r['bans'],
        'user.chat_stats.timeouts': utils.pluralize(r['timeouts'], 'time'),
        'user.chat_stats.timeouts_num': r['timeouts'],
        'user.chat_stats.deletes': utils.pluralize(r['deletes'], 'time'),
        'user.chat_stats.deletes_num': r['deletes'],
        'user.chat_stats.purges': utils.pluralize(r['purges'], 'time'),
        'user.chat_stats.purges_num': r['purges'],
    }