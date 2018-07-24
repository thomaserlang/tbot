import sqlalchemy as sa
import logging
import discord
from tbot import utils
from tbot.discord_bot import bot
from tbot.discord_bot.tasks.twitch_sync import twitch_sync_channel

@bot.command(description='Sync subscriber roles from twitch. Must have `Manage roles` permission to use.')
async def twitchsync(ctx):
    if not ctx.message.author.guild_permissions.manage_roles:
        return
    
    q = await bot.conn.execute(sa.sql.text(
        'SELECT * FROM channels WHERE discord_server_id=:discord_server_id;'), {
        'discord_server_id': ctx.guild.id,
    })
    info = await q.fetchone()

    if not info:
        return
    info = dict(info)

    msg = await ctx.send('Syncing, please wait...')
    info = await twitch_sync_channel(info)

    message = 'Sync complete.'
    if info['added_roles']:
        message += ' Added {} to {}.'.format(
            utils.pluralize(info['added_roles'], 'role'),
            utils.pluralize(info['added_users'], 'user'),
        )
    if info['removed_roles']:
        message += ' Removed {} from {}.'.format(
            utils.pluralize(info['removed_roles'], 'role'),
            utils.pluralize(info['removed_users'], 'user'),
        )
    if not info['removed_roles'] and not info['added_roles'] and not info['errors']:
        message += ' There was nothing to change.'

    if info['errors'][:10]:
        message += '\n\n **Errors**:'
        message += '```'
        for error in info['errors']:
            message += '{}\n\n'.format(error)
        message += '```'
    await msg.edit(content=message)