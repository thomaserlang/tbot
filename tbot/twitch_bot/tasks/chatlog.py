from datetime import datetime, timedelta, timezone

from tbot import logger, utils
from tbot.twitch_bot.bot_base import bot


@bot.on('PRIVMSG')
async def message(nick, target, message, **kwargs):
    if not bot.channels[kwargs['room-id']]['chatlog_enabled']:
        return
    bot.loop.create_task(
        save(
            1,
            target,
            kwargs['room-id'],
            kwargs['user'],
            kwargs['user-id'],
            message,
            kwargs['id'],
            kwargs['display-name'],
            kwargs['color'],
            kwargs['emotes'],
        )
    )

    if not message.startswith('!'):
        return

    is_mod = 'moderator' in kwargs['badges'] or 'broadcaster' in kwargs['badges']
    if is_mod and message == '!updatemods':
        await utils.twitch_save_mods(bot, kwargs['room-id'])
        if not bot.channels[kwargs['room-id']]['muted']:
            bot.send('PRIVMSG', target=target, message='Affirmative, {}'.format(nick))


async def save(
    type_,
    channel,
    channel_id,
    user,
    user_id,
    message,
    msg_id,
    display_name,
    user_color,
    emotes,
):
    try:
        now = datetime.utcnow()
        bot.loop.create_task(
            bot.db.execute(
                """
            INSERT INTO twitch_chatlog (type, created_at, channel_id, user, user_id, message, word_count, msg_id) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
                (
                    type_,
                    now,
                    channel_id,
                    user,
                    user_id,
                    message,
                    len(message.split(' ')),
                    msg_id,
                ),
            )
        )

        c = await bot.db.execute(
            """
            UPDATE twitch_user_chat_stats SET chat_messages=chat_messages+1 
            WHERE channel_id=%s AND user_id=%s
        """,
            (
                channel_id,
                user_id,
            ),
        )
        if not c.rowcount:
            bot.loop.create_task(
                bot.db.execute(
                    """
                INSERT INTO twitch_user_chat_stats (channel_id, user_id, chat_messages) 
                VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE chat_messages=chat_messages+1
            """,
                    (
                        channel_id,
                        user_id,
                    ),
                )
            )

        dt = now + timedelta(days=30)
        u = await bot.db.execute(
            'UPDATE twitch_usernames SET user_id=%s, expires=%s WHERE user=%s',
            (
                user_id,
                dt,
                user,
            ),
        )
        if not u.rowcount:
            bot.loop.create_task(
                bot.db.execute(
                    """
                INSERT INTO twitch_usernames (user_id, expires, user)
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE user=VALUES(user), expires=VALUES(expires)
            """,
                    (
                        user_id,
                        dt,
                        user,
                    ),
                )
            )
    except Exception:
        logger.exception('sql')
    try:
        if bot.redis:
            await bot.redis.publish_json(
                f'tbot:live_chat:{channel_id}',
                {
                    'type': 'message',
                    'provider': 'twitch',
                    'user_id': user_id,
                    'user': display_name,
                    'message': message,
                    'created_at': datetime.now(tz=timezone.utc).isoformat(),
                    'user_color': user_color,
                    'emotes': emotes,
                },
            )
    except Exception:
        logger.exception('sql')
