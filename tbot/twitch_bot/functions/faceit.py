import logging
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import config

@fills_vars('faceit.username', 'faceit.elo', 'faceit.level', 
    'faceit.next_level_points', 'faceit.next_level')
async def faceit_elo(bot, channel, args, var_args, **kwargs):
    if not var_args or \
        not 'faceit.username' in var_args or \
        not var_args['faceit.username']:
        raise Send_error('{faceit.username <username>} is missing')

    params = {
        'nickname': var_args['faceit.username'][0]
    }
    headers = {
        'Authorization': f'Bearer {config["faceit_apikey"]}',
    }

    elos = (
        (1, '1'),
        (801, '2'),
        (951, '3'),
        (1101, '4'),
        (1251, '5'),
        (1401, '6'),
        (1551, '7'),
        (1701, '8'),
        (1851, '9'),
        (2001, '10'),
    )

    async with bot.ahttp.get('https://open.faceit.com/data/v4/players', params=params, headers=headers) as r:
        if r.status == 404:
            raise Send_error('Unknow user on Faceit (usernames are case sensitive)')
        elif r.status >= 400:
            error = await r.text()
            raise Send_error(f'Faceit error: {error}')
        d = await r.json()
        if 'csgo' not in d['games']:
            raise Send_error('The user does not have CSGO in their Faceit profile')

        next_level_points = 0
        next_level = 'unknown'
        for i, e in enumerate(elos):
            if e[0] < d['games']['csgo']['faceit_elo']:
                if i+1 < len(elos):
                    next_level = elos[i+1][1]
                    next_level_points = elos[i+1][0] - d['games']['csgo']['faceit_elo']

        return {
            'faceit.username': '',
            'faceit.elo': d['games']['csgo']['faceit_elo'],
            'faceit.level': d['games']['csgo']['skill_level_label'],
            'faceit.next_level_points': next_level_points,
            'faceit.next_level': next_level,
        }