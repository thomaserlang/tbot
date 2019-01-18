import logging
import asyncio
import functools
from tbot import config
from tbot.twitch_bot.bot_base import bot
from tbot.twitch_bot import var_filler

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
    if not message.startswith(('!')):
        return
    if nick == bot.user['login']:
        return
    args = message.split(' ')
    cmd = args.pop(0).lower().strip('!')
    if cmd == bot.user['login']:
        cmd = '__thebotname'
    if cmd in _cmd_lookup:
        f = _cmd_lookup[cmd]['func']
        bot.loop.create_task(f(
            bot=bot,
            nick=nick,
            channel=target.strip('#'),
            channel_id=int(kwargs['room-id']),
            target=target,
            message=message,
            args=args,
            **kwargs
        ))
    bot.loop.create_task(db_command(
        cmd=cmd,
        target=target,
        data={
            'bot': bot,
            'args': args,
            'user': kwargs['user'],
            'display_name': kwargs['display-name'] or kwargs['user'],
            'user_id': int(kwargs['user-id']),
            'channel': target.strip('#'),
            'channel_id': int(kwargs['room-id']),
            'badges': kwargs['badges'],
            'emotes': kwargs['emotes'],
            'cmd': cmd,
        }
    ))

async def db_command(cmd, target, data):
    cmds = await bot.db.fetchall('''
        SELECT cmd, response, user_level, global_cooldown, user_cooldown, mod_cooldown, enabled_status
        FROM twitch_commands
        WHERE channel_id=%s AND cmd=%s
        ORDER BY user_level DESC, enabled_status DESC, id ASC
    ''', (data['channel_id'], cmd))
    if not cmds:
        return
    user_level = await get_user_level(data['badges'], data['user_id'], data['channel_id'], max([cmd['user_level'] for cmd in cmds]))
    for cmd in cmds:
        try:
            if user_level < cmd['user_level']:
                continue

            if cmd['enabled_status'] > 0 and cmd['enabled_status'] != get_enabled_status(data['channel_id']):
                continue

            cd = await has_cooldown(cmd=cmd['cmd'], channel_id=data['channel_id'], user_id=data['user_id'], 
                user_level=user_level, user_cooldown=cmd['user_cooldown'], mod_cooldown=cmd['mod_cooldown'],
                global_cooldown=cmd['global_cooldown'])
            if cd:
                continue

            msg = await var_filler.fill_message(cmd['response'], **data)
            bot.send("PRIVMSG", target=target, message=msg)
        except var_filler.Send_error as e:
            bot.send("PRIVMSG", target=target, message='@{}, {}'.format(data['display_name'], e))
        except var_filler.Send_break:
            pass
        except:
            logging.exception('db_command')

async def get_user_level(badges, user_id, channel_id, required_level):
    if 'broadcaster' in badges:
        return 9
    if required_level == 8:
        r = await bot.db.fetchone(
            'SELECT user_id FROM twitch_channel_admins WHERE channel_id=%s AND user_id=%s',
            (channel_id, user_id,)
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

async def has_cooldown(cmd, channel_id, user_id, user_level, user_cooldown, mod_cooldown, global_cooldown):
    if user_level < 7:
        if user_cooldown == 0 and global_cooldown == 0:
            return False
    else:
        if mod_cooldown == 0:
            return False

    r = bot.redis.multi_exec()
    keys = []
    if user_level < 7:
        if global_cooldown:
            k = 'tbot:cooldown:{}:{}:global'.format(channel_id, cmd)
            r.get(k)
            keys.append({'key': k, 'expire': global_cooldown})
        if user_cooldown:
            k = 'tbot:cooldown:{}:{}:user:{}'.format(channel_id, cmd, user_id)
            r.get(k)
            keys.append({'key': k, 'expire': user_cooldown})
    else:
        if mod_cooldown:
            k = 'tbot:cooldown:{}:{}:mod:{}'.format(channel_id, cmd, user_id)
            keys.append({'key': k, 'expire': mod_cooldown})
            r.get(k)
    result = await r.execute()
    if result and any(result):
        return True

    r = bot.redis.multi_exec()
    for k in keys:
        r.setex(k['key'], k['expire'], '1')
    await r.execute()
    return False

def get_enabled_status(channel_id):
    if bot.channels_check[channel_id]['is_streaming']:
        return 1
    return 2