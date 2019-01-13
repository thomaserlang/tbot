from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils

@fills_vars('user')
async def user(bot, display_name, args, **kwargs):
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        user_id = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
        if not user_id:
            user = display_name
    return {
        'user': user,
    }