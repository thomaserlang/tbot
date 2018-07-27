import logging
import asyncio
import json
from dateutil.parser import parse
from datetime import datetime
from tbot import config, utils
from tbot.twitch_bot import bot

"""
Responsible for monitoring a channel's live status
and a user's watch time
"""

_channels_check_callback = None

@bot.on('AFTER_CHANNEL_JOIN')
async def connect(**kwargs):
    global _channels_check_callback
    if not _channels_check_callback:
        for channel_id in bot.channels:
            bot.channels[channel_id].update({
                'is_live': None,
                'stream_id': None,
                'went_live_at': None,
                'went_offline_at_delay': None,
                'users': [],
                'last_check': None,
                'uptime': 0,
            })
        await load_channels_cache()
        _channels_check_callback = bot.loop.create_task(channels_check())

async def start_channels_check_callback():    
    await asyncio.sleep(config['twitch']['check_channels_every'])
    global _channels_check_callback
    _channels_check_callback = \
        bot.loop.create_task(channels_check())

async def channels_check():
    bot.loop.create_task(start_channels_check_callback())
    logging.debug('Channels check')
    try:
        await set_chatters()
        for channel_id in bot.channels:
            bot.loop.create_task(channel_check(channel_id))
    except:
        logging.exception('channels_check')

async def channel_check(channel_id):
    last_check = bot.channels[channel_id]['last_check']
    now = datetime.utcnow().replace(microsecond=0)
    bot.channels[channel_id]['last_check'] = now
    old_is_live = bot.channels[channel_id]['is_live']
    old_stream_id = bot.channels[channel_id]['stream_id']
    old_uptime = bot.channels[channel_id]['uptime']
    await update_current_stream_metadata(channel_id)
    is_live = bot.channels[channel_id]['is_live']
    await cache_channel(channel_id)
    if old_is_live == None:
        return
    if bot.channels[channel_id]['went_offline_at_delay']:
        return
    if is_live:
        inc_time = time_since_last_check = int((now - last_check).total_seconds())
        if old_is_live != is_live:
            inc_time = int((now - bot.channels[channel_id]['went_live_at']).total_seconds())
            logging.info('{} is now live ({} seconds ago)'.format(
                bot.channels[channel_id]['name'], 
                inc_time,
            ))
            await save_stream_created(channel_id)
        await inc_watchtime(channel_id, inc_time)
    else:
        if old_is_live != is_live:
            logging.info('{} went offline'.format(bot.channels[channel_id]['name']))
            await save_stream_ended(old_stream_id, old_uptime)
            await reset_streams_in_a_row(channel_id, old_stream_id)

async def inc_watchtime(channel_id, inc_time):
    data = []
    logging.debug('Increment {} viewers with {} secs'.format(
        bot.channels[channel_id]['name'], 
        inc_time,
    ))
    bot.channels[channel_id]['uptime'] += inc_time        
    bot.loop.create_task(cache_channel(channel_id))
    for u in bot.channels[channel_id]['users']:
        data.append((
            channel_id,
            u['id'],
            u['user'],
            bot.channels[channel_id]['stream_id'],
            inc_time,
        ))
    if data:
        await bot.db.executemany('''
            INSERT INTO stream_watchtime (channel_id, user_id, user, stream_id, time) 
            VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
        ''', data)

async def cache_channel(channel_id):
    went_live_at = bot.channels[channel_id]['went_live_at']
    last_check = bot.channels[channel_id]['last_check']
    went_offline_at_delay = bot.channels[channel_id]['went_offline_at_delay']
    await bot.db.execute('''
        INSERT INTO channel_cache (channel_id, data) VALUES (%s, %s) ON DUPLICATE KEY UPDATE data=VALUES(data);
    ''', (
        channel_id,
        json.dumps({
            'is_live': bot.channels[channel_id]['is_live'],
            'stream_id': bot.channels[channel_id]['stream_id'],
            'went_live_at': went_live_at.isoformat() if went_live_at else None,
            'last_check': last_check.isoformat() if last_check else None,
            'went_offline_at_delay': went_offline_at_delay.isoformat() \
                if went_offline_at_delay else None,
            'uptime': bot.channels[channel_id]['uptime'],
        })
    ))

