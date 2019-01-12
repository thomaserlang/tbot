from tbot.twitch_bot.var_filler import fills_vars

@fills_vars('channel')
async def basics(channel, **kwargs):
    return {
        'channel': channel,
    }