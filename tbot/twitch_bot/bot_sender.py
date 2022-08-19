import bottom, asyncio, random
from tbot.twitch_bot.unpack import rfc2812_handler
from tbot import config, logger

'''
Used for sending messages to channels so we can log 
the bots own messages on the main connection.
'''

bot_sender = bottom.Client('a', 0)
bot_sender.pong_check_task = None
bot_sender.ping_task = None
bot_sender.raw_handlers = [rfc2812_handler(bot_sender)]

def setup(bot):

    bot_sender.host = config.data.twitch.irc_host 
    bot_sender.port = config.data.twitch.irc_port 
    bot_sender.ssl = config.data.twitch.irc_use_ssl

    @bot_sender.on('CLIENT_CONNECT')
    async def connect(**kwargs):
        if bot_sender.pong_check_task:
            bot_sender.pong_check_task.cancel()
        if bot_sender.ping_task:
            bot_sender.ping_task.cancel()
        bot_sender.ping_task = asyncio.create_task(send_ping(10))
        if config.data.twitch.chat_token:
            bot_sender.send('PASS', password='oauth:{}'.format(config.data.twitch.chat_token))
        bot_sender.send('NICK', nick=bot.user['login'])
        bot_sender.send('USER', user=bot.user['login'], realname=bot.user['login'])

        bot.bot_sender = bot_sender

    @bot_sender.on('PING')
    def keepalive(message, **kwargs):
        logger.debug('Received ping, sending PONG back')
        bot_sender.send('PONG', message=message)

    @bot_sender.on('PONG')
    async def pong(message, **kwargs):
        logger.debug('Received pong')
        if bot_sender.pong_check_task:
            bot_sender.pong_check_task.cancel()
        if bot_sender.ping_task:
            bot_sender.ping_task.cancel()
        bot_sender.ping_task = asyncio.create_task(send_ping())

    async def send_ping(time=None):
        await asyncio.sleep(random.randint(120, 240) if not time else time)
        logger.debug('Sending ping')
        if bot_sender.pong_check_task:
            bot_sender.pong_check_task.cancel()
        bot_sender.pong_check_task = asyncio.create_task(wait_for_pong())
        bot_sender.send('PING')

    async def wait_for_pong():
        await asyncio.sleep(10)

        logger.error('Didn\'t receive a PONG in time, reconnecting')
        if bot_sender.ping_task:
            bot_sender.ping_task.cancel()
        bot_sender.ping_task = asyncio.create_task(send_ping())
        await bot_sender.connect()
    
    if bot_sender.pong_check_task:
        bot_sender.pong_check_task.cancel()
    if bot_sender.ping_task:
        bot_sender.ping_task.cancel()
    bot_sender.ping_task = asyncio.create_task(send_ping(5))