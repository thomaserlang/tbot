import time, logging
from tbot.twitch_bot.var_filler import fills_vars, Send_error, Send, Send_break
from tbot import utils, config

def get_queue_key(var_args, var, channel_id, default='twitch'):
    queue_name = utils.safe_username('_'.join(var_args.get(var, None) or [default]))
    return f'tbot:twitch:queue:{channel_id}:{queue_name}'.lower()

@fills_vars('user_queue.join', 'user_queue.join_pos')
async def user_queue_join(bot, channel_id, var_args, user_id, display_name, **kwargs):
    key = get_queue_key(var_args, 'user_queue.join', channel_id)
    keypos = get_queue_key(var_args, 'user_queue.join_pos', channel_id)
    p = await bot.redis.zrank(keypos, user_id)
    if p == None:
        await bot.redis.zadd(key, time.time(), user_id)
        p = await bot.redis.zrank(keypos, user_id)
    return {
        'user_queue.join': display_name,
        'user_queue.join_pos': str(p+1),
    }

@fills_vars('user_queue.unjoin', 'user_queue.unjoin_count', 'user_queue.unjoin_count_text')
async def user_queue_unjoin(bot, channel_id, var_args, user_id, display_name, **kwargs):
    key = get_queue_key(var_args, 'user_queue.unjoin', channel_id)
    keycount = get_queue_key(var_args, 'user_queue.unjoin_count', channel_id)
    if keycount == 'twitch':
        keycount = get_queue_key(var_args, 'user_queue.unjoin_count_text', channel_id)
    r = await bot.redis.zrem(key, user_id)
    if not r:
        raise Send_error(f'You are not in the queue.')
    c = await bot.redis.zcount(keycount)
    return {
        'user_queue.unjoin': display_name,
        'user_queue.unjoin_count': str(c),
        'user_queue.unjoin_count_text': utils.pluralize(c, 'user'),
    }

@fills_vars('user_queue.count', 'user_queue.count_text')
async def user_queue_count(bot, channel_id, var_args, user_id, **kwargs):
    key = get_queue_key(var_args, 'user_queue.count', channel_id)
    c = await bot.redis.zcount(key)
    return {
        'user_queue.count': str(c),
        'user_queue.count_text': utils.pluralize(c, 'user'),
    }

@fills_vars('user_queue.pos')
async def user_queue_pos(bot, channel_id, var_args, user_id, display_name, args, **kwargs):
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
        if not uid:
            user = display_name
        else:
            user_id = uid 
    key = get_queue_key(var_args, 'user_queue.pos', channel_id)
    p = await bot.redis.zrank(key, user_id)
    if p == None:
        raise Send_error(f'{user} is not in the queue.')
    return {
        'user_queue.pos': str(p+1),
    }

@fills_vars('user_queue.top_5')
async def user_queue_top_5(bot, channel_id, var_args, user_id, **kwargs):
    key = get_queue_key(var_args, 'user_queue.top_5', channel_id)

    top = await bot.redis.zrange(key, 0, 4)
    top = [i.decode('utf8') for i in top]
    users = await utils.twitch_lookup_from_user_id(bot.ahttp, bot.db, top)
    usersbyid = {u['id']: u['user'] for u in users}
    l = []
    for i, userid in enumerate(top):
        l.append(f'{i+1}. {usersbyid[userid]}')

    return {
        'user_queue.top_5': ' - '.join(l),
    }

@fills_vars('user_queue_admin.next', 'user_queue_admin.next_count',
    'user_queue_admin.next_count_text')
async def user_queue_admin_next(bot, channel_id, var_args, user_id, **kwargs):
    key = get_queue_key(var_args, 'user_queue_admin.next', channel_id)
    keycount = get_queue_key(var_args, 'user_queue_admin.next_count', channel_id)
    if keycount == 'twitch':
        keycount = get_queue_key(var_args, 'user_queue_admin.next_count_text', channel_id)

    top = await bot.redis.zrange(key, 0, 0)
    if not top:
        raise Send_error('No users in the queue.')
    user = top[0].decode('utf8')
    users = await utils.twitch_lookup_from_user_id(bot.ahttp, bot.db, [user])
    await bot.redis.zrem(key, user)
    c = await bot.redis.zcount(keycount)
    return {
        'user_queue_admin.next': users[0]['user'],
        'user_queue_admin.next_count': str(c),
        'user_queue_admin.next_count_text': utils.pluralize(c, 'user'),
    }

@fills_vars('user_queue_admin.remove', 'user_queue_admin.remove_count',
    'user_queue_admin.remove_count_text')
async def user_queue_admin_remove(bot, cmd, channel_id, var_args, args, user_id, **kwargs):
    key = get_queue_key(var_args, 'user_queue_admin.remove', channel_id)
    keycount = get_queue_key(var_args, 'user_queue_admin.remove_count', channel_id)
    if keycount == 'twitch':
        keycount = get_queue_key(var_args, 'user_queue_admin.remove_count_text', channel_id)

    if len(args) != 1:
        raise Send_error(f'Syntax error. Use !{cmd} username')

    user = utils.safe_username(args[0])
    uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
    if not uid:
        raise Send_error(f'Unknown user: {user}')
    a = await bot.redis.zrem(key, uid)
    if not a:
        raise Send_error(f'{user} is not in the queue.')

    c = await bot.redis.zcount(keycount)
    return {
        'user_queue_admin.remove': user,
        'user_queue_admin.remove_count': str(c),
        'user_queue_admin.remove_count_text': utils.pluralize(c, 'user'),
    }

@fills_vars('user_queue_admin.promote')
async def user_queue_admin_promote(bot, channel_id, var_args, args, **kwargs):
    key = get_queue_key(var_args, 'user_queue_admin.promote', channel_id)

    if len(args) != 1:
        raise Send_error(f'Syntax error. Use !{cmd} username')

    user = utils.safe_username(args[0])
    uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
    if not uid:
        raise Send_error(f'Unknown user: {user}')

    top = await bot.redis.zrange(key, 0, 0, withscores=True)
    if not top:
        t = time.time()
    else:
        t = top[0][1] - 1

    await bot.redis.zadd(key, t, uid)

    return {
        'user_queue_admin.promote': user,
    }

@fills_vars('user_queue_admin.add', 'user_queue_admin.add_pos')
async def user_queue_admin_add(bot, channel_id, var_args, args, **kwargs):
    key = get_queue_key(var_args, 'user_queue_admin.add', channel_id)
    keypos = get_queue_key(var_args, 'user_queue_admin.add_pos', channel_id)

    if len(args) != 1:
        raise Send_error(f'Syntax error. Use !{cmd} username')

    user = utils.safe_username(args[0])
    uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
    if not uid:
        raise Send_error(f'Unknown user: {user}')

    p = await bot.redis.zrank(keypos, uid)
    if p == None:
        await bot.redis.zadd(key, time.time(), uid)
        p = await bot.redis.zrank(keypos, uid)

    return {
        'user_queue_admin.add': user,
        'user_queue_admin.add_pos': str(p+1),
    }

@fills_vars('user_queue_admin.clear')
async def user_queue_admin_clear(bot, channel_id, var_args, **kwargs):
    key = get_queue_key(var_args, 'user_queue_admin.clear', channel_id)
    await bot.redis.delete(key)
    return {
        'user_queue_admin.clear': '',
    }
