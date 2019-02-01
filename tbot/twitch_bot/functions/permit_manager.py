from tbot.twitch_bot.var_filler import fills_vars, Send_error, Send_break
from tbot import utils

@fills_vars('permit_manager')
async def permit_manager(bot, cmd, args, channel, channel_id, var_args, **kwargs):
    if len(args) < 1:
        raise Send_error('Invalid syntax, use: !{} <user>'.format(cmd))
    user = utils.safe_username(args[0])
    user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
    if not user_id:
        raise Send_error('Unknown user')    
    time = int(var_args['permit'][0]) if 'permit' in var_args and var_args['permit'] else 60
    key = 'tbot:filter:permit:{}:{}'.format(
        channel_id, user_id,
    )
    permit = await bot.redis.setex(key, time, '1')
    bot.send("PRIVMSG", target='#'+channel, message='@{}, you will not receive a timeout for the next {}'.format(
        user, 
        utils.seconds_to_pretty(time) if time > 60 else '{} seconds'.format(time),
    ))
    raise Send_break()