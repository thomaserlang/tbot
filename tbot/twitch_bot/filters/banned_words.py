from typing import List
import logging, re
from tbot.twitch_bot.bot_base import bot
from tbot import utils

from . import base

rules = {}

async def check(target, message, kwargs):
    if kwargs['room-id'] not in rules:
        return

    f = rules[kwargs['room-id']]

    for fid in f:
        excluded = await base.is_excluded(bot, f[fid], kwargs)
        if excluded:
            continue
        if check_message(message, f[fid]['banned_words']):
            await base.warn_or_timeout(bot, 'banned_words', target, f[fid], kwargs)
            return True

def check_message(message: str, banned_words: List[str]):
    for bw in banned_words:
        if bw.startswith('re:'):
            if re.search(bw[3:], message, flags=re.IGNORECASE):
                return True
            continue

        s = utils.split(bw)
        if all([re.search(rf'\b{a}\b', message, flags=re.IGNORECASE) for a in s]):
            return True
            
    return False

@bot.on('AFTER_CONNECTED')
async def connected(**kwargs):
    if not rules:
        await load()

@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    if cmd == 'reload_filter_banned_words':
        await load(cmd_args[0])

async def load(channel_id=None):
    global rules
    sql = '''
        SELECT 
            f.*, bw.banned_words
        FROM
            twitch_filters f,
            twitch_filter_banned_words bw
        WHERE
            bw.filter_id = f.id
            AND f.type = 'banned_words'
    '''
    args = []
    if channel_id:
        sql += ' AND f.channel_id=%s'
        args.append(channel_id)
    rows = await bot.db.fetchall(sql, args)
    rules_ = rules if channel_id else {}
    if channel_id and channel_id in rules_:
        del rules_[channel_id]
    for r in rows:
        f = rules_.setdefault(r['channel_id'], {})
        banned_words = r['banned_words']
        k = f.setdefault(r['id'], r)
        if not isinstance(k['banned_words'], list):
            k['banned_words'] = []
        k['banned_words'].append(banned_words)
    rules = rules_
