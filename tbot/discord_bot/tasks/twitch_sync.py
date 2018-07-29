import logging, asyncio, math
from urllib.parse import urlencode
from dateutil.parser import parse
from datetime import datetime
from tbot import config
from tbot.discord_bot import bot

async def twitch_sync():
    await bot.wait_until_ready()
    await asyncio.sleep(1)
    while not bot.is_closed():
        try:
            logging.info('Twitch sync')
            channels = await bot.db.fetchall('SELECT * FROM channels WHERE not isnull(discord_server_id) and active="Y";')
            for info in channels:
                bot.loop.create_task(Twitch_sync_channel(info).sync())
        except:
            logging.exception('twitch_sync')
        
        await asyncio.sleep(config['discord']['twitch_sync_every'])
    logging.info('Exit twitch_sync')

class Twitch_sync_channel:
    running = {}

    def __init__(self, channel_info):
        ''' `channel_info` from the channels db table. '''
        self.info = channel_info

    async def sync(self):
        self.server = bot.get_guild(int(self.info['discord_server_id']))
        if not self.server:
            logging.error('Discord server id was not found: {}'.format(self.info['discord_server_id']))
            return
        returninfo = {
            'errors': [],
            'added_roles': 0,
            'added_users': 0,
            'removed_roles': 0,
            'removed_users': 0,
        }
        if self.running.get(self.info['channel_id']):
            logging.info('Already syncing {}'.format(self.info['name']))
            returninfo['errors'].append('Already syncing')
            return returninfo
        self.running[self.info['channel_id']] = True

        try:
            self.twitch_ids = await self.get_twitch_ids()
            self.roles = await self.get_twitch_roles()
            self.give_roles = {member: [] for member in self.server.members}
            await self.set_sub_roles(returninfo)
            await self.sync_roles(returninfo)
        except Exception as e:
            logging.exception('sync {}'.format(self.info['name']))
            returninfo['errors'].append(str(e))
        self.running[self.info['channel_id']] = False
        return returninfo

    async def set_sub_roles(self, returninfo):
        subs = await self.get_subscribers()
        subs = {int(d['user']['_id']): d for d in subs}
        cached_badges = await self.get_cached_badges_months()

        for member in self.server.members:
            try:
                twitch_id = self.twitch_ids.get(member.id)
                if twitch_id not in subs:
                    continue
                subinfo = subs[twitch_id]
                subbed_at = parse(subinfo['created_at']).replace(tzinfo=None)
                seconds = (datetime.utcnow() - subbed_at).total_seconds()
                months = math.ceil(seconds / 60 / 60 / 24 / 30)
                if twitch_id in cached_badges and cached_badges[twitch_id]['sub'] != None:
                    if months < cached_badges[twitch_id]['sub']+1:
                        months = cached_badges[twitch_id]['sub']+1
                sub_streak_role = None
                for role in self.roles:
                    if role['type'] == 'sub_tier' and role['value'] == subinfo['sub_plan']:
                        self.give_roles[member].append(role['role'])
                    elif role['type'] == 'sub_streak' and months >= int(role['value']):
                        sub_streak_role = role['role']
                    elif role['type'] == 'sub':
                        self.give_roles[member].append(role['role'])
                    elif role['type'] == 'bits':
                        if twitch_id in cached_badges and cached_badges[twitch_id]['bits'] == int(role['value']):
                            self.give_roles[member].append(role['role'])
                if sub_streak_role:
                    self.give_roles[member].append(sub_streak_role)
            except Exception as e:
                logging.exception('set_sub_roles {}'.format(self.info['name']))
                returninfo['errors'].append(str(e))

    async def sync_roles(self, returninfo):
        managed_role_ids = [r['role'].id for r in self.roles]
        for member in self.give_roles:
            remove_roles = []
            real_give_roles = []
            give_roles_ids = [r.id for r in self.give_roles[member]]
            give_roles = []
            member_role_ids = []

            for r in member.roles:
                if r.id in managed_role_ids:
                    if r.id not in give_roles_ids:
                        remove_roles.append(r)
                    else:
                        member_role_ids.append(r.id)
            member_role_ids = [r.id for r in member.roles]
            for r in self.give_roles[member]:
                if r.id not in member_role_ids:
                    give_roles.append(r)

            if give_roles:
                logging.debug('Give roles to {}: {}'.format(member.name, give_roles))
                for r in give_roles:
                    try:
                        await member.add_roles(r)
                        returninfo['added_roles'] += 1
                    except:
                        e = 'Failed to give role `{}` to `{}`'.format(r.name, member.name)
                        logging.exception(e)
                        returninfo['errors'].append(e)
                returninfo['added_users'] += 1
            if remove_roles:
                logging.debug('Remove roles from {}: {}'.format(member.name, remove_roles))
                for r in remove_roles:
                    try:
                        await member.remove_roles(r)
                        returninfo['removed_roles'] += 1
                    except:
                        e = 'Failed to give role `{}` to `{}`'.format(r.name, member.name)
                        logging.exception(e)
                        returninfo['errors'].append(e)
                returninfo['removed_users'] += 1

    async def get_subscribers(self):
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
            'Authorization': 'OAuth {}'.format(self.info['twitch_token']),
            'Client-ID': config['twitch']['client_id'],
            'Accept': 'application/vnd.twitchtv.v5+json',
        }
        url = 'https://api.twitch.tv/kraken/channels/{}/subscriptions'.format(
            self.info['channel_id']
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
                    await self.refresh_twitch_token()
                    d = await self.get_subscribers()
                    return d
                else:              
                    error = await r.text()
                    raise Exception('Error getting subscribers for: {} - Error: {}: {}'.format(
                        self.info['name'],
                        r.status,
                        error,
                    ))
        return subs

    async def get_cached_badges_months(self):
        rows = await bot.db.fetchall(
            'SELECT * FROM twitch_badges WHERE channel_id=%s',
            (self.info['channel_id']),
        )
        return {r['user_id']: dict(r) for r in rows}

    async def get_twitch_roles(self):
        db_roles = await bot.db.fetchall(
            'SELECT * FROM twitch_discord_roles WHERE channel_id=%s',
            (self.info['channel_id'])
        )
        roles = []
        for role in db_roles:
            found = False
            for r in self.server.roles:
                if r.name == role['role_name']:
                    found = True
                    if role['role_id'] != str(r.id):
                        await bot.db.execute(
                            'UPDATE twitch_discord_roles SET role_id=%s WHERE id=%s;', 
                            (r.id, role['id'])
                        )
                        role['role_id'] = str(r.id)
                    role['role'] = r
                    continue
                elif role['role_id'] == str(r.id):
                    role['role'] = r
                    found = True
                    continue
            if not found and role['role_id']:
                await bot.db.execute(
                    'UPDATE twitch_discord_roles SET role_id=%s WHERE id=%s;',
                    (None, role['id'])
                )
                role['role_id'] = None
            if not role['role_id']:
                continue
            roles.append(role)
        return roles

    async def refresh_twitch_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.info['twitch_refresh_token'],
            'client_id': config['twitch']['client_id'],
            'client_secret': config['twitch']['client_secret'],
        }
        logging.debug('Refresh token for channel: {}'.format(self.info['name']))
        async with bot.ahttp.post(url, params=params) as r:
            if r.status == 200:
                data = await r.json()
                await bot.db.execute(
                    'UPDATE channels SET twitch_token=%s, twitch_refresh_token=%s WHERE channel_id=%s;',
                    (data['access_token'], data['refresh_token'], self.info['channel_id'])
                )
                self.info['twitch_token'] = data['access_token']
                self.info['twitch_refresh_token'] = data['refresh_token']
            else:
                error = await r.text()
                raise Exception('Failed to refresh token for channel_id: {} - Error: {}: {}'.format(
                    self.info['name'],
                    r.status,
                    error,
                ))

    async def get_twitch_ids(self):
        rows = await bot.db.fetchall('SELECT discord_id, twitch_id FROM users;')
        twitch_ids = {int(r['discord_id']): r['twitch_id'] for r in rows}

        for member in self.server.members:
            try:
                if twitch_ids.get(member.id):
                    continue
                if str(member.status) == 'offline':
                    continue
                data = await discord_request(
                    bot.ahttp,
                    'https://discordapp.com/api/v6/users/{}/profile'.format(
                    member.id
                ))
                if not data:
                    continue
                for con in data['connected_accounts']:
                    if not con['verified']:
                        continue
                    if con['type'] != 'twitch':
                        continue
                    twitch_ids[member.id] = int(con['id'])
                    await bot.db.execute(
                        'INSERT IGNORE INTO users (discord_id, twitch_id) VALUES (%s, %s)', 
                        (member.id, con['id'])
                    )
                    break
            except:
                logging.exception('get_twitch_ids')
        return twitch_ids

async def discord_request(ahttp, url, params=None, headers={}):    
    headers.update({
        'Authorization': config['discord']['user_token'] or \
            config['discord']['token']
    })
    async with ahttp.get(url, params=params, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            return data
