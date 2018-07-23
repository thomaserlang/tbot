import sqlalchemy as sa
import logging
import discord
from tbot.discord_bot import bot
from tbot.discord_bot.twitch_sync import twitch_sync_channel

@bot.command()
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
    info = await twitch_sync_channel(bot, info)

    message = 'Done. Found {} subs.'.format(info['subs'])
    if info['added_roles']:
        message += ' Added {} roles.'.format(info['added_roles'])
    if info['removed_roles']:
        message += ' Removed {} roles.'.format(info['removed_roles'])

    if info['errors'][:10]:
        message += '\n\n **Errors**:'
        message += '```'
        for error in info['errors']:
            message += '{}\n\n'.format(error)
        message += '```'
    await msg.edit(content=message)