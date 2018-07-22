import bottom, logging, random
import asyncio, aiohttp
import sqlalchemy as sa
import requests
from sqlalchemy_aio import ASYNCIO_STRATEGY
from datetime import datetime
from tbot.irc.unpack import rfc2812_handler
from tbot.irc.command import handle_command
from tbot.irc.sub_log import log_sub
from tbot import config

bot = bottom.Client('a', 0)
bot.channels = {}

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

    channels = await get_channels()
    for c in channels:
        bot.send('JOIN', channel='#'+c['name'])

    if not bot.channels:
        for c in channels:
            bot.channels[c['channel_id']] = {
                'channel_id': c['channel_id'],
                'name': c['name'],
            }

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()
    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())
    bot.trigger('AFTER_CHANNEL_JOIN')

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

async def get_channels():
    q = await bot.conn.execute('SELECT channel_id, name FROM channels WHERE active="Y";')
    rows = await q.fetchall()
    l = []
    for r in rows:
        l.append({
            'channel_id': r['channel_id'],
            'name': r['name'].lower(),
        })
    return l

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
    handle_command(bot, nick, target, message, **kwargs)
    bot.loop.create_task(log_sub(bot, nick, target, message, **kwargs))

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
    bot.pong_check_callback = None
    bot.ping_callback = None
    bot.starttime = datetime.utcnow()
    return bot

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')
    logger.set_logger('bot.log')
    print('test')
    loop = asyncio.get_event_loop()
    loop.create_task(main().connect())
    loop.run_forever()