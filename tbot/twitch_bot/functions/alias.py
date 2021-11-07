from tbot.twitch_bot.var_filler import fills_vars, Send_break
from tbot.twitch_bot.tasks.command import db_command
import logging

@fills_vars('alias')
async def alias(var_args, **kwargs):
    for cmd in var_args['alias']:
        if cmd in kwargs['cmd_history'] or len(kwargs['cmd_history']) > 9:
            continue
        kwargs['cmd_history'].append(cmd)
        await db_command(cmd, '#'+kwargs['channel'], data=kwargs)
    raise Send_break()