async def load_channels_cache(): 
    rows = await bot.db.fetchall('SELECT cc.channel_id, cc.data FROM channel_cache cc, channels c WHERE c.channel_id=cc.channel_id and c.active="Y";')
    for r in rows:
        data = json.loads(r['data'])
        bot.channels[r['channel_id']]['is_live'] = data['is_live']
        bot.channels[r['channel_id']]['stream_id'] = data.get('stream_id')
        bot.channels[r['channel_id']]['went_live_at'] = \
            parse(data['went_live_at']) if data['went_live_at'] else None
        bot.channels[r['channel_id']]['last_check'] = \
            parse(data['last_check']) if data['last_check'] else None
        bot.channels[r['channel_id']]['went_offline_at_delay'] = \
            parse(data['went_offline_at_delay']) if data.get('went_offline_at_delay') else None
        bot.channels[r['channel_id']]['uptime'] = data['uptime'] if data.get('uptime') else 0

async def set_chatters():
    for channel_id in bot.channels:
        try:
            channel = bot.channels[channel_id]['name']
            async with bot.http_session.get('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel)) as r:
                if r.status == 200:
                    data = await r.json()
                    if data['chatter_count'] == 0:
                        continue
                    usernames = []
                    usernames.extend(data['chatters']['viewers'])
                    usernames.extend(data['chatters']['global_mods'])
                    usernames.extend(data['chatters']['admins'])
                    usernames.extend(data['chatters']['staff'])
                    usernames.extend(data['chatters']['moderators'])
                    if usernames:
                        bot.channels[channel_id]['users'] = \
                            await utils.twitch_lookup_usernames(bot.http_session, usernames)
        except:
            logging.exception('set_chatters')

async def update_current_stream_metadata(channel_id):
    try:
        params = {'user_id': channel_id}
        url = 'https://api.twitch.tv/helix/streams'
        data = await utils.twitch_request(bot.http_session, url, params)
        if data:
            if data['data']:
                woa = bot.channels[channel_id]['went_offline_at_delay']
                if woa:
                    bot.channels[channel_id]['went_offline_at_delay'] = None
                    logging.info('{} was detected as online again after {} seconds'.format(
                        bot.channels[channel_id]['name'],
                        int((datetime.utcnow() - woa).total_seconds()),
                    ))
                if bot.channels[channel_id]['is_live']:
                    return
                bot.channels[channel_id]['went_live_at'] = parse(data['data'][0]['started_at']).replace(tzinfo=None)
                bot.channels[channel_id]['stream_id'] = data['data'][0]['id']
                bot.channels[channel_id]['is_live'] = True
                bot.channels[channel_id]['uptime'] = 0
            else:
                if not bot.channels[channel_id]['is_live']:
                    return
                if config['twitch']['delay_offline'] and not bot.channels[channel_id]['went_offline_at_delay']:
                    logging.info('{} was detected as offline but will be delayed with {} seconds'.format(
                        bot.channels[channel_id]['name'],
                        config['twitch']['delay_offline'],
                    ))
                    bot.channels[channel_id]['went_offline_at_delay'] = datetime.utcnow()
                    return
                woa = bot.channels[channel_id]['went_offline_at_delay']
                if woa and int((datetime.utcnow() - woa).total_seconds()) <= \
                    config['twitch']['delay_offline']:
                    return
                bot.channels[channel_id]['is_live'] = False
                bot.channels[channel_id]['went_live_at'] = None
                bot.channels[channel_id]['stream_id'] = None
                bot.channels[channel_id]['went_offline_at_delay'] = None
                bot.channels[channel_id]['uptime'] = 0
    except:
        logging.exception('is_live')

async def reset_streams_in_a_row(channel_id, stream_id):
    await bot.db.execute('''
        UPDATE user_stats us
            LEFT JOIN
                stream_watchtime uw ON (uw.stream_id = %s
                    AND uw.user_id = us.user_id) 
        SET 
            streams_row = 0
        WHERE
            us.channel_id = %s AND 
            ISNULL(uw.user_id);
    ''', (
        stream_id,
        channel_id,
    ))

async def save_stream_created(channel_id):
    await bot.db.execute('''
        INSERT INTO streams (stream_id, channel_id, started_at) 
        VALUES (%s, %s, %s);
    ''', (
        bot.channels[channel_id]['stream_id'],
        channel_id,
        bot.channels[channel_id]['went_live_at'],
    ))

async def save_stream_ended(stream_id, uptime):
    await bot.db.execute('''
        UPDATE streams SET uptime=%s WHERE stream_id=%s;
    ''', (
        uptime,
        stream_id,
    ))