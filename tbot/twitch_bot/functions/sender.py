from tbot.twitch_bot.var_filler import fills_vars

@fills_vars('sender')
async def sender(display_name, **kwargs):
    return {
        'sender': display_name,
    }