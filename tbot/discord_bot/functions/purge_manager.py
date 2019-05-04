import logging
from ..var_filler import fills_vars, Send_break, Send_error, Send
from tbot import utils
from discord import Forbidden

@fills_vars('purge_manager')
async def purge_manager(bot, message, args, **kwargs):
    limit = 20
    if len(args) > 0:
        try:
            limit = int(args[-1])+1
        except ValueError:
            pass    
    def check(m):
        if m.id == message.id:
            return False
        if not message.mentions:
            return True
        return m.author in message.mentions
    try:
        purged = await message.channel.purge(
            limit=limit,
            check=check,
        )
    except Forbidden:
        raise Send_error(
            'I\'m missing permission `manage_messages`'\
            ' and `read_message_history`'
        )
    raise Send('purged {}'.format(
        utils.pluralize(len(purged), 'message')
    ))