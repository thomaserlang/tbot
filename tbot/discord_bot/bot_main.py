import logging, aiohttp, aiomysql
from tbot import config, db
from tbot.discord_bot import bot
import tbot.discord_bot.commands
import tbot.discord_bot.tasks
import tbot.discord_bot.functions

@bot.event
async def on_connect():
    if not hasattr(bot, 'ahttp'):
        bot.ahttp = aiohttp.ClientSession()
        bot.db = await db.Db().connect(bot.loop)

def main():
    log = logging.getLogger('main')
    log.setLevel('INFO')
    bot.loop.create_task(
        tbot.discord_bot.tasks.twitch_sync.twitch_sync()
    )
    log.info('Discord bot started')
    bot.run(config['discord']['token'], bot=config['discord']['bot'])
    log.info('Discord bot stopped')

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')
    logger.set_logger('discord.log')

    main()