import bottom, asyncio, logging, random, aiohttp
from datetime import datetime
from tbot.twitch_bot.unpack import rfc2812_handler
from tbot import config, db

bot = bottom.Client('a', 0)

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    if not bot.http_session:
        bot.http_session = aiohttp.ClientSession()
    if not bot.db:
        bot.db = await db.Db().connect(bot.loop)

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    logging.info('IRC Connecting to {}:{}'.format(config['twitch']['irc_host'], config['twitch']['irc_port']))
    if config['twitch']['token']:
        bot.send('PASS', password='oauth:{}'.format(config['twitch']['token']))
    bot.send('NICK', nick=config['twitch']['user'])
    bot.send('USER', user=config['twitch']['user'], realname=config['twitch']['user'])

    # Don't try to join channels until the server has
    # sent the MOTD, or signaled that there's no MOTD.
    done, pending = await asyncio.wait(
        [bot.wait("RPL_ENDOFMOTD"),
         bot.wait("ERR_NOMOTD")],
        loop=bot.loop,
        return_when=asyncio.FIRST_COMPLETED
    )

    bot.send_raw('CAP REQ :twitch.tv/tags')
    bot.send_raw('CAP REQ :twitch.tv/commands')
    bot.send_raw('CAP REQ :twitch.tv/membership')

    # Cancel whichever waiter's event didn't come in.
    for future in pending:
        future.cancel()

    bot.channels = await get_channels()
    for c in bot.channels.values():
        bot.send('JOIN', channel='#'+c['name'])
        bot.send("PRIVMSG", target='#'+c['name'], message='/mods')

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())

async def send_ping():
    await asyncio.sleep(random.randint(120, 240))
    logging.debug('Sending ping')
    bot.pong_check_callback = asyncio.ensure_future(wait_for_pong())
    bot.send('PING')

async def wait_for_pong():
    await asyncio.sleep(10)
    logging.error('Didn\'t receive a PONG in time, reconnecting')
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())
    await bot.connect()

@bot.on('CLIENT_DISCONNECT')
async def disconnect(**kwargs):
    logging.info('Disconnected')

@bot.on('PING')
def keepalive(message, **kwargs):
    logging.debug('Received ping, sending PONG back')
    bot.send('PONG', message=message)

@bot.on('PONG')
async def pong(message, **kwargs):
    logging.debug('Received pong')
    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())

@bot.on('PRIVMSG')
async def message(nick, target, message, **kwargs):
    if not bot.channels[int(kwargs['room-id'])]['enabled']:
        return

    bot.loop.create_task(
        save(1, target, kwargs['room-id'], nick, kwargs['user-id'], message)
    )

    if not message.startswith('!'):
        return

    is_mod = kwargs['mod'] == '1' or nick == target.strip('#')
    if is_mod and message == '!updatemods':
        bot.send("PRIVMSG", target=target, message='/mods')
        bot.send("PRIVMSG", target=target, message='Affirmative, {}'.format(nick))

@bot.on('CLEARCHAT')
async def clearchat(channel, banned_user, **kwargs):
    if 'ban-reason' not in kwargs:
        return
    if not bot.channels[int(kwargs['room-id'])]['enabled']:
        return
    type_ = 2
    reason = kwargs['ban-reason'] or 'empty'
    message = '<Banned. Reason: {}>'.format(reason)
    if 'ban-duration' in kwargs:
        type_ = 3
        message = '<Timeout. Duration: {}. Reason: {}>'.format(kwargs['ban-duration'], reason)
        if kwargs['ban-duration'] == '1':
            message = '<Purge. Reason: {}>'.format(reason)
            type_ = 4
    bot.loop.create_task(
        save(type_, channel, kwargs['room-id'], banned_user, kwargs['target-user-id'], message)
    )

@bot.on('NOTICE')
async def notice(target, message, **kwargs):
    logging.debug('NOTICE: {}'.format(message))
    if 'msg-id' not in kwargs:
        return

    if kwargs['msg-id'] == 'room_mods':
        bot.loop.create_task(save_mods(target, message))

async def save_mods(target, message):
    a = message.split(':')
    channel = target.strip('#')
    if len(a) == 2:
        mods = [b.strip() for b in a[1].split(',')]
    else:
        mods = []
    mods.append(channel)
    channel_id = None
    for c in bot.channels.values():
        if c['name'].lower() == channel:
            channel_id = c['channel_id'] 

    users = await lookup_usernames(mods)
    if users == None:
        return
    data = []
    for u in users:
        data.append((
            channel_id,
            u['id'],
        ))
    await bot.db.execute('DELETE FROM twitch_channel_mods WHERE channel_id=%s;', 
        (channel_id,)
    )
    await bot.db.executemany(
        'INSERT INTO twitch_channel_mods (channel_id, user_id) VALUES (%s, %s);', 
        data
    )

async def lookup_usernames(usernames):
    url = 'https://api.twitch.tv/helix/users'
    params = [('login', name) for name in usernames]
    headers = {'Authorization': 'Bearer {}'.format(config['twitch']['token'])}
    async with bot.http_session.get(url, params=params, headers=headers) as r:
        if r.status != 200:
            return None
        data = await r.json()
        users = []
        for d in data['data']:
            users.append({'id': d['id'], 'user': d['login']})
        return users

def send_whisper(nick, target, message):
    bot.send('PRIVMSG', target=target, message='/w {} {}'.format(nick, message))

async def save(type_, channel, channel_id, user, user_id, message):
    logging.debug('{} {} {} {}'.format(type_, channel, user, message))
    try:
        await bot.db.execute('''
            INSERT INTO twitch_chatlog (type, created_at, channel_id, user, user_id, message, word_count) VALUES
                (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            type_,
            datetime.utcnow(),
            channel_id,
            user,
            user_id,
            message,
            len(message.split(' ')),
        ))
    except:
        logging.exception('sql')

async def get_channels():
    rows = await bot.db.fetchall('''
    SELECT 
        c.channel_id, c.name, m.name as module
    FROM
        channels c
            LEFT JOIN
        twitch_enabled_modules m ON (m.channel_id = c.channel_id
            AND m.name = 'chatlog');
    ''')
    l = {}
    for r in rows:
        l[r['channel_id']] = {
            'channel_id': r['channel_id'],
            'name': r['name'].lower(),
            'enabled': r['module'] != None,
        }
    return l

def main():
    bot.host = config['twitch']['irc_host'] 
    bot.port = config['twitch']['irc_port'] 
    bot.ssl = config['twitch']['irc_use_ssl']
    bot.raw_handlers = [rfc2812_handler(bot)]
    bot.http_session = None
    bot.db = None
    bot.pong_check_callback = None
    bot.ping_callback = None
    return bot

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')
    logger.set_logger('chatlog.log')
    loop = asyncio.get_event_loop()
    loop.create_task(main().connect())    
    loop.run_forever()