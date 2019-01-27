import logging
from ..base import Api_handler, Api_exception
from tornado import web

class Handler(Api_handler):

    async def get(self):
        sql = 'SELECT channel_id as id, name FROM twitch_channels WHERE chatlog_enabled="Y"'
        args = []
        name = self.get_argument('name', None)
        suggest_name = self.get_argument('suggest_name', None)
        if name:
            sql += ' AND name=%s'
            args.append(name)
        elif suggest_name:
            sql += ' AND name LIKE %s'
            args.append(suggest_name+'%')
        sql += ' LIMIT 10'
        channels = await self.db.fetchall(sql, args)
        self.write_object(channels)

class Single_handle(Api_handler):

    async def get(self, channel):
        user_id = None
        if self.current_user:
            user_id = self.current_user['user_id']
        channel = await self.db.fetchone('''
            SELECT 
                c.channel_id as id, c.name, a.level
            FROM 
                twitch_channels c
                LEFT JOIN twitch_channel_admins a ON (a.channel_id=c.channel_id AND a.user_id=%s) 
            WHERE 
                c.name=%s
            ''',
            (user_id, channel,)
        )
        if not channel:
            raise Api_exception(404, 'Unknown channel')
        else:
            if channel['id'] == user_id:
                channel['level'] = 9
            self.write_object(channel)