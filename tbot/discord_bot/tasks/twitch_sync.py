import asyncio
from datetime import datetime, timezone
from tbot import config, logger
from tbot.utils.twitch import twitch_channel_token_request

async def twitch_sync(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(config.data.discord.twitch_sync_every)
        try:
            logger.info('Twitch sync')
            channels = await bot.db.fetchall('SELECT * FROM twitch_channels WHERE not isnull(discord_server_id) and active="Y";')
            for info in channels:
                bot.loop.create_task(Twitch_sync_channel(info, bot).sync())
        except:
            logger.exception('twitch_sync')

class Twitch_sync_channel:
    running = {}

    def __init__(self, channel_info, bot):
        ''' `channel_info` from the channels db table. '''
        self.info = channel_info
        self.bot = bot

    async def sync(self):
        self.server = self.bot.get_guild(int(self.info['discord_server_id']))
        if not self.server:
            logger.info('Discord server id was not found: {}'.format(self.info['discord_server_id']))
            return
        returninfo = {
            'errors': [],
            'added_roles': 0,
            'added_users': 0,
            'removed_roles': 0,
            'removed_users': 0,
        }
        if self.running.get(self.info['channel_id']):
            logger.info('Already syncing {}'.format(self.info['name']))
            returninfo['errors'].append('Already syncing')
            return returninfo
        self.running[self.info['channel_id']] = True

        try:
            self.twitch_ids = await self.get_twitch_ids()
            self.roles = await self.get_twitch_roles()
            self.give_roles = {member: [] for member in self.server.members}
            await self.set_sub_roles(returninfo)
            await self.sync_roles(returninfo)
        except Twitch_exception as e:
            returninfo['errors'].append(str(e))
        except Exception as e:
            logger.exception('sync {}'.format(self.info['name']))
            returninfo['errors'].append(str(e))
        self.running[self.info['channel_id']] = False
        return returninfo

    async def set_sub_roles(self, returninfo):
        subs = await self.get_subscribers()
        await self.count_subs(subs)
        subs = {d['user_id']: d for d in subs}
        cached_badges = await self.get_cached_badges_months()
        for member in self.server.members:
            try:
                twitch_id = self.twitch_ids.get(member.id)
                if twitch_id not in subs:
                    continue
                subinfo = subs[twitch_id]
                months = 1
                if twitch_id in cached_badges:
                    months = cached_badges[twitch_id]['sub'] or 0                    
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
                logger.exception('set_sub_roles {}'.format(self.info['name']))
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
                logger.debug('Give roles to {}: {}'.format(member.name, give_roles))
                for r in give_roles:
                    try:
                        await member.add_roles(r)
                        returninfo['added_roles'] += 1
                    except:
                        e = 'Failed to give role `{}` to `{}`'.format(r.name, member.name)
                        logger.exception(e)
                        returninfo['errors'].append(e)
                returninfo['added_users'] += 1
            if remove_roles:
                logger.debug('Remove roles from {}: {}'.format(member.name, remove_roles))
                for r in remove_roles:
                    try:
                        await member.remove_roles(r)
                        returninfo['removed_roles'] += 1
                    except:
                        e = 'Failed to remove role `{}` to `{}`'.format(r.name, member.name)
                        logger.exception(e)
                        returninfo['errors'].append(e)
                returninfo['removed_users'] += 1

    async def get_subscribers(self):
        '''
        return [
            {
                "broadcaster_id": "123",
                "broadcaster_name": "test_user",
                "is_gift": True,
                "tier": "1000",
                "plan_name": "Channel Subscription (erleperle)",
                "user_id": "36981191",
                "user_name": "erleperle",
            }
        ]
        '''

        subs = []
        url = 'https://api.twitch.tv/helix/subscriptions'
        after = ''
        while True:
            d = await twitch_channel_token_request(self.bot, self.info['channel_id'], url, params={
                'broadcaster_id': self.info['channel_id'],
                'after': after,
            })
            if d['data']:
                subs.extend(d['data'])
            else:
                break
            if not 'pagination' in d or not d['pagination']:
                break
            after = d['pagination']['cursor']
        return subs
    


    async def get_cached_badges_months(self):
        rows = await self.bot.db.fetchall(
            'SELECT * FROM twitch_badges WHERE channel_id=%s',
            (self.info['channel_id']),
        )
        return {r['user_id']: dict(r) for r in rows}

    async def get_twitch_roles(self):
        db_roles = await self.bot.db.fetchall(
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
                        await self.bot.db.execute(
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
                await self.bot.db.execute(
                    'UPDATE twitch_discord_roles SET role_id=%s WHERE id=%s;',
                    (None, role['id'])
                )
                role['role_id'] = None
            if not role['role_id']:
                continue
            roles.append(role)
        return roles

    async def get_twitch_ids(self):
        rows = await self.bot.db.fetchall('SELECT discord_id, twitch_id FROM twitch_discord_users;')
        twitch_ids = {int(r['discord_id']): r['twitch_id'] for r in rows}
        try:
            for member in self.server.members:
                if twitch_ids.get(member.id):
                    continue
                if str(member.status) == 'offline':
                    continue
                data = await discord_request(
                    self.bot.ahttp,
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
                    twitch_ids[member.id] = con['id']
                    await self.bot.db.execute(
                        'INSERT IGNORE INTO twitch_discord_users (discord_id, twitch_id) VALUES (%s, %s)', 
                        (member.id, con['id'])
                    )
                    break
        except:
            logger.exception('get_twitch_ids')
        return twitch_ids

async def discord_request(ahttp, url, params=None, headers={}):    
    headers.update({
        'Authorization': config.data.discord.user_token,
    })
    async with ahttp.get(url, params=params, headers=headers) as r:
        data = await r.json()
        if r.status == 200:
            return data
        elif r.status in (401, 403):
            data = await r.json()
            if data['code'] == 50001:
                logger.error('User "{}" is not on the same server as the user_token'.format(url))
                return
            raise Exception(data['message'])

class Twitch_exception(Exception):
    pass