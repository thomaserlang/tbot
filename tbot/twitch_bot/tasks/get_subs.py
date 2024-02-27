from datetime import datetime, timezone
import aiohttp
from tbot import db, logger
from tbot.utils.twitch import twitch_channel_token_request


async def get_subs():
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
                subs = await _get_subs(bot, c['channel_id'])
                await insert_subs(bot, c['channel_id'], subs)
            except Exception as e:
                logger.exception(e)
    finally:
        await bot.ahttp.close()
        bot.db.pool.close()
        await bot.db.pool.wait_closed()

            
async def _get_subs(bot, channel_id: str):
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


async def insert_subs(bot, channel_id: str, subs: list):
    data = []
    updated_at = datetime.now(tz=timezone.utc)
    for sub in subs:
        data.append((
            channel_id,
            updated_at,
            updated_at,
            sub['user_id'],
            sub['tier'],
            sub['gifter_id'],
            sub['is_gift'],
        ))
    await bot.db.executemany('''
        INSERT INTO twitch_subs 
            (channel_id, created_at, updated_at, user_id, tier, gifter_id, is_gift)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            updated_at=VALUES(updated_at),
            user_id=VALUES(user_id),
            tier=VALUES(tier),
            gifter_id=VALUES(gifter_id),
            is_gift=VALUES(is_gift)
    ''', data)
    await bot.db.execute('''
        delete from twitch_subs where channel_id=%s and updated_at < %s
    ''', (channel_id, updated_at.replace(microsecond=0)))