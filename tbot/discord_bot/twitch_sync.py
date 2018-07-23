import logging, asyncio, math
import sqlalchemy as sa
from urllib.parse import urlencode
from dateutil.parser import parse
from datetime import datetime
from tbot import config

async def twitch_sync(bot):
    await bot.wait_until_ready()
    await asyncio.sleep(1)
    while not bot.is_closed():
        try:
            logging.info('Twitch sync')
            q = await bot.conn.execute(sa.sql.text('SELECT * FROM channels WHERE not isnull(discord_server_id) and active="Y";'))
            channels = await q.fetchall()
            for info in channels:
                bot.loop.create_task(twitch_sync_channel(bot, dict(info)))
        except:
            logging.exception('twitch_sync')
        
        await asyncio.sleep(config['discord']['twitch_sync_every'])

running = {}
async def twitch_sync_channel(bot, info):
    returninfo = {
        'errors': [],
        'added_roles': 0,
        'removed_roles': 0,
        'subs': 0,
    }
    server = bot.get_guild(int(info['discord_server_id']))
    if not server:
        logging.error('Discord server id was not found: {}'.format(info['discord_server_id']))
        return
    if running.get(info['channel_id']):
        logging.info('Already syncing {}'.format(info['name']))
        returninfo['errors'].append('Already syncing')
        return returninfo
    running[info['channel_id']] = True
    try:
        try:
            users = await get_twitch_ids(bot, server)
            subs = await get_subscribers(bot, info)
            subs = {int(d['user']['_id']): d for d in subs}
            roles = await get_twitch_roles(bot, server, info)
            roles_ids = [r['role_id'] for r in roles if r['role_id']]
            server_roles = {str(r.id): r for r in server.roles}
            cached_badges = await get_cached_badges_months(bot, info)

            for member in server.members:
                give_roles = []
                try:
                    if str(member.id) not in users:
                        continue
                    twitch_id = users[str(member.id)]
                    if twitch_id not in subs:
                        continue
                    returninfo['subs'] += 1
                    subinfo = subs[twitch_id]
                    subbed_at = parse(subinfo['created_at']).replace(tzinfo=None)
                    seconds = (datetime.utcnow() - subbed_at).total_seconds()
                    months = math.ceil(seconds / 60 / 60 / 24 / 30)
                    if twitch_id in cached_badges and cached_badges[twitch_id]['sub'] != None:
                        if months < cached_badges[twitch_id]['sub']+1:
                            months = cached_badges[twitch_id]['sub']+1
                    time_role = None
                    for role in roles:
                        if not role['role_id']:
                            continue
                        if role['role_id'] not in server_roles:
                            continue
                        if role['type'] == 'sub_tier' and role['value'] == subinfo['sub_plan']:
                            give_roles.append(server_roles[role['role_id']])
                        elif role['type'] == 'sub_time' and months >= int(role['value']):
                            time_role = server_roles[role['role_id']]
                        elif role['type'] == 'sub':
                            give_roles.append(server_roles[role['role_id']])
                    if time_role:
                        give_roles.append(time_role)
                finally:
                    remove_roles = []
                    real_give_roles = []
                    give_roles_ids = [r.id for r in give_roles]
                    give_roles = []
                    for r in member.roles:
                        if str(r.id) in roles_ids:
                            if r.id not in give_roles_ids:
                                remove_roles.append(r)
                    member_roles_ids = [r.id for r in member.roles]
                    for r in give_roles_ids:
                        if r not in member_roles_ids:
                            give_roles.append(server_roles[str(r)])

                    if give_roles:
                        logging.debug('Give roles to {}: {}'.format(member.name, give_roles))
                        for r in give_roles:
                            try:
                                await member.add_roles(r)
                                returninfo['added_roles'] += 1
                            except:
                                e = 'Failed to give role {} to {}'.format(r.name, member.name)
                                logging.exception(e)
                                returninfo['errors'].append(e)
                    if remove_roles:
                        logging.debug('Remove roles from {}: {}'.format(member.name, remove_roles))
                        for r in remove_roles:
                            try:
                                await member.remove_roles(r)
                                returninfo['removed_roles'] += 1
                            except:
                                e = 'Failed to give role {} to {}'.format(r.name, member.name)
                                logging.exception(e)
                                returninfo['errors'].append(e)
        except Exception as e:
            logging.exception('twitch_sync_channel {}'.format(info['name']))
            returninfo['errors'].append(str(e))
    finally:
        running[info['channel_id']] = False
        return returninfo

