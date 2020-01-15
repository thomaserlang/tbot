import logging
import urllib.parse
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import config

@fills_vars('lol.summoner', 'lol.rank', 'lol.tier', 'lol.lp',
    'lol.wins', 'lol.losses')
async def lol_rank(bot, channel, args, var_args, **kwargs):   
    if not var_args or not var_args.get('lol.summoner') or \
        len(var_args['lol.summoner']) != 2:
        raise Send_error('{lol.summoner "<name>" "<region>"} is missing')


    headers = {
        'X-Riot-Token': config['riot_apikey'],
    }

    summoner = var_args['lol.summoner'][0]
    region = var_args['lol.summoner'][1]
    if region.upper() not in regions:
        raise Send_error(f'Invalid region "{region}". Valid regions: {", ".join(regions)}')

    url = f'https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        d = await r.json()
        encrypted_id = d['id']

    url = f'https://{region.lower()}.api.riotgames.com//lol/league/v4/entries/by-summoner/{encrypted_id}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        d = await r.json()
    logging.info(d)
    r = {
        'lol.summoner': '',
        'lol.rank': 'Unranked',
        'lol.tier': '',
        'lol.lp': '0',
        'lol.wins': '0',
        'lol.losses': '0',
    }

    for a in d:
        if a['queueType'] == 'RANKED_SOLO_5x5':
            r['lol.wins'] = str(a['wins'])
            r['lol.losses'] = str(a['losses'])
            r['lol.rank'] = a['rank']
            r['lol.tier'] = a['tier']            
            r['lol.lp'] = a['leaguePoints']
            break

    return r

regions = [
    'EUW1',
    'RU',
    'KR',
    'BR1',
    'OC1',
    'JP1',
    'NA1',
    'EUN1',
    'TR1',
    'LA1',
    'LA2',
]