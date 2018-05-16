import bottom, logging, random
import asyncio, aiohttp
import sqlalchemy as sa
import requests
from dateutil.parser import parse
from datetime import datetime
from tbot.unpack import rfc2812_handler
from tbot import config

bot = bottom.Client('a', 0)

bot.channels = {}

bot.pong_check_callback = None
bot.ping_callback = None
bot.channel_watchtime_increment = None

async def channel_watchtime_increment():
    asyncio.ensure_future(start_channel_watchtime())
    try:
        await get_users()
        for channel in config['channels']:
            old_live = bot.channels[channel]['is_live']
            is_live = await get_is_live(channel)
            if not is_live:
                if old_live != is_live:
                    bot.conn.execute(sa.sql.text('''
                        DELETE FROM current_stream_watchtime WHERE channel=:channel;
                    '''), {
                        'channel': channel,
                    })
                    bot.channels[channel]['inc_stream_watchtime_counter'] = 0
            else:
                data = []
                bot.channels[channel]['inc_stream_watchtime_counter'] += 1
                logging.debug('Incrementing watchtime for channel: {} - count: {}'.format(
                    channel,
                    bot.channels[channel]['inc_stream_watchtime_counter']
                ))
                for user in bot.channels[channel]['users']:
                    data.append({'user': user, 'channel': channel})
                if data:
                    bot.conn.execute(sa.sql.text('''
                        INSERT INTO current_stream_watchtime (channel, user, time) 
                        VALUES (:channel, :user, 60) ON DUPLICATE KEY UPDATE time=time+60;
                    '''), data)
    except:
        logging.exception('channel_watchtime_increment')

async def start_channel_watchtime():    
    await asyncio.sleep(60)
    bot.channel_watchtime_increment = \
        asyncio.ensure_future(channel_watchtime_increment())

@bot.on('PRIVMSG')
def message(nick, target, message, **kwargs):
    if not message.startswith('!'):
        return    
    args = message.split(' ')
    cmd = args.pop(0)
    if cmd == '!streamwatchtime':
        answer_streamwatchtime(nick, target, args)

def answer_streamwatchtime(nick, target, args):
    try:
        user = nick
        if len(args) > 0:
            user = args[0].strip('@')

        channel = target.strip('#')

        if not bot.channels[channel]['is_live']:
            msg = '{}, the stream seems to be offline'.format(nick)
            bot.send("PRIVMSG", target=target, message=msg)            
            return

        r = bot.conn.execute(sa.sql.text('SELECT time FROM current_stream_watchtime WHERE channel=:channel AND user=:user'),
            {'channel': channel, 'user': user}
        )
        r = r.fetchone()
        if not r or (r['time'] == 0):    
            msg = 'I have nothing on {} yet, wait a minute'.format(user)
            bot.send("PRIVMSG", target=target, message=msg)
            return

        seconds = r['time']

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        periods = [('hours', hours), ('minutes', minutes), ('seconds', seconds)]
        time_string = ', '.join('{} {}'.format(value, name) for name, value in periods if value)

        msg = '{} has watched this stream for {}'.format(user, time_string)
        bot.send("PRIVMSG", target=target, message=msg)
    except:
        logging.exception('answer_streamwatchtime')


async def get_users():
    for channel in config['channels']:
        try:
            async with bot.http_session.get('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel)) as r:
                if r.status == 200:
                    data = await r.json()
                    if data['chatter_count'] == 0:
                        continue
                    users = []
                    users.extend(data['chatters']['viewers'])
                    users.extend(data['chatters']['global_mods'])
                    users.extend(data['chatters']['admins'])
                    users.extend(data['chatters']['staff'])
                    users.extend(data['chatters']['moderators'])
                    if users:
                        bot.channels[channel]['users'] = users
        except:
            logging.exception('get_users')

async def get_is_live(channel):
    try:
        async with bot.http_session.get('https://api.twitch.tv/kraken/streams/{}'.format(channel),
            params={'client_id': config['client_id']}) as r:
            if r.status == 200:
                data = await r.json()
                if 'stream' in data:
                    if data['stream']:
                        bot.channels[channel]['is_live'] = True
                    else:
                        bot.channels[channel]['is_live'] = False
    except:
        logging.exception('is_live')
    if config['channel_always_live']:
        bot.channels[channel]['is_live'] = True
    return bot.channels[channel]['is_live'] 

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

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    if not bot.http_session:
        bot.http_session = aiohttp.ClientSession()
    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    logging.info('IRC Connecting to {}:{}'.format(config['irc']['host'], config['irc']['port']))
    if config['token']:
        bot.send('PASS', password='oauth:{}'.format(config['token']))
    bot.send('NICK', nick=config['user'])
    bot.send('USER', user=config['user'], realname=config['user'])

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

    for channel in config['channels']:
        channel = channel.strip('#')
        if channel not in bot.channels:
            bot.channels[channel] = {
                'is_live': False,
                'users': [],
                'inc_stream_watchtime_counter': 0,
            }
        bot.send('JOIN', channel='#'+channel)

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())

    if bot.channel_watchtime_increment:
        bot.channel_watchtime_increment.cancel()
    bot.channel_watchtime_increment = \
        asyncio.ensure_future(channel_watchtime_increment())

def main():
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    bot.host = config['irc']['host'] 
    bot.port = config['irc']['port'] 
    bot.ssl = config['irc']['use_ssl']
    bot.raw_handlers = [rfc2812_handler(bot)]
    bot.conn = sa.create_engine(config['sql_url'],
        convert_unicode=True,
        echo=False,
        pool_recycle=3599,
        encoding='UTF-8',
        connect_args={'charset': 'utf8mb4'},
    )
    bot.http_session = None
    return bot

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load()    
    logger.set_logger('irc.log')
    loop = asyncio.get_event_loop()
    loop.create_task(main().connect())    
    loop.run_forever()