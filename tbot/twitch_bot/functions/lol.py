import urllib.parse, asyncio, logging
from datetime import datetime, timedelta
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import config

@fills_vars('lol.summoner', 'lol.rank', 'lol.tier', 'lol.lp',
    'lol.wins', 'lol.losses', 
    'lol.live_wins', 'lol.live_losses')
async def lol(bot, channel, channel_id, args, var_args, **kwargs):   
    if not var_args or not var_args.get('lol.summoner') or \
        len(var_args['lol.summoner']) != 2:
        raise Send_error('{lol.summoner "<name>" "<region>"} is missing')


    headers = {
        'X-Riot-Token': config.data.lol_apikey,
    }

    summoner = var_args['lol.summoner'][0]
    region = var_args['lol.summoner'][1].lower()
    if region not in regions:
        raise Send_error(f'Invalid region "{region}". Valid regions: {", ".join(regions)}')

    url = f'https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        d = await r.json()
        encrypted_id = d['id']
        puuid = d['puuid']

    r = {
        'lol.summoner': '',
        'lol.rank': 'Unranked',
        'lol.tier': '',
        'lol.lp': 0,
        'lol.wins': 0,
        'lol.losses': 0,
        'lol.live_wins': 0,
        'lol.live_losses': 0,
    }

    rank_vars = ['lol.rank', 'lol.tier', 'lol.lp', 'lol.wins', 'lol.losses']
    if any(a in var_args for a in rank_vars):
        await get_rank(bot, headers, region, encrypted_id, r)

    live_vars = ['lol.live_wins', 'lol.live_losses']
    if any(a in var_args for a in live_vars):
        await get_live(channel_id, bot, headers, region, puuid, r)

    return r


async def get_rank(bot, headers, region, encrypted_id, result):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_id}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        d = await r.json()

    for a in d:
        if a['queueType'] == 'RANKED_SOLO_5x5':
            result['lol.wins'] = a['wins']
            result['lol.losses'] = a['losses']
            result['lol.rank'] = a['rank']
            result['lol.tier'] = a['tier'].title()
            result['lol.lp'] = a['leaguePoints']
            break

async def get_live(channel_id, bot, headers, region, puuid, result):
    if not bot.channels_check[channel_id]['went_live_at']:
        return
    new_region = new_regions[region]    
    url = f'https://{new_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100&startTime={int(bot.channels_check[channel_id]["went_live_at"].timestamp())}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        matches = await r.json()

    w = []
    for m in matches:
        w.append(count_match(bot, m, new_region, headers, puuid))
    r = await asyncio.gather(*w)
    for t in r:
        if t:
            result['lol.live_wins'] += 1
        else:
            result['lol.live_losses'] += 1

async def count_match(bot, game_id, region, headers, puuid):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{game_id}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        match = await r.json()
        if match['info']['gameDuration'] < 60*10:
            return
        for p in match['info']['participants']:
            if p['puuid'] == puuid:
                return p['win']

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

new_regions = {
    'euw1': 'europe',
    'ru': 'europe',
    'kr': 'asia',
    'br1': 'americas',
    'oc1': 'americas',
    'jp1': 'asia',
    'na1': 'americas',
    'eun1': 'europe',
    'tr1': 'europe',
    'la1': 'americas',
    'la2': 'americas',
}