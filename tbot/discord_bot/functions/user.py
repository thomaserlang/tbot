from ..var_filler import fills_vars, Send_break, Send_error

@fills_vars('user')
async def user(bot, message, **kwargs):
    return {
        'user': message.author.mention,
    }