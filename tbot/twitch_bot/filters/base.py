from tbot.twitch_bot.tasks.command import get_user_level
from tbot.twitch_bot import var_filler

async def warn_or_timeout(bot, type_, target, filter_, kwargs):
    respond_data =  {
        'bot': bot,
        'args': [],
        'user': kwargs['user'],
        'display_name': kwargs['display-name'] or kwargs['user'],
        'user_id': kwargs['user-id'],
        'channel': target.strip('#'),
        'channel_id': kwargs['room-id'],
        'badges': kwargs['badges'],
        'emotes': kwargs['emotes'],
        'cmd': '',
    }
    if filter_['warning_enabled'] == 'Y':
        key = 'tbot:filter-{}:warning:{}:{}:{}'.format(
            type_, kwargs['room-id'], kwargs['user-id'], filter_['warning_expire'],
        )
        warned = await bot.redis.get(key)
        if not warned:
            bot.loop.create_task(bot.redis.setex(key, filter_['warning_expire'], '1'))
            bot.send("PRIVMSG", target=target, message='.delete {}'.format(kwargs['id']))
            if filter_['warning_message']:
                msg = await var_filler.fill_message(filter_['warning_message'], **respond_data)
                bot.send("PRIVMSG", target=target, message=msg)
            return

    bot.send("PRIVMSG", target=target, message='.timeout {} {} {}'.format(
        kwargs['user'], 
        filter_['timeout_duration'], 
        '[{}] {} filter'.format(bot.user['display_name'], type_),
    ))
    if filter_['timeout_message']:          
        msg = await var_filler.fill_message(filter_['timeout_message'], **respond_data)          
        bot.send("PRIVMSG", target=target, message=msg)

async def has_permit(bot, kwargs):
    key = 'tbot:filter:permit:{}:{}'.format(
        kwargs['room-id'], kwargs['user-id']
    )
    permit = await bot.redis.get(key)
    return True if permit else False

async def is_excluded(bot, filter_, kwargs):
    if filter_['enabled'] != 'Y':
        return True
    ul = await get_user_level(kwargs['badges'], kwargs['user-id'], kwargs['room-id'], filter_['exclude_user_level'])
    if ul >= filter_['exclude_user_level']:
        return True
    return False