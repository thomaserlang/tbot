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
        'X-Riot-Token': config['lol_apikey'],
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
        account_id = d['accountId']

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
        await get_live(channel_id, bot, headers, region, account_id, r)

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

async def get_live(channel_id, bot, headers, region, account_id, result):
    if not bot.channels_check[channel_id]['went_live_at']:
        return

    url = f'https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        matches = await r.json()

    w = []
    for m in matches['matches']:
        dt = datetime.fromtimestamp(m['timestamp']/1000)
        if dt < bot.channels_check[channel_id]['went_live_at']:
            break
        w.append(count_match(bot, m["gameId"], region, headers, account_id))
    r = await asyncio.gather(*w)
    for t in r:
        if t:
            result['lol.live_wins'] += 1
        else:
            result['lol.live_losses'] += 1

async def count_match(bot, game_id, region, headers, account_id):
    url = f'https://{region}.api.riotgames.com/lol/match/v4/matches/{game_id}'
    async with bot.ahttp.get(url, headers=headers) as r:
        if r.status >= 400:
            error = await r.text()
            raise Send_error(f'Riot error: {error}')
        match = await r.json()
        team_id = 0
        if match['gameDuration'] < 60*10:
            return
        # http://static.developer.riotgames.com/docs/lol/queues.json
        #if match['queueId'] not in [400, 420]:
        #    return
        for p in match['participantIdentities']:
            if p['player']['currentAccountId'] == account_id:
                team_id = 0 if p['participantId'] <= 5 else 1
        if match['teams'][team_id]['win'] == 'Win':
            return True
        else:
            return False

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