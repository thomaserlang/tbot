import logging, pytz
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils
from datetime import datetime

@fills_vars('time')
async def time(bot, var_args, **kwargs):
    if 'time' not in var_args or not var_args['time']:
        raise Send_error('A timezone must be specified with time. Example {time Europe/Copenhagen}')
    if var_args['time'][0] not in pytz.all_timezones:
        raise Send_error('Invalid timezone. Valid list: https://docs.botashell.com/vars/time')
    dt = pytz.utc.localize(
        datetime.utcnow(),
    ).astimezone(pytz.timezone(var_args['time'][0]))
    return {
        'time': dt.strftime('%H:%M:%S')
    }