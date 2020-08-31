import logging, asyncio, json, copy
from dateutil.parser import parse
from datetime import datetime
from tbot import config, utils
from tbot.twitch_bot.bot_main import bot

"""
Responsible for monitoring a channel's live status
and a user's watch time.

Sets the bot.channels_check with the following info:

bot.channels_check[channel_id] = {
    'is_live': True/False,
    'stream_id': id of the stream id when first detected as live,
    'went_live_at': datetime,
    'went_offline_at_delay': datetime, used by the delay offline
    'users': list({'id': str, 'user': str}) chatters,
    'last_check': datetime,
    'uptime': int of seconds, 
}

"""

_started = None

def channel_extra_default():
    return {
        'is_live': False,
        'is_streaming': False,
        'stream_id': None,
        'went_live_at': None,
        'went_offline_at_delay': None,
        'users': [],
        'last_check': None,
        'uptime': 0,
    }

@bot.on('AFTER_CHANNELS_JOINED')
async def connect(**kwargs):
    global _started
    if not _started:
        _started = True
        bot.channels_check = {}
        for channel_id in bot.channels:
            bot.channels_check[channel_id] = channel_extra_default()
        await load_channels_cache()
        bot.loop.create_task(channels_check_runner())

async def channels_check_runner(): 
    while True:
        bot.loop.create_task(channels_check())
        await asyncio.sleep(config['twitch']['check_channels_every'])

async def channels_check():
    logging.debug('Channels check')
    try:
        for channel_id in bot.channels:
            if channel_id not in bot.channels_check:
                bot.channels_check[channel_id] = channel_extra_default()
        prev_channels_check = copy.deepcopy(bot.channels_check)
        await update_channels_check()
        for channel_id in bot.channels_check.keys():
            bot.loop.create_task(channel_check(
                channel_id, 
                prev_channels_check[channel_id]
            ))
    except:
        logging.exception('channels_check')

async def channel_check(channel_id, prev_channel_check):
    now = datetime.utcnow().replace(microsecond=0)
    bot.channels_check[channel_id]['last_check'] = now    
    is_live = bot.channels_check[channel_id]['is_live']
    await cache_channel(channel_id)

    if prev_channel_check['is_live'] == None:
        return
    if bot.channels_check[channel_id]['went_offline_at_delay']:
        return
    await set_chatters(channel_id)
    if is_live:
        inc_time = time_since_last_check = int(
            (now - (
                prev_channel_check['last_check'] or 
                bot.channels_check[channel_id]['went_live_at']
            )).total_seconds()
        )
        if prev_channel_check['is_live'] != is_live:
            inc_time = int((now - bot.channels_check[channel_id]['went_live_at']).total_seconds())            
            if channel_id in bot.channels:
                logging.info('{} is now live ({} seconds ago)'.format(
                    bot.channels[channel_id]['name'], 
                    inc_time,
                ))
                bot.loop.create_task(send_discord_live_notification(channel_id))
            await save_stream_created(channel_id)
        await inc_watchtime(channel_id, inc_time)
    else:
        if prev_channel_check['is_live'] != is_live:
            if channel_id in bot.channels:
                logging.info('{} went offline'.format(bot.channels[channel_id]['name']))
            await save_stream_ended(prev_channel_check['stream_id'], prev_channel_check['uptime'])
            if prev_channel_check['uptime'] >= int(config['twitch']['stream_min_length']): 
                await reset_streams_in_a_row(channel_id, prev_channel_check['stream_id'])
        # Detect if the bot was parted.
        # Incase the bot is parted doing a live stream we will keep checking
        # until the stream ends.
        if channel_id not in bot.channels:
            del bot.channels_check[channel_id]

