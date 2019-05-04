import logging
from ..var_filler import fills_vars, Send_break, Send_error, Send
from tbot import utils
from discord import Forbidden, Object

@fills_vars('ban_manager')
async def ban_manager(bot, message, args, **kwargs):
    user_ids = get_user_ids(args)
    if not user_ids:
        raise Send_error(
            'No user mentioned'
        )
    reason = get_reason(args)
    try:
        for id_ in user_ids:
            await message.guild.ban(Object(id=id_), reason=reason)
        raise Send('Done.')
    except Forbidden:
        raise Send_error(
            'I\'m missing permission `ban_members`'
        )

@fills_vars('unban_manager')
async def unban_manager(bot, message, args, **kwargs):
    user_ids = get_user_ids(args)
    if not user_ids:
        raise Send_error(
            'No user mentioned'
        )
    reason = get_reason(args)
    try:
        for id_ in user_ids:
            await message.guild.unban(Object(id=id_), reason=reason)
        raise Send('Done.')
    except Forbidden:
        raise Send_error(
            'I\'m missing permission `ban_members`'
        )

def get_user_ids(args):
    ids = []
    for a in args:
        if a.startswith('<@') and a.endswith('>'):
            ids.append(a.strip('<@>'))
    return ids

def get_reason(args):
    reason = []
    for a in args:
        if not a.startswith('<@'):
            reason.append(a)
    return ' '.join(reason)