import logging, good, json
from tornado import httpclient, escape
from ..base import Api_handler, Level, Api_exception
from tbot import config
from tbot.utils.twitch import twitch_request

class Handler(Api_handler):

    async def get(self):
        if not self.current_user:
            self.write_object([])
            return
        suggest_name = self.get_argument('suggest_name', None)
        args = [self.current_user['user_id']]
        sql = '''
            SELECT 
                c.channel_id AS id, c.name
            FROM
                twitch_channels c,
                twitch_channel_admins a
            WHERE
                a.user_id = %s AND 
                a.channel_id = c.channel_id
        '''

        if suggest_name:
            sql += ' AND c.name LIKE %s'
            args.append(suggest_name+'%')

        sql += ' LIMIT 10'

        admin_of = await self.db.fetchall(
            sql, 
            args
        )
        if not admin_of:
            admin_of = []

        if not suggest_name:
            admin_of.insert(0, {
                'id': self.current_user['user_id'],
                'name': self.current_user['user'],
                'level': 9,
            })

        self.write_object(admin_of)

class Channel_admins(Api_handler):

    __schema__ = good.Schema({
        'user': good.All(str, good.Length(min=4, max=25)),
        'level': good.All(good.Coerce(int), good.Range(min=1, max=3)),
    })

    __update_schema__ = good.Schema({
        'level': good.All(good.Coerce(int), good.Range(min=1, max=3)),
    })

    @Level(3)
    async def get(self, channel_id):
        admins = await self.db.fetchall('''
            SELECT user_id as id, user as name, level 
            FROM twitch_channel_admins 
            WHERE channel_id=%s
            ORDER BY level DESC
            ''',
            (channel_id,)
        )
        self.write_object(admins)

    @Level(3)
    async def post(self, channel_id):
        data = self.validate()

        url = 'https://api.twitch.tv/helix/users'
        users = await twitch_request(self.ahttp, url, {
            'login': data['user'],
        })
        if not users['data']:
            raise Api_exception(400, 'User does not exist on Twitch')
        user = users['data'][0]
        await self.db.execute('''
            INSERT INTO 
                twitch_channel_admins 
                    (channel_id, user_id, user, level, created_at, updated_at)
            VALUES
                (%s, %s, %s, %s, now(), now())
            ON DUPLICATE KEY UPDATE 
                user=VALUES(user),
                level=VALUES(level),
                updated_at=VALUES(updated_at)
        ''', (channel_id, user['id'], user['display_name'], data['level']))

        self.set_status(204)

    @Level(3)
    async def put(self, channel_id, user_id):
        data = self.validate(self.__update_schema__)
        await self.db.execute(
            'UPDATE twitch_channel_admins SET level=%s WHERE channel_id=%s AND user_id=%s',
            (data['level'], channel_id, user_id)
        )

    @Level(3)
    async def delete(self, channel_id, user_id):
        await self.db.execute(
            'DELETE FROM twitch_channel_admins WHERE channel_id=%s AND user_id=%s',
            (channel_id, user_id)
        )
        self.set_status(204)