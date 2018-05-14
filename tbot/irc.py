import bottom, asyncio, logging, random
import sqlalchemy as sa
import requests
from dateutil.parser import parse
from datetime import datetime
from tbot.unpack import rfc2812_handler
from tbot import config

bot = bottom.Client('a', 0)

bot.users = {}

bot.pong_check_callback = None
bot.ping_callback = None
bot.channel_watchtime_increment = None

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
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
        bot.send('JOIN', channel='#'+channel.strip('#'))

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())

    if bot.channel_watchtime_increment:
        bot.channel_watchtime_increment.cancel()
    bot.channel_watchtime_increment = \
        asyncio.ensure_future(channel_watchtime_increment())

def get_users():
    for channel in config['channels']:
        r = requests.get('https://tmi.twitch.tv/group/user/{}/chatters'.format(
            channel.strip('#')
        ))
        if r.status_code == 200:
            bot.users[channel] = []
            data = r.json()
            bot.users[channel].extend(data['chatters']['viewers'])
            bot.users[channel].extend(data['chatters']['global_mods'])
            bot.users[channel].extend(data['chatters']['admins'])
            bot.users[channel].extend(data['chatters']['staff'])
            bot.users[channel].extend(data['chatters']['moderators'])
        else:
            logging.error(r.text)

def is_live(channel):
    r = requests.get('https://api.twitch.tv/kraken/streams/{}?client_id={}'.format(
        channel,
        config['client_id']
    ))
    if r.status_code == 200:
        data = r.json()
        if data['stream']:
            return data['stream']['created_at']
        return False
    else:
        logging.error(r.text)

async def channel_watchtime_increment():
    asyncio.ensure_future(start_channel_watchtime())
    try:
        get_users()
        for channel in config['channels']:
            live = is_live(channel)
            if live == False:
                bot.conn.execute(sa.sql.text('''
                    DELETE FROM current_stream_watchtime WHERE channel=:channel;
                '''), {
                    'channel': channel,
                })
            elif live:
                if channel in bot.users:
                    data = []
                    for user in bot.users[channel]:
                        data.append({'user': user, 'channel': channel})
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
        r = bot.conn.execute(sa.sql.text('SELECT time FROM current_stream_watchtime WHERE channel=:channel AND user=:user'),
            {'channel': target.strip('#'), 'user': user}
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

def main():
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
    return bot

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load()    
    logger.set_logger('irc.log')
    loop = asyncio.get_event_loop()
    loop.create_task(main().connect())    
    loop.run_forever()