async def inc_watchtime(channel_id, inc_time):
    data = []
    if channel_id in bot.channels:
        logging.debug('Increment {} viewers with {} secs'.format(
            bot.channels[channel_id]['name'], 
            inc_time,
        ))
    bot.channels_check[channel_id]['uptime'] += inc_time        
    bot.loop.create_task(cache_channel(channel_id))
    for u in bot.channels_check[channel_id]['users']:
        data.append((
            channel_id,
            u['id'],
            u['user'],
            bot.channels_check[channel_id]['stream_id'],
            inc_time,
        ))
    if data:
        await bot.db.executemany('''
            INSERT INTO twitch_stream_watchtime (channel_id, user_id, user, stream_id, time) 
            VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
        ''', data)

async def cache_channel(channel_id):
    went_live_at = bot.channels_check[channel_id]['went_live_at']
    last_check = bot.channels_check[channel_id]['last_check']
    went_offline_at_delay = bot.channels_check[channel_id]['went_offline_at_delay']
    await bot.db.execute('''
        INSERT INTO twitch_channel_cache (channel_id, data) VALUES (%s, %s) ON DUPLICATE KEY UPDATE data=VALUES(data);
    ''', (
        channel_id,
        json.dumps({
            'is_live': bot.channels_check[channel_id]['is_live'],
            'stream_id': bot.channels_check[channel_id]['stream_id'],
            'went_live_at': went_live_at.isoformat() if went_live_at else None,
            'last_check': last_check.isoformat() if last_check else None,
            'went_offline_at_delay': went_offline_at_delay.isoformat() \
                if went_offline_at_delay else None,
            'uptime': bot.channels_check[channel_id]['uptime'],
        })
    ))

async def load_channels_cache():
    rows = await bot.db.fetchall('SELECT cc.channel_id, cc.data FROM twitch_channel_cache cc, twitch_channels c WHERE c.channel_id=cc.channel_id and c.active="Y";')
    for r in rows:
        data = json.loads(r['data'])
        bot.channels_check[r['channel_id']]['is_live'] = data['is_live']
        bot.channels_check[r['channel_id']]['stream_id'] = data.get('stream_id')
        bot.channels_check[r['channel_id']]['went_live_at'] = \
            parse(data['went_live_at']) if data['went_live_at'] else None
        bot.channels_check[r['channel_id']]['last_check'] = \
            parse(data['last_check']) if data['last_check'] else None
        bot.channels_check[r['channel_id']]['went_offline_at_delay'] = \
            parse(data['went_offline_at_delay']) if data.get('went_offline_at_delay') else None
        bot.channels_check[r['channel_id']]['uptime'] = data['uptime'] if data.get('uptime') else 0

