import logging
import asyncio
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
                'went_live_at': None,
                'users': [],
                'check_counter': 0,
                'last_check': None,
            }
    global _channels_check_callback
    if _channels_check_callback:
        _channels_check_callback.cancel()
    _channels_check_callback = bot.loop.create_task(channels_check())

async def channels_check():
    bot.loop.create_task(start_channels_check_callback())
    logging.info('Channels check')
    try:
        await get_users()
        for channel in config['channels']:
            old_is_live = bot.channels[channel]['is_live']
            is_live = await get_is_live(channel)
            if old_is_live == None:
                continue
            if is_live:
                inc_time = 60
                if old_is_live != is_live:
                    await reset_stream_watchtime(channel)
                    inc_time = round((datetime.utcnow() - bot.channels[channel]['went_live_at']).total_seconds())
                    logging.info('{} is now live ({} seconds ago)'.format(channel, inc_time))
                await inc_watchtime(channel, inc_time)
            else:
                if old_is_live != is_live:
                    logging.info('{} went offline'.format(channel))
                    await reset_stream_watchtime(channel)
    except:
        logging.exception('channels_check')

async def inc_watchtime(channel, inc_time):
    data = []
    bot.channels[channel]['check_counter'] += 1
    logging.debug('Channel check: {} - count: {}'.format(
        channel,
        bot.channels[channel]['check_counter']
    ))
    for user in bot.channels[channel]['users']:
        data.append({'user': user, 'channel': channel, 'inc_time': inc_time})
    if data:
        await bot.conn.execute(sa.sql.text('''
            INSERT INTO current_stream_watchtime (channel, user, time) 
            VALUES (:channel, :user, :inc_time) ON DUPLICATE KEY UPDATE time=time+VALUES(time);
        '''), data)

async def reset_stream_watchtime(channel):
    await bot.conn.execute(sa.sql.text('''
        DELETE FROM current_stream_watchtime WHERE channel=:channel;
    '''), {
        'channel': channel,
    })
    bot.channels[channel]['check_counter'] = 0

async def start_channels_check_callback():    
    await asyncio.sleep(60)
    global _channels_check_callback
    _channels_check_callback = \
        bot.loop.create_task(channels_check())

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
        async with bot.http_session.get('https://api.twitch.tv/kraken/streams/{}'.format(channel),
            params={'client_id': config['client_id']}) as r:
            if r.status == 200:
                data = await r.json()
                if 'stream' in data:
                    if data['stream']:
                        if not bot.channels[channel]['is_live']:
                            bot.channels[channel]['went_live_at'] = parse(data['stream']['created_at']).replace(tzinfo=None)
                        bot.channels[channel]['is_live'] = True
                    else:
                        bot.channels[channel]['is_live'] = False
                        bot.channels[channel]['went_live_at'] = None
                    bot.channels[channel]['last_check'] = datetime.utcnow()
                    logging.info(bot.channels[channel]['is_live'])
    except:
        logging.exception('is_live')
    if config['channel_always_live']:
        bot.channels[channel]['is_live'] = True
    return bot.channels[channel]['is_live'] 
