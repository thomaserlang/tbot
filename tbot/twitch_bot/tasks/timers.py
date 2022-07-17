import asyncio, random
from tbot.twitch_bot.bot_base import bot
from tbot import utils, config
from datetime import datetime, timedelta
from tbot.twitch_bot import var_filler

_started = False

@bot.on('AFTER_CONNECTED')
async def connected(**kwargs):
    global _started
    if not _started:
        _started = True
        bot.loop.create_task(runner())

async def runner():
    while True:
        await asyncio.sleep(config.data.twitch.check_timers_every)
        bot.loop.create_task(check_timers())

async def check_timers():
    timers = await bot.db.fetchall(
        'SELECT *, c.name as channel_name FROM twitch_timers t, twitch_channels c WHERE t.enabled=1 AND t.next_run<=%s AND t.channel_id=c.channel_id',
        (datetime.utcnow(),)
    )
    for t in timers:
        bot.loop.create_task(handle_timer(t))

async def handle_timer(t):
    await bot.db.execute(
        'UPDATE twitch_timers SET next_run=%s WHERE id=%s',(
        datetime.utcnow()+timedelta(minutes=t['interval']),
        t['id']
    ))
    if t['enabled_status'] > 0 and \
        t['enabled_status'] != get_enabled_status(t['channel_id']):
        return
    messages = utils.json_loads(t['messages'])

    if len(messages) > 1:
        # last_sent_message: 0 would mean it has never been sent before
        if t['send_message_order'] == 1:
            pos = t['last_sent_message'] + 1
            if pos > len(messages):
                pos = 1
        elif t['send_message_order'] == 2:
            pos = t['last_sent_message']
            while pos == t['last_sent_message']:
                pos = random.randint(1, len(messages))
    else:
        pos = 1

    await bot.db.execute(
        'UPDATE twitch_timers SET last_sent_message=%s WHERE id=%s',(
        pos,
        t['id']
    ))
    try:
        data = {
            'bot': bot,
            'args': [],
            'user': bot.user['login'],
            'display_name': bot.user['login'],
            'user_id': bot.user['id'],
            'channel': t['channel_name'],
            'channel_id': t['channel_id'],
            'badges': '',
            'emotes': '',
            'cmd': '',
        }
        msg = await var_filler.fill_message(messages[pos-1], **data)
        bot.send("PRIVMSG", target='#'+t['channel_name'], message=msg)
    except var_filler.Send_error as e:
        bot.send("PRIVMSG", target='#'+t['channel_name'], message=str(e))
    except var_filler.Send_break:
        pass

def get_enabled_status(channel_id):
    if bot.channels_check[channel_id]['is_streaming']:
        return 1
    return 2