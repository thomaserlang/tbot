import logging, re
from tbot.twitch_bot.bot_base import bot
from tbot.twitch_bot.tasks.command import get_user_level
from tbot import config, utils

filters = {}

@bot.on('PRIVMSG')
async def message(nick, target, message, **kwargs):
    if kwargs['room-id'] not in filters:
        return
    f = filters[kwargs['room-id']]
    if f['enabled'] != 'Y':
        return
    ul = await get_user_level(kwargs['badges'], kwargs['user-id'], kwargs['room-id'], f['exclude_user_level'])
    if ul >= f['exclude_user_level']:
        return

    matches = URL.findall(message)
    if matches: # check if the user is permitted to post links
        key = 'tbot:filter:permit:{}:{}'.format(
            kwargs['room-id'], kwargs['user-id']
        )
        permit = await bot.redis.get(key)
        if permit:
            return

    for m in matches:
        if m[2] in f['whitelist']:
            continue

        if f['warning_enabled'] == 'Y':
            key = 'tbot:filter-link:warning:{}:{}'.format(
                kwargs['room-id'], kwargs['user-id']
            )
            warned = await bot.redis.get(key)
            if not warned:
                bot.loop.create_task(bot.redis.setex(key, f['warning_expire'], '1'))
                bot.send("PRIVMSG", target=target, message='.delete {}'.format(kwargs['id']))
                if f['warning_message']:                    
                    bot.send("PRIVMSG", target=target, message='@{}, {}'.format(
                        kwargs['display-name'] or kwargs['user'],
                        f['warning_message'],
                    ))
                return

        bot.send("PRIVMSG", target=target, message='.timeout {} {} {}'.format(
            kwargs['user'], 
            f['timeout_duration'], 
            '[{}] Link filter'.format(bot.user['display_name']),
        ))
        if f['timeout_message']:                    
            bot.send("PRIVMSG", target=target, message='@{}, {}'.format(
                kwargs['display-name'] or kwargs['user'],
                f['timeout_message'],
            ))

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