import logging, aiohttp
import sqlalchemy as sa
from sqlalchemy_aio import ASYNCIO_STRATEGY
from tbot import config
from tbot.discord_bot.twitch_sync import twitch_sync
from tbot.discord_bot import bot
import tbot.discord_bot.commands 

@bot.event
async def on_ready():
    bot.ahttp = aiohttp.ClientSession()

def main():
    bot.conn = sa.create_engine(config['sql_url'],
        convert_unicode=True,
        echo=False,
        pool_recycle=3599,
        encoding='UTF-8',
        connect_args={'charset': 'utf8mb4'},
        strategy=ASYNCIO_STRATEGY,
    )
    bot.loop.create_task(twitch_sync(bot))
    bot.run(config['discord']['token'], bot=config['discord']['bot'])

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')    
    logger.set_logger('discord.log')

    main()