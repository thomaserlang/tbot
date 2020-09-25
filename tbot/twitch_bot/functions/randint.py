from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils
from random import randint

@fills_vars('randint',)
async def countdown(bot, var_args, args, **kwargs):
    from_ = 1
    to = 100
    try:
        if 'randint' in var_args:
            if len(var_args['randint']) == 1:
                to = int(var_args['randint'][0])
            elif len(var_args['randint']) > 1:
                from_ = int(var_args['randint'][0])
                to = int(var_args['randint'][1])
    except ValueError:
        pass
    
    try:
        if len(args) == 1:
            to = int(args[0])
        elif len(args) > 1:
            from_ = int(args[0])
            to = int(args[1])
    except ValueError:
        pass

    if from_ <= to:
        raise Send_error('First argument must be lower than the second')
    
    return {
        'randint': randint(from_, to),
    }