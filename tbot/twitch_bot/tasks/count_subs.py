from datetime import datetime, timezone
import aiohttp
from tbot import db, logger
from tbot.utils.twitch import twitch_channel_token_request


async def count_subs():
    from tbot.twitch_bot.bot_base import bot
    bot.db = await db.Db().connect()
    bot.ahttp = aiohttp.ClientSession()
    try:
        channels = await bot.db.fetchall('''
            SELECT channel_id, twitch_scope 
            FROM twitch_channels 
            WHERE 
                active="Y" AND 
                not isnull(twitch_scope)
        ''')
        logger.info('Counting subs')
        for c in channels:
            if 'channel:read:subscriptions' not in c['twitch_scope']:
                continue
            
            logger.info(f'Channel: {c["channel_id"]}')
            try:
                subs = await get_subs(bot, c['channel_id'])
                await _count_subs(bot, c['channel_id'], subs)
                await insert_subs(bot, c['channel_id'], subs)
            except Exception as e:
                logger.exception(e)
    finally:
        await bot.ahttp.close()
        bot.db.pool.close()
        await bot.db.pool.wait_closed()

            
async def get_subs(bot, channel_id: str):
    url = 'https://api.twitch.tv/helix/subscriptions'
    after = ''
    subs = []
    while True:
        d = await twitch_channel_token_request(bot, channel_id, url, params={
            'broadcaster_id': channel_id,
            'after': after,
        })
        if d['data']:
            subs.extend(d['data'])
        else:
            break
        if not 'pagination' in d or not d['pagination']:
            break
        after = d['pagination']['cursor']
    return subs


async def _count_subs(bot, channel_id: str, subs: list):
    self_subs = 0
    gifted_subs = 0
    primes = 0
    for sub in subs:
        points = 1
        if sub['tier'] == '2000':
            points = 2
        elif sub['tier'] == '3000':
            points = 6

        if sub['is_gift']:
            gifted_subs += points
        elif sub['tier'].lower() == 'prime':
            primes += points
        else:
            self_subs += points
    await bot.db.execute('''
        INSERT INTO twitch_sub_stats 
            (channel_id, self_sub_points, gifted_sub_points, primes, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            self_sub_points=VALUES(self_sub_points),
            gifted_sub_points=VALUES(gifted_sub_points),
            primes=VALUES(primes),
            updated_at=VALUES(updated_at)
    ''', (channel_id, self_subs, gifted_subs, primes, datetime.now(tz=timezone.utc)))


async def insert_subs(bot, channel_id: str, subs: list):
    data = []
    updated_at = datetime.now(tz=timezone.utc)
    for sub in subs:
        data.append((
            channel_id,
            updated_at,
            sub['user_id'],
            sub['plan_name'],
            sub['tier'],
            sub['gifter_id'],
            sub['is_gift'],
        ))
    await bot.db.executemany('''
        INSERT INTO twitch_subs 
            (channel_id, updated_at, user_id, plan_name, tier, gifter_id, is_gift)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            updated_at=VALUES(updated_at),
            user_id=VALUES(user_id),
            plan_name=VALUES(plan_name),
            tier=VALUES(tier),
            gifter_id=VALUES(gifter_id),
            is_gift=VALUES(is_gift)
    ''', data)
    await bot.db.execute('''
        delete from twitch_subs where channel_id=%s and updated_at < %s
    ''', (channel_id, updated_at))