import logging, asyncio, aioredis
from tbot import config, db

async def main():
    from tbot.twitch_bot.bot_base import bot
    from tbot.twitch_bot import commands, modlog, tasks, functions, filters
    bot.db = await db.Db().connect(bot.loop)
    bot.redis = await aioredis.create_redis_pool(
        f'redis://{config.data.redis.host}:{config.data.redis.port}',
        minsize=config.data.redis.pool_min_size, 
        maxsize=config.data.redis.pool_max_size,
    )
    await bot.connect()
    mlog = modlog.Pubsub()
    mlog.db = bot.db
    mlog.redis = await aioredis.create_redis_pool(
        f'redis://{config.data.redis.host}:{config.data.redis.port}',
        minsize=config.data.redis.pool_min_size, 
        maxsize=config.data.redis.pool_max_size,
    )
    mlog.loop.create_task(mlog.run())

    log = logging.getLogger('main')
    log.setLevel('INFO')
    log.info('Twitch bot started')
    await asyncio.Event().wait()
    log.info('Twitch bot stopped')