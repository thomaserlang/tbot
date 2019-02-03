import logging, re
from tbot.twitch_bot.bot_base import bot
from tbot import utils

from . import base

filters = {}

async def check(target, message, kwargs):
    if kwargs['room-id'] not in filters:
        return
    f = filters[kwargs['room-id']]

    excluded = await base.is_excluded(bot, f, kwargs)
    if excluded:
        return

    if len(message) < f['min_length']:
        return

    message = utils.twitch_remove_emotes(message, kwargs['emotes'])
    caps = CAPS.findall(message)
    if ((len(caps)/len(message))*100) > f['max_percent']:
        has_permit = await base.has_permit(bot, kwargs)
        if has_permit:
            return        
        await base.warn_or_timeout(bot, 'caps', target, f, kwargs)
        return True

@bot.on('AFTER_CONNECTED')
async def connected(**kwargs):
    if not filters:
        await load()

@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    if cmd == 'reload_filter_caps':
        await load(cmd_args[0])

async def load(channel_id=None):
    global filters
    sql = '''
        SELECT f.*, l.min_length, l.max_percent 
        FROM twitch_filters f 
            LEFT JOIN twitch_filter_caps l 
                ON (l.channel_id=f.channel_id) 
        WHERE 
            type="caps"
    '''
    args = []
    if channel_id:
        sql += ' AND f.channel_id=%s'
        args.append(channel_id)
    rows = await bot.db.fetchall(sql, args)
    filters_ = filters if channel_id else {}
    for r in rows:
        filters_[r['channel_id']] = r
    filters = filters_

CAPS = re.compile(r'[A-Z]')