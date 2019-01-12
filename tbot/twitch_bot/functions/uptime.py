from tbot.twitch_bot.var_filler import fills_vars
from tbot import utils

@fills_vars('uptime')
async def uptime(bot, channel_id, **kwargs):
    return {
        'uptime': utils.seconds_to_pretty(
            bot.channels_check[channel_id]['uptime']
        )
    }