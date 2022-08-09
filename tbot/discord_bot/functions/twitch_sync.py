from ..var_filler import fills_vars, Send_break, Send_error
from tbot.discord_bot.tasks.twitch_sync import Twitch_sync_channel
from tbot import utils

@fills_vars('twitch.sync')
async def twitchsync(bot, message, **kwargs):
    if not message.author.guild_permissions.manage_roles:
        return
    
    info = await bot.db.fetchone(
        'SELECT * FROM twitch_channels WHERE discord_server_id=%s;',
        (message.guild.id)
    )
    if not info:
        raise Send_error('This discord server is not connected to a Twitch channel')
    message = await message.channel.send('Syncing, please wait...')
    info = await Twitch_sync_channel(info, bot).sync()

    text = 'Sync complete.'
    if info['added_roles']:
        text += ' Added {} to {}.'.format(
            utils.pluralize(info['added_roles'], 'role'),
            utils.pluralize(info['added_users'], 'user'),
        )
    if info['removed_roles']:
        text += ' Removed {} from {}.'.format(
            utils.pluralize(info['removed_roles'], 'role'),
            utils.pluralize(info['removed_users'], 'user'),
        )
    if not info['removed_roles'] and not info['added_roles'] and not info['errors']:
        text += ' There was nothing to change.'

    if info['errors'][:10]:
        text += '\n\n **Errors**:'
        text += '```'
        for error in info['errors']:
            text += '{}\n\n'.format(error)
        text += '```'
    await message.edit(content=text)
    raise Send_break()