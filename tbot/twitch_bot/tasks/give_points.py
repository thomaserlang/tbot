import logging, asyncio, json
from tbot import config, utils
from tbot.twitch_bot.bot_main import bot

_started = False
sub_plan_multiplier = {
    'Prime': 1,
    '1000': 1,
    '2000': 2,
    '3000': 5,
}

@bot.on('AFTER_CHANNELS_JOINED')
async def connect(**kwargs):
    global _started
    if not _started:
        _started = True
        bot.loop.create_task(give_points_runner())

async def give_points_runner(): 
    while True:
        await asyncio.sleep(config['twitch']['check_channels_every'])
        bot.loop.create_task(give_points())

@bot.on('USERNOTICE')
async def give_points_for_sub(**kwargs):
    if kwargs['msg-id'] not in ('sub', 'resub', 'subgift', 
        'giftpaidupgrade', 'extendsub'):
        return

    data = await bot.db.fetchone('''
        SELECT  
            points_per_sub
        FROM 
            twitch_channel_point_settings
        WHERE
            channel_id=%s and enabled=1;
    ''', (kwargs['room-id'],))

    if not data:
        return
    if data['points_per_sub'] == 0:
        return

    await add_user_points(
        kwargs['room-id'], 
        kwargs['user-id'],
        kwargs['login'],
        data['points_per_sub']*sub_plan_multiplier.get(kwargs.get('msg-param-sub-plan', 1), 1),
    )

@bot.on('PRIVMSG')
async def give_points_for_cheer(**kwargs):
    if 'cheer' not in kwargs:
        return

    data = await bot.db.fetchone('''
        SELECT  
            points_per_cheer
        FROM 
            twitch_channel_point_settings
        WHERE
            channel_id=%s and enabled=1;
    ''', (kwargs['room-id'],))

    if not data:
        return
    if data['points_per_cheer'] == 0:
        return

    await add_user_points(
        kwargs['room-id'], 
        kwargs['user-id'],
        kwargs['user'],
        int(kwargs['cheer'])*data['points_per_cheer'],
    )

async def give_points():
    settings = await bot.db.fetchall('''
        SELECT channel_id, points_name, points_per_min, 
            points_per_min_sub_multiplier, ignore_users
        FROM
            twitch_channel_point_settings
        WHERE
            enabled=1;
    ''')
    for s in settings:
        if s['channel_id'] not in bot.channels_check:
            continue
        channel = bot.channels_check[s['channel_id']]
        if not channel['is_streaming']:
            continue
        bot.loop.create_task(give_points_channel(
            s['channel_id'], 
            int(config['twitch']['check_channels_every'] / 60) * s['points_per_min'],
            json.loads(s['ignore_users']),
        ))

async def give_points_channel(channel_id, points, ignore_users):
    ignore_users = [u.lower() for u in ignore_users]
    data = []
    for u in bot.channels_check[channel_id]['users']:
        if u['user'] in ignore_users:
            continue
        data.append((
            channel_id,
            u['id'],
            u['user'],
            points
        ))
    await bot.db.executemany('''
        INSERT INTO twitch_user_channel_points (channel_id, user_id, user, points) 
        VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE points=points+VALUES(points), user=VALUES(user);
    ''', data)


async def add_user_points(channel_id, user_id, user, points):
    if points == 0:
        return
    c = await bot.db.execute('''
        UPDATE twitch_user_channel_points 
        SET 
            points=points+%s
        WHERE
            channel_id=%s AND
            user_id=%s;
        ''', (points, channel_id, user_id))
    if not c.rowcount:
        await bot.db.execute('''
            INSERT INTO twitch_user_channel_points
                (channel_id, user_id, user, points)
            VALUES 
                (%s, %s, %s, %s)
        ''', (channel_id, user_id, user, points,))
    return await get_user_points(channel_id, user_id)

async def get_user_points(channel_id, user_id):
    d = await bot.db.fetchone('''
        SELECT points FROM twitch_user_channel_points
        WHERE channel_id=%s and user_id=%s;
    ''', (channel_id, user_id,))
    return d['points'] if d else 0