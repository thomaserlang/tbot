from tbot.twitch_bot.var_filler import fills_vars, Send_break
from tbot.twitch_bot.tasks.command import db_command
import logging

@fills_vars('alias')
async def alias(var_args, channel, **kwargs):
    for cmd in var_args['alias']:
        await db_command(cmd, '#'+channel, data=kwargs)
    raise Send_break()