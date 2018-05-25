import logging
import asyncio
import json
import sqlalchemy as sa
from dateutil.parser import parse
from datetime import datetime
from tbot import config
from tbot.irc import bot

"""
Responsible for monitoring a channel's live status
and a user's watch time
"""

_channels_check_callback = None
bot.channels = {}

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    for channel in config['channels']:
        if channel not in bot.channels:
            bot.channels[channel] = {
                'is_live': None,
                'stream_id': None,
                'went_live_at': None,
                'users': [],
                'last_check': None,
                'user': None,
            }
    global _channels_check_callback
    if not _channels_check_callback:
        await load_channels_cache()
        _channels_check_callback = bot.loop.create_task(channels_check())


async def start_channels_check_callback():    
    await asyncio.sleep(60)
    global _channels_check_callback
    _channels_check_callback = \
        bot.loop.create_task(channels_check())

async def channels_check():
    bot.loop.create_task(start_channels_check_callback())
    logging.debug('Channels check')
    try:
        await get_users()
        for channel in config['channels']:
            bot.loop.create_task(channel_check(channel))
    except:
        logging.exception('channels_check')

async def channel_check(channel):
    last_check = bot.channels[channel]['last_check']
    now = datetime.utcnow().replace(microsecond=0)
    bot.channels[channel]['last_check'] = now
    old_is_live = bot.channels[channel]['is_live']
    is_live = await get_is_live(channel)
    await cache_channel(channel)
    if old_is_live == None:
        return
    if is_live:
        inc_time = time_since_last_check = int((now - last_check).total_seconds())
        if old_is_live != is_live:
            inc_time = int((now - bot.channels[channel]['went_live_at']).total_seconds())
            logging.info('{} is now live ({} seconds ago)'.format(channel, inc_time))
        await inc_watchtime(channel, inc_time)
    else:
        if old_is_live != is_live:
            logging.info('{} went offline'.format(channel))

async def inc_watchtime(channel, inc_time):
    data = []
    logging.debug('Increment {} viewers with {} secs'.format(channel, inc_time))
    for user in bot.channels[channel]['users']:
        data.append({
            'user': user, 
            'channel': channel, 
            'stream_id': bot.channels[channel]['stream_id'],
            'inc_time': inc_time,
        })
    if data:
        await bot.conn.execute(sa.sql.text('''
            INSERT INTO current_stream_watchtime (channel, user, stream_id, time) 
            VALUES (:channel, :user, :stream_id, :inc_time) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
        '''), data)

async def cache_channel(channel):
    went_live_at = bot.channels[channel]['went_live_at']
    last_check = bot.channels[channel]['last_check']
    await bot.conn.execute(sa.sql.text('''
        INSERT INTO channel_cache (channel, data) VALUES (:channel, :data) ON DUPLICATE KEY UPDATE data=VALUES(data);
    '''), {
        'channel': channel,
        'data': json.dumps({
            'is_live': bot.channels[channel]['is_live'],
            'stream_id': bot.channels[channel]['stream_id'],
            'went_live_at': went_live_at.isoformat() if went_live_at else None,
            'last_check': last_check.isoformat() if last_check else None,
        })
    })

async def load_channels_cache(): 
    q = await bot.conn.execute('SELECT channel, data FROM channel_cache;')
    rows = await q.fetchall()
    for r in rows:
        data = json.loads(r['data'])
        bot.channels[r['channel']]['is_live'] = data['is_live']
        bot.channels[r['channel']]['stream_id'] = data.get('stream_id')
        bot.channels[r['channel']]['went_live_at'] = \
            parse(data['went_live_at']) if data['went_live_at'] else None
        bot.channels[r['channel']]['last_check'] = \
            parse(data['last_check']) if data['last_check'] else None

async def get_users():
    for channel in config['channels']:
        try:
            async with bot.http_session.get('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel)) as r:
                if r.status == 200:
                    data = await r.json()
                    if data['chatter_count'] == 0:
                        continue
                    users = []
                    users.extend(data['chatters']['viewers'])
                    users.extend(data['chatters']['global_mods'])
                    users.extend(data['chatters']['admins'])
                    users.extend(data['chatters']['staff'])
                    users.extend(data['chatters']['moderators'])
                    if users:
                        bot.channels[channel]['users'] = users
        except:
            logging.exception('get_users')

async def get_is_live(channel):
    try:
        headers = {'Client-ID': config['client_id']}
        params = {'user_login': channel}
        url = 'https://api.twitch.tv/helix/streams'
        async with bot.http_session.get(url, params=params, headers=headers) as r:
            if r.status == 200:
                data = await r.json()
                if data['data']:
                    if not bot.channels[channel]['is_live']:
                        bot.channels[channel]['went_live_at'] = parse(data['data'][0]['started_at']).replace(tzinfo=None)
                    bot.channels[channel]['is_live'] = True
                    bot.channels[channel]['stream_id'] = data['data'][0]['id']
                else:
                    bot.channels[channel]['is_live'] = False
                    bot.channels[channel]['went_live_at'] = None
                    bot.channels[channel]['stream_id'] = None
    except:
        logging.exception('is_live')
    if config['channel_always_live']:
        bot.channels[channel]['is_live'] = True
    return bot.channels[channel]['is_live'] 