import logging, random, math, asyncio, json
from tbot import config, utils
from ..var_filler import fills_vars, Send_error, fill_from_dict
from ..tasks.give_points import give_points_channel, get_user_points, add_user_points
from ..bot_main import bot

@fills_vars('gamble_roulette')
async def roulette(bot, channel_id, cmd, user, user_id, display_name, args, **kwargs):
    data = await bot.db.fetchone('''
        SELECT  
            win_chance, win_message, lose_message, 
            allin_win_message, allin_lose_message, 
            min_bet, max_bet,
            points_name
        FROM 
            twitch_gambling_roulette_settings r,
            twitch_channel_point_settings s
        WHERE
            r.channel_id=%s AND
            s.channel_id=r.channel_id
    ''', (channel_id,))
    if not data:
        raise Send_error('Roulette settings has not been setup')
    data['points'] = await get_user_points(channel_id, user_id)
    bet = get_bet(args, data)

    n = random.randint(1, 100)
    d = {
        'bet': bet,
        'points_name': data['points_name'],
        'user': display_name,
    }
    if n <= data['win_chance']:
        d['bet'] = bet
        d['points'] = await add_user_points(channel_id, user_id, user, bet)
        if bet == data['points']:
            msg = fill_from_dict(data['allin_win_message'], d)
        else:
            msg = fill_from_dict(data['win_message'], d)
        await update_stats(channel_id, user_id, 'roulette_wins', 1)

    else:        
        d['points'] = await add_user_points(channel_id, user_id, user, -bet)
        if bet == data['points']:
            msg = fill_from_dict(data['allin_lose_message'], d)
        else:
            msg = fill_from_dict(data['lose_message'], d)
        await update_stats(channel_id, user_id, 'roulette_loses', 1)

    return {
        'gamble_roulette': msg,
    }

@fills_vars('gamble_slots')
async def slots(bot, channel_id, cmd, user, user_id, display_name, args, **kwargs):
    data = await bot.db.fetchone('''
        SELECT  
            win_message, lose_message, 
            allin_win_message, allin_lose_message, 
            min_bet, max_bet,
            points_name,
            emotes, emote_pool_size, payout_percent
        FROM 
            twitch_gambling_slots_settings r,
            twitch_channel_point_settings s
        WHERE
            r.channel_id=%s AND
            s.channel_id=r.channel_id
    ''', (channel_id,))
    if not data:
        raise Send_error('Slots settings has not been setup')
    data['points'] = await get_user_points(channel_id, user_id)
    bet = get_bet(args, data)

    emotes = json.loads(data['emotes'])

    if data['emote_pool_size'] > len(emotes):
        raise Send_error('Too few emotes has been added')

    if data['emote_pool_size'] < len(emotes):
        t = []
        for i in range(data['emote_pool_size']):
            e = random.choice(emotes)
            emotes.remove(e)
            t.append(e)
        emotes = t

    got = [random.choice(emotes) for i in range(3)]
    d = {
        'bet': bet,
        'points_name': data['points_name'],
        'user': display_name,
        'emotes': ' | '.join(got),
    }
    chance = ((len(emotes) / (len(emotes)**3)) * 100)
    multiplier = math.floor(data['payout_percent']/chance) or 1
    if len(set(got)) == 1:
        d['bet'] = bet*multiplier
        d['points'] = await add_user_points(channel_id, user_id, user, d['bet'])
        if bet == data['points']:
            msg = fill_from_dict(data['allin_win_message'], d)
        else:
            msg = fill_from_dict(data['win_message'], d)
        await update_stats(channel_id, user_id, 'slots_wins', 1)
    else:        
        d['points'] = await add_user_points(channel_id, user_id, user, -bet)
        if bet == data['points']:
            msg = fill_from_dict(data['allin_lose_message'], d)
        else:
            msg = fill_from_dict(data['lose_message'], d)
        await update_stats(channel_id, user_id, 'slots_loses', 1)

    return {
        'gamble_slots': msg,
    }