async def get_twitch_ids(bot, server):
    q = await bot.conn.execute(sa.sql.text(
        'SELECT discord_id, twitch_id FROM users;'
    ))
    rows = await q.fetchall()
    users = {r['discord_id']: r['twitch_id'] for r in rows}

    for user in server.members:
        try:
            if str(user.id) in users and users[str(user.id)]:
                continue
            if str(user.status) == 'offline':
                continue
            data = await discord_request(
                bot.ahttp,
                'https://discordapp.com/api/v6/users/{}/profile'.format(
                user.id
            ))
            if not data:
                continue
            for con in data['connected_accounts']:
                if not con['verified']:
                    continue
                if con['type'] != 'twitch':
                    continue
                users[str(user.id)] = int(con['id'])
                await bot.conn.execute(sa.sql.text('''
                    INSERT IGNORE INTO users (discord_id, twitch_id) VALUES (:discord_id, :twitch_id);
                '''), {
                    'discord_id': user.id,
                    'twitch_id': con['id'],
                })
        except:
            logging.exception('get_twitch_ids')
    return users

async def discord_request(http_session, url, params=None, headers={}):    
    headers.update({
        'Authorization': config['discord']['user_token'] or \
            config['discord']['token']
    })
    async with http_session.get(url, params=params, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            return data

async def get_subscribers(bot, info):
    '''
    return [
        {
            "_id": "e5e2ddc37e74aa9636625e8d2cc2e54648a30418",
            "created_at": "2018-05-21T00:14:13Z",
            "sub_plan": "3000",
            "sub_plan_name": "Channel Subscription (erleperle)",
            "user": {
                "_id": "36981191",
                "bio": "",
                "created_at": "2018-05-21T00:14:13Z",
                "display_name": "ErlePerle",
                "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/mr_woodchuck-profile_image-a8b10154f47942bc-300x300.jpeg",
                "name": "erleperle",
                "type": "asd",
                "updated_at": "2018-07-21T00:14:13Z"
            }
        },
    ]
    '''
    headers = {
        'Authorization': 'OAuth {}'.format(info['twitch_token']),
        'Client-ID': config['client_id'],
        'Accept': 'application/vnd.twitchtv.v5+json',
    }
    url = 'https://api.twitch.tv/kraken/channels/{}/subscriptions'.format(
        info['channel_id']
    )
    params = {
        'offset': 0,
        'limit': 100,
    }
    subs = []
    total = None
    while not total or (params['offset'] <= total):
        async with bot.ahttp.get(url, params=params, headers=headers) as r:
            if r.status == 200:
                data = await r.json()
                subs.extend(data['subscriptions'])
                params['offset'] += params['limit']
                total = data['_total']
            elif r.status == 401:
                await refresh_twitch_token(bot, info)
                d = await get_subscribers(bot, info)
                return d
            else:              
                error = await r.text()
                raise Exception('Error getting subscribers for: {} - Error: {}: {}'.format(
                    info['name'],
                    r.status,
                    error,
                ))
    return subs

async def get_cached_badges_months(bot, info):
    q = await bot.conn.execute(sa.sql.text(
        'SELECT * FROM twitch_badges WHERE channel_id=:channel_id'
    ), {
        'channel_id': info['channel_id'],
    })
    rows = await q.fetchall()
    return {r['user_id']: dict(r) for r in rows}

async def get_twitch_roles(bot, server, info):
    q = await bot.conn.execute(sa.sql.text(
        'SELECT * FROM twitch_discord_roles WHERE channel_id=:channel_id'
    ), {
        'channel_id': info['channel_id'],
    })
    db_roles = await q.fetchall()
    db_roles = [dict(d) for d in db_roles]
    for role in db_roles:
        for r in server.roles:
            if r.name == role['role_name']:
                if role['role_id'] != str(r.id):
                    await bot.conn.execute(sa.sql.text(
                        'UPDATE twitch_discord_roles SET role_id=:role_id WHERE id=:id;'
                    ), {
                        'id': role['id'],
                        'role_id': r.id,
                    })
                    role['role_id'] = str(r.id)
    return db_roles

async def refresh_twitch_token(bot, info):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': info['twitch_refresh_token'],
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
    }
    logging.debug('Refresh token for channel: {}'.format(info['name']))
    async with bot.ahttp.post(url, params=params) as r:
        if r.status == 200:
            data = await r.json()
            await bot.conn.execute(sa.sql.text(
                'UPDATE channels SET twitch_token=:twitch_token, twitch_refresh_token=:twitch_refresh_token WHERE channel_id=:channel_id;'
            ), {
                'channel_id': info['channel_id'],
                'twitch_token': data['access_token'],
                'twitch_refresh_token': data['refresh_token'],
            })
            info['twitch_token'] = data['access_token']
            info['twitch_refresh_token'] = data['refresh_token']
        else:
            error = await r.text()
            raise Exception('Failed to refresh token for channel_id: {} - Error: {}: {}'.format(
                info['name'],
                r.status,
                error,
            ))