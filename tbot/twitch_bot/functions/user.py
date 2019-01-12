from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils

@fills_vars('user')
async def user(display_name, args, **kwargs):
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
    return {
        'user': user,
    }