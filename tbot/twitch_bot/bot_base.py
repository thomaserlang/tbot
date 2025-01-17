import asyncio
import random
from datetime import datetime
from typing import Optional

import aiohttp
import bottom
from aioredis import Redis

from tbot import config, logger, utils
from tbot.twitch_bot import bot_sender
from tbot.twitch_bot.unpack import rfc2812_handler


class Client(bottom.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rate_limit_count = 0
        self.rate_limit_bucket = []
        self.is_running = False
        self.raw_handlers = [rfc2812_handler(self)]
        self.ahttp = None
        self.db = None
        self.redis: Optional[Redis] = None
        self.redis_sub = None
        self.pong_check_task = None
        self.ping_task = None
        self.starttime = datetime.utcnow()
        self.user = None
        self.bot_sender = None

        self.host = config.data.twitch.irc_host
        self.port = config.data.twitch.irc_port
        self.ssl = config.data.twitch.irc_use_ssl

    def send(self, command: str, **kwargs) -> None:
        if self.rate_limit_count < config.data.twitch.irc_rate_limit:
            if command == 'PRIVMSG' and bot.bot_sender:
                bot.bot_sender.send(command, **kwargs)
            else:
                super().send(command, **kwargs)
            self.rate_limit_count += 1
        else:
            self.rate_limit_bucket.append(
                {
                    'command': command,
                    'kwargs': kwargs,
                }
            )
            logger.warning(
                f'Rate limit reached. In queue: {len(self.rate_limit_bucket)}'
            )

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

    async def send_ping(self, time=None):
        await asyncio.sleep(random.randint(120, 240) if not time else time)
        logger.debug('Sending ping')
        if self.pong_check_task:
            self.pong_check_task.cancel()
        self.pong_check_task = asyncio.create_task(self.wait_for_pong())
        self.send('PING')

    async def wait_for_pong(self):
        await asyncio.sleep(10)
        logger.error("Didn't receive a PONG in time, reconnecting")
        await self.connect()

    async def connect(self) -> None:
        if self.ping_task:
            self.ping_task.cancel()
        self.ping_task = asyncio.create_task(self.send_ping(10))
        return await super().connect()


bot = Client('a', 0)


@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    if not bot.is_running:
        bot.ahttp = aiohttp.ClientSession()
        bot.loop.create_task(bot.rate_limit_reset_runner())
        bot.user = await utils.twitch_current_user(bot.ahttp)
        bot.redis_sub = await bot.redis.subscribe('tbot:server:commands')
        bot.loop.create_task(receive_redis_server_commands())
        bot.is_running = True

        bot_sender.setup(bot)
        bot.loop.create_task(bot_sender.bot_sender.connect())

    logger.info(
        'IRC Connecting to {}:{} as {}'.format(
            config.data.twitch.irc_host,
            config.data.twitch.irc_port,
            bot.user['login'],
        )
    )
    try:
        if config.data.twitch.chat_token:
            bot.send('PASS', password='oauth:{}'.format(config.data.twitch.chat_token))
        bot.send('NICK', nick=bot.user['login'])
        bot.send('USER', user=bot.user['login'], realname=bot.user['login'])
    except RuntimeError:
        # Didn't connect for some reason, try again
        await asyncio.sleep(5)
        asyncio.create_task(bot.connect(**kwargs))
        return

    # Don't try to join channels until the server has
    # sent the MOTD, or signaled that there's no MOTD.
    done, pending = await asyncio.wait(
        [bot.wait('RPL_ENDOFMOTD'), bot.wait('ERR_NOMOTD')],
        loop=bot.loop,
        return_when=asyncio.FIRST_COMPLETED,
    )

    bot.send_raw('CAP REQ :twitch.tv/tags')
    bot.send_raw('CAP REQ :twitch.tv/commands')
    bot.send_raw('CAP REQ :twitch.tv/membership')

    for future in pending:
        future.cancel()
    bot.trigger('AFTER_CONNECTED')


async def receive_redis_server_commands():
    sub = bot.redis_sub[0]
    while await sub.wait_message():
        try:
            msg = await sub.get_json()
            logger.debug('Received server command: {}'.format(msg))
            if len(msg) < 2:
                return
            cmd = msg.pop(0)

            bot.trigger('REDIS_SERVER_COMMAND', cmd=cmd, cmd_args=msg)

        except:
            logger.exception('receive_redis_server_commands')


@bot.on('CLIENT_DISCONNECT')
async def disconnect(**kwargs):
    logger.info('Disconnected')


@bot.on('PING')
def keepalive(message, **kwargs):
    logger.debug('Received ping, sending PONG back')
    bot.send('PONG', message=message)


@bot.on('PONG')
async def pong(message, **kwargs):
    logger.debug('Received pong')
    if bot.pong_check_task:
        bot.pong_check_task.cancel()
    if bot.ping_task:
        bot.ping_task.cancel()
    bot.ping_task = asyncio.create_task(bot.send_ping())


bot.channels = {}


@bot.on('AFTER_CONNECTED')
async def join(**kwargs):
    bot.channels = await get_channels()
    # From what I can find you are allowed to
    # join 50 channels every 15 seconds
    for c in bot.channels.values():
        bot.send('JOIN', channel='#' + c['name'])
        asyncio.create_task(utils.twitch_save_mods(bot, c['channel_id']))
        await asyncio.sleep(0.20)
    bot.trigger('AFTER_CHANNELS_JOINED')
    asyncio.create_task(timer_update_mods())


async def timer_update_mods():
    await asyncio.sleep(1800)
    asyncio.create_task(timer_update_mods())
    for c in bot.channels.values():
        await utils.twitch_save_mods(bot, c['channel_id'])


async def get_channels():
    rows = await bot.db.fetchall("""
    SELECT 
        c.channel_id, c.name, c.muted, c.chatlog_enabled, twitch_scope
    FROM
        twitch_channels c
    WHERE
        c.active="Y";
    """)
    l = {}
    for r in rows:
        l[r['channel_id']] = {
            'channel_id': r['channel_id'],
            'name': r['name'].lower(),
            'muted': r['muted'] == 'Y',
            'chatlog_enabled': r['chatlog_enabled'] == 'Y',
            'twitch_scopes': utils.json_loads(r['twitch_scope'])
            if r['twitch_scope']
            else [],
        }
    return l


@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    try:
        if cmd not in [
            'join',
            'part',
            'mute',
            'unmute',
            'enable_chatlog',
            'disable_chatlog',
        ]:
            return
        c = await bot.db.fetchone(
            'SELECT channel_id, name, muted, chatlog_enabled FROM twitch_channels WHERE channel_id=%s',
            (cmd_args[0]),
        )
        if cmd == 'join':
            bot.send('JOIN', channel='#' + c['name'])
            bot.send('PRIVMSG', target='#' + c['name'], message='/mods')
            bot.channels[c['channel_id']] = {
                'channel_id': c['channel_id'],
                'name': c['name'].lower(),
                'muted': c['muted'] == 'Y',
                'chatlog_enabled': c['chatlog_enabled'] == 'Y',
            }
            bot.send(
                'PRIVMSG',
                target='#' + c['name'],
                message='I have arrived MrDestructoid',
            )
        elif cmd == 'part':
            bot.send('PART', channel='#' + c['name'])
            del bot.channels[c['channel_id']]
            bot.send(
                'PRIVMSG',
                target='#' + c['name'],
                message='I have been asked to leave FeelsBadMan',
            )
        elif cmd == 'unmute':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['muted'] = False
        elif cmd == 'mute':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['muted'] = True
        elif cmd == 'enable_chatlog':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['chatlog_enabled'] = True
        elif cmd == 'disable_chatlog':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['chatlog_enabled'] = False
    except:
        logger.exception('redis_server_command')
