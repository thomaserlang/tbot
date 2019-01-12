import logging, asyncio
from datetime import datetime
from tbot import config, db
from tbot.twitch_bot.bot_base import bot
from tbot.twitch_bot import commands, tasks, functions

bot.channels = {}

@bot.on('AFTER_CONNECTED')
async def join(**kwargs):
    bot.channels = await get_channels()
    # From what I can find you are allowed to 
    # join 50 channels every 15 seconds
    for c in bot.channels.values():
        bot.send('JOIN', channel='#'+c['name'])
        bot.send("PRIVMSG", target='#'+c['name'], message='/mods')
        await asyncio.sleep(0.20)
    bot.trigger('AFTER_CHANNELS_JOINED')

async def get_channels():
    rows = await bot.db.fetchall('''
    SELECT 
        c.channel_id, c.name, c.muted, c.chatlog_enabled
    FROM
        twitch_channels c
    WHERE
        c.active="Y";
    ''')
    l = {}
    for r in rows:
        l[r['channel_id']] = {
            'channel_id': r['channel_id'],
            'name': r['name'].lower(),
            'muted': r['muted'] == 'Y',
            'chatlog_enabled': r['chatlog_enabled'] == 'Y',
        }
    return l

@bot.on('REDIS_SERVER_COMMAND')
async def redis_server_command(cmd, cmd_args):
    try:
        if cmd not in ['join', 'part', 'mute', 'unmute', 'enable_chatlog', 'disable_chatlog']:
            return
        c = await bot.db.fetchone(
            'SELECT channel_id, name, muted, chatlog_enabled FROM twitch_channels WHERE channel_id=%s', 
            (cmd_args[0])
        )
        if cmd == 'join':
            bot.send('JOIN', channel='#'+c['name'])
            bot.send("PRIVMSG", target='#'+c['name'], message='/mods')
            bot.channels[c['channel_id']] = {
                'channel_id': c['channel_id'],
                'name': c['name'].lower(),
                'muted': c['muted'] == 'Y',
                'chatlog_enabled': c['chatlog_enabled'] == 'Y',
            }
            bot.send("PRIVMSG", target='#'+c['name'], message='I have arrived MrDestructoid')
        elif cmd == 'part':
            bot.send('PART', channel='#'+c['name'])
            del bot.channels[c['channel_id']]
            bot.send("PRIVMSG", target='#'+c['name'], message='I have been asked to leave FeelsBadMan')
        elif cmd == 'unmute':                
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['muted'] = False
        elif cmd == 'mute':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['muted'] = True
        elif cmd == 'enable_chatlog':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['chatlog_enabled'] = True
        elif cmd == 'disable_chatlog':
            if c['channel_id'] in bot.channels:
                bot.channels[c['channel_id']]['chatlog_enabled'] = False
    except:
        logging.exception('redis_server_command')

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')
    logger.set_logger('bot.log')

    loop = asyncio.get_event_loop()
    loop.create_task(bot.connect())
    loop.run_forever()