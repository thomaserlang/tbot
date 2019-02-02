import logging, re
from tbot.twitch_bot.bot_base import bot

from . import base

filters = {}

async def check(target, message, kwargs):
    if kwargs['room-id'] not in filters:
        return
    f = filters[kwargs['room-id']]

    excluded = await base.is_excluded(bot, f, kwargs)
    if excluded:
        return

    symbols = SYMBOLS.findall(message)
    if len(symbols) > f['max_symbols']:
        has_permit = await base.has_permit(bot, kwargs)
        if has_permit:
            return        
        await base.warn_or_timeout(bot, 'symbol', target, f, kwargs)
        return True

@bot.on('AFTER_CONNECTED')
async def connected(**kwargs):
    if not filters:
        await load()

@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    if cmd == 'reload_filter_symbol':
        await load(cmd_args[0])

async def load(channel_id=None):
    global filters
    sql = '''
        SELECT f.*, l.max_symbols 
        FROM twitch_filters f 
            LEFT JOIN twitch_filter_symbol l 
                ON (l.channel_id=f.channel_id) 
        WHERE 
            type="symbol"
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

SYMBOLS = re.compile(r'[^ \w]')