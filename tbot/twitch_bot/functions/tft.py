from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import config

@fills_vars('tft.summoner', 'tft.rank', 'tft.tier', 'tft.lp',
    'tft.wins', 'tft.losses')
async def lol(bot, channel, channel_id, args, var_args, **kwargs):   
    if not var_args or not var_args.get('tft.summoner') or \
        len(var_args['tft.summoner']) != 2:
        raise Send_error('{tft.summoner "<name>" "<region>"} is missing')

    headers = {
        'X-Riot-Token': config.data.tft_apikey,
    }
    summoner = var_args['tft.summoner'][0]
    region = var_args['tft.summoner'][1].lower()
    if region not in regions:
        raise Send_error(f'Invalid region "{region}". Valid regions: {", ".join(regions)}')

    url = f'https://{region.lower()}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        d = await r.json()
        encrypted_id = d['id']

    result = {
        'tft.summoner': '',
        'tft.rank': 'Unranked',
        'tft.tier': '',
        'tft.lp': 0,
        'tft.wins': 0,
        'tft.losses': 0,
    }
    
    url = f'https://{region}.api.riotgames.com/tft/league/v1/entries/by-summoner/{encrypted_id}'

    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        d = await r.json()

    for a in d:
        if a['queueType'] == 'RANKED_TFT':
            result['tft.wins'] = a['wins']
            result['tft.losses'] = a['losses']
            result['tft.rank'] = a['rank']
            result['tft.tier'] = a['tier'].title()
            result['tft.lp'] = a['leaguePoints']
            break

    return result


regions = [
    'euw1',
    'ru',
    'kr',
    'br1',
    'oc1',
    'jp1',
    'na1',
    'eun1',
    'tr1',
    'la1',
    'la2',
]