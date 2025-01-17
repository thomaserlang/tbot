import asyncio
import logging

from tbot import logger
from tbot.twitch_bot import var_filler
from tbot.twitch_bot.bot_base import bot
from tbot.utils.twitch import Twitch_request_error

cmds = []
_cmd_lookup = {}


def command(cmd, alias=None, arg_desc=None):
    def wrapper(f):
        wrapped = f
        if not asyncio.iscoroutinefunction(wrapped):
            wrapped = asyncio.coroutine(wrapped)
        d = {
            'func': wrapped,
            'cmd': cmd,
            'alias': alias,
            'arg_desc': arg_desc,
        }
        cmds.append(d)
        _cmd_lookup[cmd] = d
        if alias:
            _cmd_lookup[alias] = d

    return wrapper


@bot.on('PRIVMSG')
def handle_command(nick, target, message, **kwargs):
    if not message.startswith('!'):
        return
    if nick == bot.user['login']:
        return
    args = message.split(' ')
    cmd = args.pop(0).lower().strip('!')
    if cmd == bot.user['login']:
        cmd = '__thebotname'
    logging.info(kwargs)
    if kwargs['source-room-id'] and kwargs['source-room-id'] != kwargs['room-id']:
        return
    if cmd in _cmd_lookup:
        f = _cmd_lookup[cmd]['func']
        bot.loop.create_task(
            f(
                bot=bot,
                nick=nick,
                channel=target.strip('#'),
                channel_id=kwargs['room-id'],
                target=target,
                message=message,
                args=args,
                **kwargs,
            )
        )
    bot.loop.create_task(
        twitch_command(
            cmd=cmd,
            target=target,
            data={
                'bot': bot,
                'args': args,
                'user': kwargs['user'],
                'display_name': kwargs['display-name'] or kwargs['user'],
                'user_id': kwargs['user-id'],
                'channel': target.strip('#'),
                'channel_id': kwargs['room-id'],
                'badges': kwargs['badges'],
                'emotes': kwargs['emotes'],
                'cmd': cmd,
            },
        )
    )


async def twitch_command(cmd, target, data):
    msg = await db_command(
        cmd=cmd,
        data=data,
    )
    if msg:
        bot.send('PRIVMSG', target=target, message=msg)


async def db_command(cmd, data):
    cmds = await bot.db.fetchall(
        """
        SELECT 
            cmd, response, user_level, global_cooldown, 
            user_cooldown, mod_cooldown, enabled_status
        FROM twitch_commands
        WHERE channel_id=%s AND cmd=%s AND enabled=1
        ORDER BY user_level DESC, enabled_status DESC, id ASC
    """,
        (data['channel_id'], cmd),
    )
    if not cmds:
        return
    user_level = await get_user_level(
        data['badges'],
        data['user_id'],
        data['channel_id'],
        max([cmd['user_level'] for cmd in cmds]),
    )
    for cmd in cmds:
        try:
            if user_level < cmd['user_level']:
                continue

            if cmd['enabled_status'] > 0 and cmd[
                'enabled_status'
            ] != get_enabled_status(data['channel_id']):
                continue

            cd = await has_cooldown(
                cmd=cmd['cmd'],
                channel_id=data['channel_id'],
                user_id=data['user_id'],
                user_level=user_level,
                user_cooldown=cmd['user_cooldown'],
                mod_cooldown=cmd['mod_cooldown'],
                global_cooldown=cmd['global_cooldown'],
            )
            if cd:
                continue
            data.setdefault('cmd_history', []).append(cmd['cmd'])
            msg = await var_filler.fill_message(cmd['response'], **data)
            return msg
        except (var_filler.Send_error, var_filler.Send) as e:
            return '@{}, {}'.format(data['display_name'], e)
        except var_filler.Send_break:
            pass
        except Twitch_request_error as e:
            return str(e)
        except Exception as e:
            logger.exception(str(e))


async def get_user_level(badges, user_id, channel_id, required_level):
    if 'broadcaster' in badges:
        return 9
    if required_level == 8:
        r = await bot.db.fetchone(
            'SELECT user_id FROM twitch_channel_admins WHERE channel_id=%s AND user_id=%s',
            (
                channel_id,
                user_id,
            ),
        )
        if r:
            return 8
    if 'moderator' in badges:
        return 7
    if 'vip' in badges:
        return 2
    if 'subscriber' in badges:
        return 1
    return 0


async def has_cooldown(
    cmd, channel_id, user_id, user_level, user_cooldown, mod_cooldown, global_cooldown
):
    keys = []

    global_cooldown_key = 'tbot:cooldown:{}:{}:global'.format(channel_id, cmd)
    keys.append({'key': global_cooldown_key, 'expire': global_cooldown})

    user_cooldown_key = 'tbot:cooldown:{}:{}:user:{}'.format(channel_id, cmd, user_id)
    keys.append({'key': user_cooldown_key, 'expire': user_cooldown})

    mod_key = 'tbot:cooldown:{}:{}:mod:{}'.format(channel_id, cmd, user_id)
    keys.append({'key': mod_key, 'expire': mod_cooldown})

    r = bot.redis.multi_exec()
    if user_level < 7:
        if global_cooldown:
            r.get(global_cooldown_key)
        if user_cooldown:
            r.get(user_cooldown_key)
    else:
        r.get(mod_key)

    result = await r.execute()
    if result and any(result):
        return True

    r = bot.redis.multi_exec()
    for k in keys:
        if k['expire']:
            r.setex(k['key'], k['expire'], '1')
    await r.execute()

    return False


def get_enabled_status(channel_id):
    if bot.channels_check[channel_id]['is_streaming']:
        return 1
    return 2
