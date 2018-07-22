import logging, re
import sqlalchemy as sa
from tbot import config, utils

subs = {}
async def log_sub(bot, nick, target, message, **kwargs):
    if not subs:
        for channel in bot.channels:
            subs[channel] = {}
        q = await bot.conn.execute('SELECT * FROM subscribers')
        rows = await q.fetchall()
        for r in rows:
            subs[r['channel_id']][r['user_id']] = r['months']
    if kwargs['subscriber'] == '1':
        months = None
        for b in kwargs['badges'].split(','):
            b2 = b.split('/')
            if b2[0] == 'subscriber':
                months = int(b2[1])
                break
        user_id = int(kwargs['user-id'])
        channel_id = int(kwargs['room-id'])
        if months != None:
            if user_id not in subs[channel_id] or \
                subs[channel_id][user_id] != months:
                await bot.conn.execute(sa.sql.text('''
                    INSERT INTO subscribers (channel_id, user_id, months) 
                    VALUES (:channel_id, :user_id, :months) ON DUPLICATE KEY UPDATE months=VALUES(months)
                '''), {
                    'channel_id': channel_id,
                    'user_id': user_id,
                    'months': months,
                })
                subs[channel_id][user_id] = months