async def set_chatters(channel_id):
    try:
        if channel_id not in bot.channels:
            logging.error('{} not in `bot.channels`'.format(channel_id))
            return
        channel = bot.channels[channel_id]['name']
        async with bot.ahttp.get('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel)) as r:
            if r.status == 200:
                data = await r.json()
                if data['chatter_count'] == 0:
                    return
                usernames = []
                for k in data['chatters']:
                    usernames.extend(data['chatters'][k])
                if usernames:
                    bot.channels_check[channel_id]['users'] = \
                        await utils.twitch_lookup_usernames(bot.ahttp, bot.db, usernames)
    except:
        logging.exception('set_chatters')

async def update_channels_check():
    try:
        streams = {key: None for key in bot.channels_check}
        url = 'https://api.twitch.tv/helix/streams'
        for channel_ids in utils.chunks(list(bot.channels_check.keys()), 100):
            params = [('user_id', str(channel_id)) for channel_id in channel_ids]
            params.append(('first', '100'))
            data = await utils.twitch_request(bot.ahttp, url, params)
            for stream in data['data']:
                streams[stream['user_id']] = stream
        for channel_id, stream in streams.items():
            if stream:                
                bot.channels_check[channel_id]['is_streaming'] = True
                woa = bot.channels_check[channel_id]['went_offline_at_delay']
                if woa:
                    bot.channels_check[channel_id]['went_offline_at_delay'] = None
                    if channel_id in bot.channels:
                        logging.info('{} was detected as online again after {} seconds'.format(
                            bot.channels[channel_id]['name'],
                            int((datetime.utcnow() - woa).total_seconds()),
                        ))
                if bot.channels_check[channel_id]['is_live']:
                    continue
                bot.channels_check[channel_id]['went_live_at'] = parse(stream['started_at']).replace(tzinfo=None)
                bot.channels_check[channel_id]['stream_id'] = stream['id']
                bot.channels_check[channel_id]['is_live'] = True
                bot.channels_check[channel_id]['uptime'] = 0
            else:
                bot.channels_check[channel_id]['is_streaming'] = False
                if not bot.channels_check[channel_id]['is_live']:
                    continue
                if config['twitch']['delay_offline'] and not bot.channels_check[channel_id]['went_offline_at_delay']:
                    if channel_id in bot.channels:
                        logging.info('{} was detected as offline but will be delayed with {} seconds'.format(
                            bot.channels[channel_id]['name'],
                            config['twitch']['delay_offline'],
                        ))
                    bot.channels_check[channel_id]['went_offline_at_delay'] = datetime.utcnow()
                    continue
                woa = bot.channels_check[channel_id]['went_offline_at_delay']
                if woa and int((datetime.utcnow() - woa).total_seconds()) <= \
                    config['twitch']['delay_offline']:
                    continue
                bot.channels_check[channel_id]['is_live'] = False
                bot.channels_check[channel_id]['went_live_at'] = None
                bot.channels_check[channel_id]['stream_id'] = None
                bot.channels_check[channel_id]['went_offline_at_delay'] = None
                bot.channels_check[channel_id]['uptime'] = 0
    except:
        logging.exception('is_live')

async def reset_streams_in_a_row(channel_id, stream_id):
    await bot.db.execute('''
        UPDATE twitch_user_stats
        SET 
            streams_row = 0
        WHERE
            channel_id = %s AND 
            streams_row>0 AND
            last_viewed_stream_id != %s;
    ''', (
        channel_id,
        stream_id,
    ))

async def save_stream_created(channel_id):
    await bot.db.execute('''
        INSERT INTO twitch_streams (stream_id, channel_id, started_at) 
        VALUES (%s, %s, %s);
    ''', (
        bot.channels_check[channel_id]['stream_id'],
        channel_id,
        bot.channels_check[channel_id]['went_live_at'],
    ))

async def save_stream_ended(stream_id, uptime):
    await bot.db.execute('''
        UPDATE twitch_streams SET uptime=%s WHERE stream_id=%s;
    ''', (
        uptime,
        stream_id,
    ))

async def send_discord_live_notification(channel_id):
    webhooks = await bot.db.fetchall('''
        SELECT id, webhook_url, message FROM twitch_discord_live_notification
        WHERE channel_id=%s;
    ''', (channel_id))
    if not webhooks:
        return
    d = {
        'name': bot.channels[channel_id]['name'],
        'url': 'https://twitch.tv/{}'.format(bot.channels[channel_id]['name']),
    }
    for w in webhooks:
        if not w['message'] or not w['webhook_url']:
            continue
        m = w['message']
        for k in d:
            m = m.replace('{'+k+'}', d[k])
        data = {
            'content': m,
            'embeds': [{
                'url': d['url'],
                'image': {
                    'url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1280x720.jpg'.format(
                        bot.channels[channel_id]['name'].lower()
                    ),
                },
                'color': 3447003, #blue
            }],
        }
        try:
            async with bot.ahttp.request('POST', w['webhook_url'], json=data) as r:
                if r.status >= 400:
                    error = await r.text()
                    logging.warning(
                        'Failed to send live notification to id: {} - Error: ({}) {}'.format(
                            w['id'],
                            r.status,
                            error,
                        )
                    )
        except:
            logging.exception('twitch discord webhook-id: {} '.format(
                w['id'],
            ))