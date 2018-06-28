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

@bot.on('AFTER_CHANNEL_JOIN')
async def connect(**kwargs):
    global _channels_check_callback
    if not _channels_check_callback:
        for channel_id in bot.channels:
            bot.channels[channel_id].update({
                'is_live': None,
                'stream_id': None,
                'went_live_at': None,
                'users': [],
                'last_check': None,
            })
        await load_channels_cache()
        _channels_check_callback = bot.loop.create_task(channels_check())

async def start_channels_check_callback():    
    await asyncio.sleep(config['check_channels_every'])
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
    await update_current_stream_metadata(channel_id)
    is_live = bot.channels[channel_id]['is_live']
    await cache_channel(channel_id)
    if old_is_live == None:
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
            await save_stream_ended(old_stream_id)
            await reset_streams_in_a_row(channel_id, old_stream_id)

async def inc_watchtime(channel_id, inc_time):
    data = []
    logging.debug('Increment {} viewers with {} secs'.format(
        bot.channels[channel_id]['name'], 
        inc_time,
    ))
    for u in bot.channels[channel_id]['users']:
        data.append({
            'channel_id': channel_id,
            'user_id': u['id'],
            'user': u['user'],
            'stream_id': bot.channels[channel_id]['stream_id'],
            'inc_time': inc_time,
        })
    if data:
        await bot.conn.execute(sa.sql.text('''
            INSERT INTO stream_watchtime (channel_id, user_id, user, stream_id, time) 
            VALUES (:channel_id, :user_id, :user, :stream_id, :inc_time) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
        '''), data)

async def cache_channel(channel_id):
    went_live_at = bot.channels[channel_id]['went_live_at']
    last_check = bot.channels[channel_id]['last_check']
    await bot.conn.execute(sa.sql.text('''
        INSERT INTO channel_cache (channel_id, data) VALUES (:channel_id, :data) ON DUPLICATE KEY UPDATE data=VALUES(data);
    '''), {
        'channel_id': channel_id,
        'data': json.dumps({
            'is_live': bot.channels[channel_id]['is_live'],
            'stream_id': bot.channels[channel_id]['stream_id'],
            'went_live_at': went_live_at.isoformat() if went_live_at else None,
            'last_check': last_check.isoformat() if last_check else None,
        })
    })

async def load_channels_cache(): 
    q = await bot.conn.execute('SELECT cc.channel_id, cc.data FROM channel_cache cc, channels c WHERE c.channel_id=cc.channel_id and c.active="Y";')
    rows = await q.fetchall()
    for r in rows:
        data = json.loads(r['data'])
        bot.channels[r['channel_id']]['is_live'] = data['is_live']
        bot.channels[r['channel_id']]['stream_id'] = data.get('stream_id')
        bot.channels[r['channel_id']]['went_live_at'] = \
            parse(data['went_live_at']) if data['went_live_at'] else None
        bot.channels[r['channel_id']]['last_check'] = \
            parse(data['last_check']) if data['last_check'] else None

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
                if not bot.channels[channel_id]['is_live']:
                    bot.channels[channel_id]['went_live_at'] = parse(data['data'][0]['started_at']).replace(tzinfo=None)
                    bot.channels[channel_id]['stream_id'] = data['data'][0]['id']
                    bot.channels[channel_id]['is_live'] = True
            else:
                bot.channels[channel_id]['is_live'] = False
                bot.channels[channel_id]['went_live_at'] = None
                bot.channels[channel_id]['stream_id'] = None                
    except:
        logging.exception('is_live')

async def reset_streams_in_a_row(channel_id, stream_id):
    await bot.conn.execute(sa.sql.text('''
        UPDATE user_stats us
                LEFT JOIN
            stream_watchtime uw ON (uw.stream_id = :stream_id
                AND uw.user_id = us.user_id) 
        SET 
            streams_row = 0
        WHERE
            us.channel_id = :channel_id
                AND ISNULL(uw.user_id);
    '''), {
        'stream_id': stream_id,
        'channel_id': channel_id,
    })

async def save_stream_created(channel_id):
    await bot.conn.execute(sa.sql.text('''
        INSERT INTO streams (stream_id, channel_id, started_at) 
        VALUES (:stream_id, :channel_id, :started_at);
    '''), {
        'channel_id': channel_id,
        'stream_id': bot.channels[channel_id]['stream_id'],
        'started_at': bot.channels[channel_id]['went_live_at'],
    })

async def save_stream_ended(stream_id):
    await bot.conn.execute(sa.sql.text('''
        UPDATE streams SET ended_at=:ended_at WHERE stream_id=:stream_id;
    '''), {
        'stream_id': stream_id,
        'ended_at': datetime.utcnow(),
    })