import logging
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
                twitch_channels c
                LEFT JOIN twitch_channel_mods m ON (m.user_id = %s AND m.channel_id = c.channel_id)
                LEFT JOIN twitch_channel_admins a ON (a.user_id = %s AND a.channel_id = c.channel_id)
            WHERE
                c.active = 'Y' AND 
                c.chatlog_enabled = 'Y' AND 
                (not isnull(m.user_id) OR not isnull(a.user_id));
        ''', (self.current_user['user_id'], self.current_user['user_id']))
        self.write_object(mod_of)