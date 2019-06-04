import discord
from ..var_filler import fills_vars, Send_break, Send_error
from datetime import datetime
from tbot import utils
from .ban_manager import get_user_ids

def user_info(prefix, user):
    return {
        f'{prefix}.id': user.id,
        f'{prefix}.name': user.name,
        f'{prefix}.display_name': user.display_name,
        f'{prefix}.mention': user.mention,

        f'{prefix}.created_at': user.created_at.isoformat()[0:19] + ' UTC',
        f'{prefix}.created_time_since': \
            utils.seconds_to_pretty((datetime.now()-user.created_at).total_seconds()),

        f'{prefix}.joined_at': user.joined_at.isoformat()[0:19] + ' UTC' \
            if hasattr(user, 'joined_at') and user.joined_at else 'Unknown',
        f'{prefix}.joined_time_since': \
            utils.seconds_to_pretty((datetime.now()-user.joined_at).total_seconds()) \
                if hasattr(user, 'joined_at') and user.joined_at else 'Unknown',
    }

def user_fields(prefix):
    return (
        f'{prefix}.mention',
        f'{prefix}.name',
        f'{prefix}.id',
        f'{prefix}.display_name',
        f'{prefix}.created_at',
        f'{prefix}.created_time_since',
        f'{prefix}.joined_at',
        f'{prefix}.joined_time_since',
    )

@fills_vars(*user_fields('author'))
async def author(bot, message, **kwargs):
    return user_info('author', message.author)

@fills_vars(*user_fields('user'))
async def user(bot, message, args, **kwargs):
    user = message.author
    if args:
        ids = get_user_ids(args)
        if ids:
            user = message.guild.get_member(int(ids[0])) or \
                bot.get_user(int(ids[0]))
            if not user:
                raise Send_error('User was not found')
    return user_info('user', user)

@fills_vars('user_card')
async def user_card(bot, message, args, **kwargs):
    user = message.author
    if args:
        ids = get_user_ids(args)
        if ids:
            user = message.guild.get_member(int(ids[0])) or \
                bot.get_user(int(ids[0]))
            if not user:
                raise Send_error('User was not found')

    embed = discord.Embed()
    embed.colour = discord.colour.Colour.blue()
    embed.title = user.display_name

    created = utils.seconds_to_pretty((datetime.now()-user.created_at).total_seconds()) + ' ago'
    joined = utils.seconds_to_pretty((datetime.now()-user.joined_at).total_seconds()) + ' ago' \
                if hasattr(user, 'joined_at') and user.joined_at else None
    embed.add_field(name='Created', value=created, inline=False)
    embed.add_field(
        name='Joined', 
        value=joined if joined else 'Not a member of this server',
        inline=False,
    )

    await message.channel.send(embed=embed)
    raise Send_break()