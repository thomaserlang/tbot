import logging
from tornado import web
from ..base import Api_handler

class Handler(Api_handler):

    async def get(self):
        if not self.current_user:
            self.write_object([])
            return
        mod_of = await self.db.fetchall('''
            SELECT 
                c.channel_id AS id, c.name
            FROM
                channels c,
                twitch_channel_mods m
            WHERE
                m.user_id = %s
                    AND m.channel_id = c.channel_id
                    AND c.active = 'Y';
        ''', [self.current_user['user_id']])
        self.write_object(mod_of)
