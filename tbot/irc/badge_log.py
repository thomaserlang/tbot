import logging, re
import sqlalchemy as sa
from tbot import config, utils

badges = {}
async def badge_log(bot, nick, target, message, **kwargs):
    if not badges:
        for channel in bot.channels:
            badges[channel] = {}
        q = await bot.conn.execute('SELECT * FROM twitch_badges')
        rows = await q.fetchall()
        for r in rows:
            badges[r['channel_id']][r['user_id']] = {
                'sub': r['sub'],
                'bits': r['bits'],
            }
    if not kwargs['badges']:
        return

    sub = None
    bits = None
    for b in kwargs['badges'].split(','):
        b2 = b.split('/')
        if b2[0] == 'subscriber':
            sub = int(b2[1])
        elif b2[0] == 'bits':
            bits = int(b2[1])

    user_id = int(kwargs['user-id'])
    channel_id = int(kwargs['room-id'])

    update = False
    if user_id in badges[channel_id]:
        if badges[channel_id][user_id]['sub'] != sub:
            update = True        
        if badges[channel_id][user_id]['bits'] != bits:
            update = True
    else:
        update = True
        badges[channel_id][user_id] = {}

    if update:
        await bot.conn.execute(sa.sql.text('''
            INSERT INTO twitch_badges (channel_id, user_id, sub, bits) 
            VALUES (:channel_id, :user_id, :sub, :bits) 
            ON DUPLICATE KEY UPDATE sub=VALUES(sub), bits=VALUES(bits)
        '''), {
            'channel_id': channel_id,
            'user_id': user_id,
            'sub': sub,
            'bits': bits,
        })
        badges[channel_id][user_id]['sub'] = sub
        badges[channel_id][user_id]['bits'] = bits