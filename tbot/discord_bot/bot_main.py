import logging, aiohttp, aiomysql
import sqlalchemy as sa
from sqlalchemy_aio import ASYNCIO_STRATEGY
from tbot import config
from tbot.discord_bot import bot
import tbot.discord_bot.commands
import tbot.discord_bot.tasks

@bot.event
async def on_connect():
    if not hasattr(bot, 'ahttp'):
        bot.ahttp = aiohttp.ClientSession()
        bot.pool = await aiomysql.create_pool(
            host=config['mysql']['host'], 
            port=config['mysql']['port'],
            user=config['mysql']['user'], 
            password=config['mysql']['password'],
            db=config['mysql']['database'], 
            loop=bot.loop,
            charset='utf8mb4',
            use_unicode=True,
            echo=False,
        )

def main():
    bot.loop.create_task(tbot.discord_bot.tasks.twitch_sync.twitch_sync())
    bot.run(config['discord']['token'], bot=config['discord']['bot'])

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')    
    logger.set_logger('discord.log')

    main()