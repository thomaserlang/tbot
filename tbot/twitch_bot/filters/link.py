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
    
    matches = URL.findall(message)
    if matches: # check if the user is permitted to post links
        has_permit = await base.has_permit(bot, kwargs)
        if has_permit:
            return
    else:
        return

    for m in matches:
        if m[2] in f['whitelist']:
            continue
        await base.warn_or_timeout(bot, 'link', target, f, kwargs)
        return True

@bot.on('AFTER_CONNECTED')
async def connected(**kwargs):
    if not filters:
        await load()

@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    if cmd == 'reload_filter_link':
        await load(cmd_args[0])

async def load(channel_id=None):
    global filters
    sql = '''
        SELECT f.*, l.whitelist 
        FROM twitch_filters f 
            LEFT JOIN twitch_filter_link l 
                ON (l.channel_id=f.channel_id) 
        WHERE 
            type="link"
    '''
    args = []
    if channel_id:
        sql += ' AND f.channel_id=%s'
        args.append(channel_id)
    rows = await bot.db.fetchall(sql, args)
    filters_ = filters if channel_id else {}
    for r in rows:
        r['whitelist'] = utils.json_loads(r['whitelist']) if r['whitelist'] else []
        filters_[r['channel_id']] = r
    filters = filters_

# https://github.com/PhantomBot/PhantomBot/blob/9d8d1faa4394723052db64b53cb0efadc36cae3c/javascript-source/core/patternDetector.js#L26
URL = re.compile(
    '((?:(http|https|rtsp):\\/\\/(?:(?:[a-z0-9\\$\\-\\_\\.\\+\\!\\*\\\'\\(\\)'\
    '\\,\\;\\?\\&\\=]|(?:\\%[a-fA-F0-9]{2})){1,64}(?:\\:(?:[a-z0-9\\$\\-\\_'\
    '\\.\\+\\!\\*\\\'\\(\\)\\,\\;\\?\\&\\=]|(?:\\%[a-fA-F0-9]{2})){1,25})?\\@)?)?'\
    '((?:(?:[a-z0-9][a-z0-9\\-]{0,64}\\.)+'\
    '(?:'\
    '(?:aero|a[cdefgilmnoqrstuwxz])'\
    '|(?:biz|b[abdefghijmnorstvwyz])'\
    '|(?:com|c[acdfghiklmnoruvxyz])'\
    '|d[ejkmoz]'\
    '|(?:edu|e[cegrstu])'\
    '|(?:fyi|f[ijkmor])'\
    '|(?:gov|g[abdefghilmnpqrstuwy])'\
    '|(?:how|h[kmnrtu])'\
    '|(?:info|i[delmnoqrst])'\
    '|(?:jobs|j[emop])'\
    '|k[eghimnrwyz]'\
    '|l[abcikrstuvy]'\
    '|(?:mil|mobi|moe|m[acdeghklmnopqrstuvwxyz])'\
    '|(?:name|net|n[acefgilopruz])'\
    '|(?:org|om)'\
    '|(?:pro|p[aefghklmnrstwy])'\
    '|qa'\
    '|(?:r[eouw])'\
    '|(?:s[abcdeghijklmnortuvyz])'\
    '|(?:t[cdfghjklmnoprtvwz])'\
    '|u[agkmsyz]'\
    '|(?:vote|v[ceginu])'\
    '|(?:xxx)'\
    '|(?:watch|w[fs])'\
    '|y[etu]'\
    '|z[amw]))'\
    '|(?:(?:25[0-5]|2[0-4]'\
    '[0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\\.(?:25[0-5]|2[0-4][0-9]'\
    '|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(?:25[0-5]|2[0-4][0-9]|[0-1]'\
    '[0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}'\
    '|[1-9][0-9]|[0-9])))'\
    '(?:\\:\\d{1,5})?)'\
    '(\\/(?:(?:[a-z0-9\\;\\/\\?\\:\\@\\&\\=\\#\\~'\
    '\\-\\.\\+\\!\\*\\\'\\(\\)\\,\\_])|(?:\\%[a-fA-F0-9]{2}))*)?'\
    '(?:\\b|$)'\
    '|(\\.[a-z]+\\/|magnet:\/\/|mailto:\/\/|ed2k:\/\/|irc:\/\/|ircs:\/\/|skype:\/\/|ymsgr:\/\/|xfire:\/\/|steam:\/\/|aim:\/\/|spotify:\/\/)'
    , re.IGNORECASE)