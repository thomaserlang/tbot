import asyncio, logging, json, aiohttp
try:
    import discord
except ImportError:
    raise Exception('''
        The discord libary must be installed manually:
            pip install https://github.com/Rapptz/discord.py/archive/rewrite.zip
    ''')
import sqlalchemy as sa
from tbot.discord_bot.twitch_sync import twitch_sync
from sqlalchemy_aio import ASYNCIO_STRATEGY
from tbot import config

client = discord.Client()

def main():
    client.conn = sa.create_engine(config['sql_url'],
        convert_unicode=True,
        echo=False,
        pool_recycle=3599,
        encoding='UTF-8',
        connect_args={'charset': 'utf8mb4'},
        strategy=ASYNCIO_STRATEGY,
    )
    client.ahttp = aiohttp.ClientSession()
    client.loop.create_task(twitch_sync(client))
    client.run(config['discord']['token'], bot=config['discord']['bot'])

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')    
    logger.set_logger('discord.log')

    main()