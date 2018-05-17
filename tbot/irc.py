import bottom, logging, random
import asyncio, aiohttp
import sqlalchemy as sa
import requests
from sqlalchemy_aio import ASYNCIO_STRATEGY
from dateutil.parser import parse
from datetime import datetime
from tbot.unpack import rfc2812_handler
from tbot import config

bot = bottom.Client('a', 0)

bot.channels = {}

bot.pong_check_callback = None
bot.ping_callback = None
bot.channels_check_callback = None
bot.starttime = datetime.utcnow()

async def channels_check():
    asyncio.ensure_future(start_channel_check_callback())
    logging.info('Channels check')
    try:
        await get_users()
        for channel in config['channels']:
            old_is_live = bot.channels[channel]['is_live']
            is_live = await get_is_live(channel)
            if old_is_live == None:
                continue
            if is_live:
                inc_time = 60
                if old_is_live != is_live:
                    inc_time = round((datetime.utcnow() - bot.channels[channel]['went_live_at']).total_seconds())
                    logging.info('{} is now live ({} seconds ago)'.format(channel, inc_time))
                    await reset_stream_watchtime(channel)
                data = []
                bot.channels[channel]['check_counter'] += 1
                logging.debug('Channel check: {} - count: {}'.format(
                    channel,
                    bot.channels[channel]['check_counter']
                ))
                for user in bot.channels[channel]['users']:
                    data.append({'user': user, 'channel': channel, 'inc_time': inc_time})
                if data:
                    await bot.conn.execute(sa.sql.text('''
                        INSERT INTO current_stream_watchtime (channel, user, time) 
                        VALUES (:channel, :user, :inc_time) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
                    '''), data)
            else:
                if old_is_live != is_live:
                    logging.info('{} went offline'.format(channel))
                    await reset_stream_watchtime(channel)
    except:
        logging.exception('channels_check')

async def reset_stream_watchtime(channel):
    await bot.conn.execute(sa.sql.text('''
        DELETE FROM current_stream_watchtime WHERE channel=:channel;
    '''), {
        'channel': channel,
    })
    bot.channels[channel]['check_counter'] = 0

async def start_channel_check_callback():    
    await asyncio.sleep(60)
    bot.channels_check_callback = \
        asyncio.ensure_future(channels_check())

@bot.on('PRIVMSG')
def message(nick, target, message, **kwargs):
    if not message.startswith('!'):
        return    
    args = message.split(' ')
    cmd = args.pop(0).lower()
    if cmd == '!streamwatchtime' or cmd == '!swt':
        asyncio.ensure_future(cmd_streamwatchtime(kwargs['display-name'], target, args))
    elif cmd == '!{}'.format(config['user'].lower()):
        asyncio.ensure_future(cmd_bot(kwargs['display-name'], target, args))
    elif cmd == '!betteruptime':
        asyncio.ensure_future(cmd_better_uptime(kwargs['display-name'], target, args))


async def cmd_streamwatchtime(nick, target, args):
    try:
        user = nick
        if len(args) > 0:
            user = args[0].strip('@')

        channel = target.strip('#')

        if not bot.channels[channel]['is_live']:
            msg = '@{}, the stream is offline'.format(nick)
            bot.send("PRIVMSG", target=target, message=msg)            
            return

        r = await bot.conn.execute(sa.sql.text('SELECT time FROM current_stream_watchtime WHERE channel=:channel AND user=:user'),
            {'channel': channel, 'user': user}
        )
        r = await r.fetchone()

        if not r or (r['time'] == 0):    
            msg = '{} is unknown to me'.format(user)
            bot.send("PRIVMSG", target=target, message=msg)
            return

        total_live_seconds = round((bot.channels[channel]['last_check'] - \
            bot.channels[channel]['went_live_at']).total_seconds())
        p = r['time'] / total_live_seconds
        msg = '{} has been here for {} this stream ({:.0%})'.format(
            user, 
            seconds_to_pretty(r['time']),
            p
        )
        bot.send("PRIVMSG", target=target, message=msg)
    except:
        logging.exception('cmd_streamwatchtime')


async def cmd_better_uptime(nick, target, args):
    channel = target.strip('#')

    if not bot.channels[channel]['is_live']:
        msg = '@{}, the stream is offline'.format(nick)
        bot.send("PRIVMSG", target=target, message=msg)
        return

    if not bot.channels[channel]['went_live_at']:
        msg = '@{}, the stream start time is unknown to me'.format(nick)
        bot.send("PRIVMSG", target=target, message=msg)
        return

    seconds = (datetime.utcnow() - bot.channels[channel]['went_live_at']).total_seconds()
    msg = 'This stream has been live for {}'.format(seconds_to_pretty(seconds))
    bot.send("PRIVMSG", target=target, message=msg)            


async def cmd_bot(nick, target, args):
    
    if len(args) == 0:
        bot.send("PRIVMSG", target=target, message='@{}, Commands: !streamwatchtime (!swt), !betteruptime'.format(nick))
        return

    if args[0].lower() == 'uptime':
        seconds = (datetime.utcnow() - bot.starttime).total_seconds()
        msg = 'I\'ve been up for {}'.format(seconds_to_pretty(seconds))
        bot.send("PRIVMSG", target=target, message=msg)


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
                        if not bot.channels[channel]['is_live']:
                            bot.channels[channel]['went_live_at'] = parse(data['stream']['created_at']).replace(tzinfo=None)
                        bot.channels[channel]['is_live'] = True
                    else:
                        bot.channels[channel]['is_live'] = False
                        bot.channels[channel]['went_live_at'] = None
                    bot.channels[channel]['last_check'] = datetime.utcnow()
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
                'is_live': None,
                'went_live_at': None,
                'users': [],
                'check_counter': 0,
                'last_check': None,
            }
        bot.send('JOIN', channel='#'+channel)

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())

    if bot.channels_check_callback:
        bot.channels_check_callback.cancel()
    bot.channels_check_callback = \
        asyncio.ensure_future(channels_check())

def seconds_to_pretty(seconds):
    if seconds < 60:
        return '{} seconds'.format(round(seconds))

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    ts = []
    if hours == 1:
        ts.append('1 hour')
    elif hours > 1:
        ts.append('{} hours'.format(round(hours)))
    if minutes == 1:
        ts.append('1 min')
    elif minutes > 1:
        ts.append('{} mins'.format(round(minutes)))

    return ' '.join(ts)

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
        strategy=ASYNCIO_STRATEGY,
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