@fills_vars('add_points')
async def cmd_add_points(bot, channel_id, cmd, user, user_id, display_name, args, **kwargs):
    if len(args) < 2:
        raise Send_error(f'Syntax: !{cmd} <user> <amount>')
    try:
        points = int(args[1])
    except:        
        raise Send_error(f'Syntax: !{cmd} <user> <amount>')


    data = await bot.db.fetchone('''
        SELECT  
            points_name, ignore_users
        FROM 
            twitch_channel_point_settings
        WHERE
            channel_id=%s;
    ''', (channel_id,))
    if not data:
        raise Send_error('Channel point settings has not been setup')

    if args[0].lower() == 'all':
        await give_points_channel(channel_id, points, json.loads(data['ignore_users']))
        user_count = len(bot.channels_check[channel_id]['users'])
        msg = f'Added {points} {data["points_name"]} to {user_count} viewers'
    else:
        to_uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))
        if not to_uid:
            raise Send_error('Unknown user')
        p = await add_user_points(channel_id, to_uid, args[0], points)
        msg = f'{args[0]} now has {p} {data["points_name"]}'

    return {
        'add_points': msg,
    }

@fills_vars('give_points')
async def cmd_give_points(bot, channel_id, cmd, user, user_id, display_name, args, **kwargs):
    if len(args) < 2:
        raise Send_error(f'Syntax: !{cmd} <user> <amount>')

    data = await bot.db.fetchone('''
        SELECT  
            points_name
        FROM 
            twitch_channel_point_settings
        WHERE
            channel_id=%s
    ''', (channel_id,))
    if not data:
        raise Send_error('Channel point settings has not been setup')

    points = await get_user_points(channel_id, user_id)
    try:
        give_points = str_bet_to_int(args[1], points)
    except:        
        raise Send_error(f'Syntax: !{cmd} <user> <amount>')

    if give_points > points:
        raise Send_error(f'You only have {points} {data["points_name"]}')
    if give_points < 1:
        raise Send_error(f'Must at least give 1 {data["points_name"]}')

    to_uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, utils.safe_username(args[0]))
    if not to_uid:
        raise Send_error('Unknown user')

    if user_id == to_uid:
        raise Send_error(f'Can\'t give {data["points_name"]} to yourself')

    await asyncio.wait([
        add_user_points(channel_id, user_id, user, -give_points),
        add_user_points(channel_id, to_uid, args[0], give_points),
    ])
    msg = f'{display_name} gave {give_points} {data["points_name"]} to {args[0]}'

    return {
        'give_points': msg,
    }

@fills_vars('points', 'points_rank', 'total_point_users')
async def cmd_points(bot, channel_id, cmd, user, user_id, display_name, args, **kwargs):
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
        if not uid:
            user = display_name
        else:
            user_id = uid 
    data = await bot.db.fetchone('''
        SELECT 
            points, points_rank, total_point_users
        FROM
            twitch_user_channel_points p,
            (SELECT 
                user_id,
                ROW_NUMBER() OVER (ORDER BY points DESC) AS points_rank
            FROM
                twitch_user_channel_points WHERE channel_id=%s) as r,
            (SELECT 
                count(user_id) as total_point_users
            FROM
                twitch_user_channel_points WHERE channel_id=%s) as t
        where p.channel_id=%s AND p.user_id=%s and r.user_id=p.user_id
    ''', (channel_id, channel_id, channel_id, user_id,))
    if not data:
        raise Send_error('Unknown user')
    return data

@fills_vars('points_name')
async def cmd_points_name(bot, channel_id, **kwargs):
    data = await bot.db.fetchone('''
        SELECT  
            points_name
        FROM 
            twitch_channel_point_settings
        WHERE
            channel_id=%s
    ''', (channel_id,))
    if not data:
        raise Send_error('Channel point settings has not been setup')
    return {
        'points_name': data['points_name'],
    }

