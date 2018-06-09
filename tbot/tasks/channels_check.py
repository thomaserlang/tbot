import logging
import asyncio
import json
import sqlalchemy as sa
from dateutil.parser import parse
from datetime import datetime
from tbot import config, utils
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
        await set_chatters()
        for channel in config['channels']:
            bot.loop.create_task(channel_check(channel))
    except:
        logging.exception('channels_check')

async def channel_check(channel):
    last_check = bot.channels[channel]['last_check']
    now = datetime.utcnow().replace(microsecond=0)
    bot.channels[channel]['last_check'] = now
    old_is_live = bot.channels[channel]['is_live']
    stream_id = bot.channels[channel]['stream_id']    
    is_live = await get_is_live(channel)
    await cache_channel(channel)
    if old_is_live == None:
        return
    if is_live:
        inc_time = time_since_last_check = int((now - last_check).total_seconds())
        if old_is_live != is_live:
            inc_time = int((now - bot.channels[channel]['went_live_at']).total_seconds())
            logging.info('{} is now live ({} seconds ago)'.format(channel, inc_time))
            await save_stream_created(
                channel, 
                bot.channels[channel]['stream_id'], 
                bot.channels[channel]['went_live_at']
            )
        await inc_watchtime(channel, inc_time)
    else:
        if old_is_live != is_live:
            logging.info('{} went offline'.format(channel))
            await save_stream_ended(stream_id)
            await reset_streams_in_a_row(channel, stream_id)

async def inc_watchtime(channel, inc_time):
    data = []
    logging.debug('Increment {} viewers with {} secs'.format(channel, inc_time))
    for u in bot.channels[channel]['users']:
        data.append({
            'user_id': u['id'],
            'user': u['user'], 
            'channel': channel, 
            'stream_id': bot.channels[channel]['stream_id'],
            'inc_time': inc_time,
        })
    if data:
        await bot.conn.execute(sa.sql.text('''
            INSERT INTO stream_watchtime (channel, user_id, user, stream_id, time) 
            VALUES (:channel, :user_id, :user, :stream_id, :inc_time) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
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

async def set_chatters():
    for channel in config['channels']:
        try:
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
                        bot.channels[channel]['users'] = \
                            await utils.twitch_lookup_usernames(bot.http_session, usernames)
        except:
            logging.exception('set_chatters')

async def get_is_live(channel):
    try:
        params = {'user_login': channel}
        url = 'https://api.twitch.tv/helix/streams'
        data = await utils.twitch_request(bot.http_session, url, params)
        if data:
            if data['data']:
                if not bot.channels[channel]['is_live']:
                    bot.channels[channel]['went_live_at'] = parse(data['data'][0]['started_at']).replace(tzinfo=None)
                    bot.channels[channel]['stream_id'] = data['data'][0]['id']
                    bot.channels[channel]['is_live'] = True
            else:
                bot.channels[channel]['is_live'] = False
                bot.channels[channel]['went_live_at'] = None
                bot.channels[channel]['stream_id'] = None                
    except:
        logging.exception('is_live')
    if config['channel_always_live']:
        bot.channels[channel]['is_live'] = True
    return bot.channels[channel]['is_live'] 

async def reset_streams_in_a_row(channel, stream_id):
    await bot.conn.execute(sa.sql.text('''
        UPDATE user_stats us
                LEFT JOIN
            stream_watchtime uw ON (uw.stream_id = :stream_id
                AND uw.user_id = us.user_id) 
        SET 
            streams_row = 0
        WHERE
            us.channel = :channel
                AND ISNULL(uw.user_id);
    '''), {
        'stream_id': stream_id,
        'channel': channel,
    })

async def save_stream_created(channel, stream_id, started_at):
    await bot.conn.execute(sa.sql.text('''
        INSERT INTO streams (stream_id, channel, started_at) 
        VALUES (:stream_id, :channel, :started_at);
    '''), {
        'channel': channel,
        'stream_id': stream_id,
        'started_at': started_at,
    })

async def save_stream_ended(stream_id):
    await bot.conn.execute(sa.sql.text('''
        UPDATE streams SET ended_at=:ended_at WHERE stream_id=:stream_id;
    '''), {
        'stream_id': stream_id,
        'ended_at': datetime.utcnow(),
    })