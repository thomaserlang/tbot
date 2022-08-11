from datetime import datetime, timedelta
from tbot.twitch_bot.bot_base import bot
from tbot import utils, logger

@bot.on('PRIVMSG')
async def message(nick, target, message, **kwargs):
    if not bot.channels[kwargs['room-id']]['chatlog_enabled']:
        return

    bot.loop.create_task(
        save(1, target, kwargs['room-id'], kwargs['user'], kwargs['user-id'], message, kwargs['id'])
    )

    if not message.startswith('!'):
        return

    is_mod = 'moderator' in kwargs['badges'] or 'broadcaster' in kwargs['badges']
    if is_mod and message == '!updatemods':
        bot.send("PRIVMSG", target=target, message='/mods')
        if not bot.channels[kwargs['room-id']]['muted']:
            bot.send("PRIVMSG", target=target, message='Affirmative, {}'.format(nick))

async def save(type_, channel, channel_id, user, user_id, message, msg_id):
    try:
        now = datetime.utcnow()
        bot.loop.create_task(bot.db.execute('''
            INSERT INTO twitch_chatlog (type, created_at, channel_id, user, user_id, message, word_count, msg_id) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            type_,
            now,
            channel_id,
            user,
            user_id,
            message,
            len(message.split(' ')),
            msg_id,
        )))
        
        c = await bot.db.execute('''
            UPDATE twitch_user_chat_stats SET chat_messages=chat_messages+1 
            WHERE channel_id=%s AND user_id=%s
        ''', (channel_id, user_id,))
        if not c.rowcount:
            bot.loop.create_task(bot.db.execute('''
                INSERT INTO twitch_user_chat_stats (channel_id, user_id, chat_messages) 
                VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE chat_messages=chat_messages+1
            ''', (channel_id, user_id,)))

        dt = now + timedelta(days=30)
        u = await bot.db.execute(
            'UPDATE twitch_usernames SET user_id=%s, expires=%s WHERE user=%s',
            (user_id, dt, user,)
        )
        if not u.rowcount:
            bot.loop.create_task(bot.db.execute('''
                INSERT INTO twitch_usernames (user_id, expires, user)
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE user=VALUES(user), expires=VALUES(expires)
            ''', (user_id, dt, user,)
            ))
    except:
        logger.exception('sql')

@bot.on('NOTICE')
async def notice(target, message, **kwargs):
    if 'msg-id' not in kwargs:
        return

    if kwargs['msg-id'] == 'room_mods':
        bot.loop.create_task(save_mods(target, message))

async def save_mods(target, message):
    a = message.split(':')
    channel = target.strip('#')
    if len(a) == 2:
        mods = [b.strip() for b in a[1].split(',')]
    else:
        mods = []
    mods.append(channel)
    channel_id = None
    for c in bot.channels.values():
        if c['name'].lower() == channel:
            channel_id = c['channel_id'] 

    users = await utils.twitch_lookup_usernames(bot.ahttp, bot.db, mods)
    if users == None:
        return
    data = []
    for u in users:
        data.append((
            channel_id,
            u['id'],
        ))
    await bot.db.execute('DELETE FROM twitch_channel_mods WHERE channel_id=%s;', 
        (channel_id,)
    )
    await bot.db.executemany(
        'INSERT INTO twitch_channel_mods (channel_id, user_id) VALUES (%s, %s);', 
        data
    )