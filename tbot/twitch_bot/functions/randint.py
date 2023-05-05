import re
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from random import randint

@fills_vars('randint',)
async def countdown(bot, var_args, args, **kwargs):
    from_ = 1
    to = 100
    try:
        if 'randint' in var_args:
            num_args = [arg for arg in var_args['randint'] if re.match(r'^[0-9]+$', arg)]
            if len(num_args) == 1:
                to = int(num_args[0])
            elif len(num_args) > 1:
                from_ = int(num_args[0])
                to = int(num_args[1])

        num_args = [re.sub(r'^[^0-9]+', '', arg) for arg in args if re.match(r'^[0-9]+', arg)]
        if len(num_args) == 1:
            to = int(num_args[0])
        elif len(num_args) > 1:
            from_ = int(num_args[0])
            to = int(num_args[1])
    except ValueError:
        raise Send_error('Arguments must be integers')

    if to <= from_:
        raise Send_error('First argument must be lower than the second')
    
    return {
        'randint': randint(from_, to),
    }