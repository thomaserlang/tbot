from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot.twitch_bot.tasks.command import db_command
from tbot import utils
import logging

@fills_vars('cmd_manager')
async def cmd_manager(bot, display_name, args, cmd, channel_id, **kwargs):
    if len(args) < 2:
        raise Send_error('Syntax error, use: !{} add/edit/get/delete [cmd] <response>'.format(cmd))

    method = args.pop(0).lower()
    cmd_name = args.pop(0).lower().strip('!')

    if method == 'add' or method == 'edit':
        if len(args) == 0:
            raise Send_error('Syntax error, use: !{} {} {} <reponse>'.format(cmd, method, cmd_name))
        try:
            utils.validate_cmd(cmd_name)
            utils.validate_cmd_response(' '.join(args))
        except Exception as e:
            raise Send_error(str(e))

    if method == 'add':
        r = await get_cmd(bot, channel_id, cmd_name)
        if r:
            raise Send_error('Cmd "{0}" already exists, use: !{1} edit {0} <response>'.format(cmd_name, cmd))
        await bot.db.execute(
            'INSERT INTO twitch_commands (channel_id, cmd, response) VALUES (%s, %s, %s)',
            (channel_id, cmd_name, ' '.join(args),)
        )
        raise Send_error('!{} successfully saved'.format(cmd_name))

    elif method == 'edit':
        r = await get_cmd(bot, channel_id, cmd_name)
        if not r:
            raise Send_error('Cmd "{0}" does not exist, use !{1} add {0} <response>'.format(cmd_name, cmd))

        await bot.db.execute(
            'UPDATE twitch_commands SET response=%s WHERE channel_id=%s and cmd=%s',
            (' '.join(args), channel_id, cmd_name,)
        )
        raise Send_error('!{} successfully saved'.format(cmd_name))

    elif method == 'delete':
        r = await get_cmd(bot, channel_id, cmd_name)
        if not r:
            raise Send_error('Cmd "{0}" does not exist'.format(cmd_name))
        await bot.db.execute(
            'DELETE FROM twitch_commands WHERE channel_id=%s and cmd=%s',
            (channel_id, cmd_name,)
        )
        raise Send_error('!{} successfully deleted'.format(cmd_name))

    elif method == 'get':
        r = await get_cmd(bot, channel_id, cmd_name)
        if not r:
            raise Send_error('Cmd "{0}" does not exist'.format(cmd_name))
        raise Send_error('{}'.format(r['response']))        

    else:
        raise Send_error('Syntax error, use: !{} add/edit/get/delete [cmd] <response>'.format(cmd))

async def get_cmd(bot, channel_id, cmd):
    r = await bot.db.fetchone(
        'SELECT id, response FROM twitch_commands WHERE channel_id=%s AND cmd=%s LIMIT 1',
        (channel_id, cmd,)
    )
    return r