@fills_vars('points_ranking')
async def cmd_ranking(bot, channel_id, **kwargs):
    data = await bot.db.fetchall('''
        SELECT 
            user,
            points,
            ROW_NUMBER() OVER (ORDER BY points DESC) AS points_rank
        FROM
            twitch_user_channel_points WHERE channel_id=%s
        LIMIT 5
    ''', (channel_id,))
    return {
        'points_ranking': ', '.join(
            [f'{r["points_rank"]}. {r["user"]} ({r["points"]})' for r in data ]
        )
    }


@fills_vars(
    'gambling_stats.slots_wins',
    'gambling_stats.slots_loses',
    'gambling_stats.slots_total_games',
    'gambling_stats.slots_win_percent',
    'gambling_stats.roulette_wins',
    'gambling_stats.roulette_loses',
    'gambling_stats.roulette_total_games',
    'gambling_stats.roulette_win_percent',
)
async def gambling_stats(bot, channel_id, cmd, user, user_id, display_name, args, **kwargs):
    user = display_name
    if len(args) > 0:
        user = utils.safe_username(args[0])
        uid = await utils.twitch_lookup_user_id(bot.ahttp, bot.db, user)
        if not uid:
            user = display_name
        else:
            user_id = uid 
    data = await bot.db.fetchone('''
        SELECT * FROM twitch_gambling_stats
        WHERE channel_id=%s and user_id=%s
    ''', (channel_id, user_id,))

    r = {
        'gambling_stats.slots_wins': 0,
        'gambling_stats.slots_loses': 0,
        'gambling_stats.slots_total_games': 0,
        'gambling_stats.slots_win_percent': '0%',
        'gambling_stats.roulette_wins': 0,
        'gambling_stats.roulette_loses': 0,
        'gambling_stats.roulette_total_games': 0,
        'gambling_stats.roulette_win_percent': '0%',
    }

    if not data:
        return r

    slots_total = data['slots_wins']+data['slots_loses']
    slots_win_percent = '{:.1%}'.format((slots_total/data['slots_wins'])*100) \
        if data['slots_wins'] > 0 else '0%'
    r['gambling_stats.slots_wins'] = data['slots_wins']
    r['gambling_stats.slots_loses'] = data['slots_loses']
    r['gambling_stats.slots_total_games'] = slots_total
    r['gambling_stats.slots_win_percent'] = slots_win_percent

    roulette_total = data['roulette_wins']+data['roulette_loses']
    roulette_win_percent = '{:.1%}'.format((roulette_total/data['roulette_wins'])*100) \
        if data['roulette_wins'] > 0 else '0%'
    r['gambling_stats.roulette_wins'] = data['roulette_wins']
    r['gambling_stats.roulette_loses'] = data['roulette_loses']
    r['gambling_stats.roulette_total_games'] = roulette_total
    r['gambling_stats.roulette_win_percent'] = roulette_win_percent

    return r

def get_bet(args, data):
    if not args:
        bet = data['min_bet']
    else:
        try:
            bet = str_bet_to_int(args[0].lower(), data['points'])        
        except ValueError:
            bet = min_bet

    if bet < 0:
        raise Send_error('Your bet must be a positive number')

    if bet < data['min_bet']:
        raise Send_error(f'A minimum bet of {data["min_bet"]} {data["points_name"]} is required.')

    if bet > data['points']:
        raise Send_error(f'You only have {data["points"]} {data["points_name"]}')

    if data['max_bet'] > 0 and data['max_bet'] < bet:
        bet = data['max_bet']

    return bet

def str_bet_to_int(str_bet, points):
    if str_bet in ['all', 'all-in', 'allin']:
        return points
    if '%' in str_bet:
        p = int(str_bet.strip('%'))
        return int((points / 100) * p)
    return int(str_bet)

async def update_stats(channel_id, user_id, field, value):
    r = await bot.db.execute(f'''
        UPDATE twitch_gambling_stats SET {field}={field}+%s
        WHERE channel_id=%s AND user_id=%s
    ''',
        (value, channel_id, user_id,)
    )

    if r.rowcount == 0:
        await bot.db.execute(f'''
            INSERT INTO twitch_gambling_stats (channel_id, user_id, {field})
            VALUES (%s, %s, %s)
        ''', (channel_id, user_id, value,))