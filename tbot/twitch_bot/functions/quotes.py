from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import config
from datetime import datetime

@fills_vars('quote.add')
async def quote_add(bot, channel_id, cmd, user, user_id, args, **kwargs):
    if len(args) == 0:
        raise Send_error(f'Syntax error, use !{cmd} your quote')

    c = await bot.db.execute(
        'INSERT INTO twitch_quotes '
        '(channel_id, created_by_user_id, created_by_user, '
        'message, enabled, created_at, updated_at) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (channel_id, user_id, user, ' '.join(args), 1, 
            datetime.utcnow(), datetime.utcnow())
    )
    r = await bot.db.fetchone('SELECT number FROM twitch_quotes WHERE id=%s', 
        (c.lastrowid,))
    raise Send_error(f'Quote created with number: {r["number"]}')

@fills_vars('quote.edit')
async def quote_edit(bot, channel_id, cmd, args, **kwargs):
    if len(args) < 2:
        raise Send_error(f'Syntax error, use !{cmd} <number> <new text>')

    n = args.pop(0)

    r = await bot.db.fetchone('SELECT enabled FROM twitch_quotes WHERE channel_id=%s and number=%s', 
        (channel_id, n,))
    if not r:
        raise Send_error('Unknown quote')

    if r['enabled'] == 0:
        raise Send_error('This quote is deleted')

    await bot.db.execute(
        'UPDATE twitch_quotes SET '
        'message=%s, updated_at=%s '
        'WHERE channel_id=%s and number=%s',
        (' '.join(args), datetime.utcnow(), channel_id, n)
    )
    raise Send_error(f'Quote updated')

@fills_vars('quote.delete')
async def quote_delete(bot, channel_id, cmd, args, **kwargs):
    if len(args) != 1:
        raise Send_error(f'Syntax error, use !{cmd} <number>')

    r = await bot.db.fetchone('SELECT enabled FROM twitch_quotes WHERE channel_id=%s and number=%s', 
        (channel_id, args[0],))

    if not r:
        raise Send_error('Unknown quote')

    if r['enabled'] == 0:
        raise Send_error('This quote is deleted')

    await bot.db.execute(
        'UPDATE twitch_quotes SET '
        'enabled=0 '
        'WHERE channel_id=%s AND number=%s',
        (channel_id, args[0],)
    )

    raise Send_error('Quote deleted')

@fills_vars('quote.message', 'quote.number', 'quote.user', 'quote.date')
async def quote_get(bot, args, channel_id, cmd, **kwargs):
    if (args[0].lower() == 'random') or (len(args) == 0):
        r = await bot.db.fetchone('SELECT * FROM twitch_quotes WHERE channel_id=%s and enabled=1 ORDER BY RAND()',
            (channel_id,))
    else:
        r = await bot.db.fetchone('SELECT * FROM twitch_quotes WHERE channel_id=%s and number=%s',
            (channel_id, args[0],))

    if not r:
        raise Send_error('Unknown quote')

    if r['enabled'] == 0:
        raise Send_error('This quote is deleted')

    return {
        'quote.message': r['message'],
        'quote.number': r['number'],
        'quote.user': r['created_by_user'],
        'quote.date': r['created_at'].strftime('%Y-%m-%d'),
    }