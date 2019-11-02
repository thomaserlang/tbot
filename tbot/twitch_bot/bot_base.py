import logging, random, bottom
import asyncio, aiohttp, aiomysql, aioredis
from datetime import datetime
from tbot.twitch_bot.unpack import rfc2812_handler
from tbot.twitch_bot import bot_sender
from tbot import config, db, utils

class Client(bottom.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rate_limit_count = 0
        self.rate_limit_bucket = []
        self.is_running = False
        self.raw_handlers = [rfc2812_handler(self)]
        self.ahttp = None
        self.db = None
        self.redis = None
        self.redis_sub = None
        self.pong_check_callback = None
        self.ping_callback = None
        self.starttime = datetime.utcnow()
        self.user = None
        self.bot_sender = None

        self.host = config['twitch']['irc_host'] 
        self.port = config['twitch']['irc_port'] 
        self.ssl = config['twitch']['irc_use_ssl']
    
    def send(self, command: str, **kwargs) -> None:
        if self.rate_limit_count < config['twitch']['irc_rate_limit']:
            if command == 'PRIVMSG' and bot.bot_sender and kwargs['message'] != '/mods':
                bot.bot_sender.send(command, **kwargs)
            else:
                super().send(command, **kwargs)
            self.rate_limit_count += 1
        else:
            self.rate_limit_bucket.append({
                'command': command,
                'kwargs': kwargs,
            })
            logging.warning('Rate limit reached. In queue: {}'.format(len(self.rate_limit_bucket)))

    async def rate_limit_reset_runner(self):
        while True:
            self.rate_limit_count = 0
            if self.rate_limit_bucket:
                self.loop.create_task(self.rate_limit_send_bucket())
            await asyncio.sleep(30)

    async def rate_limit_send_bucket(self):
        bucket = self.rate_limit_bucket
        self.rate_limit_bucket = []
        for b in bucket:
            self.send(b['command'], **b['kwargs'])

bot = Client('a', 0)

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    if not bot.is_running:  
        bot.ahttp = aiohttp.ClientSession()        
        bot.db = await db.Db().connect(bot.loop)
        bot.loop.create_task(bot.rate_limit_reset_runner())
        bot.redis = await aioredis.create_redis_pool(
            'redis://{}:{}'.format(config['redis']['host'], config['redis']['port']),
            minsize=config['redis']['pool_min_size'], 
            maxsize=config['redis']['pool_max_size'],
            loop=bot.loop,
        )
        bot.user = await utils.twitch_current_user(bot.ahttp)
        bot.redis_sub = await bot.redis.subscribe('tbot:server:commands')
        bot.loop.create_task(receive_redis_server_commands())
        bot.is_running = True

        bot_sender.setup(bot)
        bot.loop.create_task(bot_sender.bot_sender.connect())

    if bot.pong_check_callback:
        bot.pong_check_callback.cancel()

    logging.info('IRC Connecting to {}:{} as {}'.format(
        config['twitch']['irc_host'], 
        config['twitch']['irc_port'],
        bot.user['login'],
    ))
    if config['twitch']['token']:
        bot.send('PASS', password='oauth:{}'.format(config['twitch']['token']))
    bot.send('NICK', nick=bot.user['login'])
    bot.send('USER', user=bot.user['login'], realname=bot.user['login'])

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

    for future in pending:
        future.cancel()

    if bot.ping_callback:
        bot.ping_callback.cancel()
    bot.ping_callback = asyncio.ensure_future(send_ping())
    bot.trigger('AFTER_CONNECTED')

async def receive_redis_server_commands():
    sub = bot.redis_sub[0]
    while (await sub.wait_message()):
        try:
            msg = await sub.get_json()
            logging.debug('Received server command: {}'.format(msg))
            if len(msg) < 2:
                return
            cmd = msg.pop(0)

            bot.trigger('REDIS_SERVER_COMMAND', cmd=cmd, cmd_args=msg)

        except:
            logging.exception('receive_redis_server_commands')

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