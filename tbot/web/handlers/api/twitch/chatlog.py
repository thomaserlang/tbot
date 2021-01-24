import logging
from tornado import web
from ..base import Api_handler

class Handler(Api_handler):

    async def get(self, channel_id):
        # TODO: Add setting to allow or disallow non mods to view the logs
        # For the moment only mods are allowed to view them
        if True:
            if not self.current_user:
                raise web.HTTPError(401, 'Authentication required')
            mod = await self.db.fetchone('SELECT user_id FROM twitch_channel_mods WHERE channel_id=%s AND user_id=%s',
                [channel_id, self.current_user['user_id']])
            if not mod:
                raise web.HTTPError(403, 'You are not a moderator of this channel')

        args = [channel_id]
        sql = 'SELECT * FROM twitch_chatlog WHERE channel_id=%s  AND type IN (1,100) '

        user = self.get_argument('user', None)
        if user:
            u = await self.db.fetchone('SELECT user_id FROM twitch_usernames WHERE user=%s', [user])
            user_id = 0
            if u:
                user_id = u['user_id']
            sql += ' AND user_id=%s'
            args.append(user_id)

        before_id = self.get_argument('before_id', None)
        if before_id:
            sql += ' AND id<%s'
            args.append(before_id)

        after_id = self.get_argument('after_id', None)
        if after_id:
            sql += ' AND id>%s'
            args.append(after_id)

        message = self.get_argument('message', None)
        if message:
            sql += ' AND message LIKE %s'
            args.append('%{}%'.format(message))

        show_mod_actions_only = self.get_argument('show_mod_actions_only', None)
        if show_mod_actions_only == 'yes':
            sql += ' AND type=100'

        if not after_id:
            sql += ' ORDER BY id DESC LIMIT %s'
        else:            
            sql += ' ORDER BY id ASC LIMIT %s'
        per_page = 10
        args.append(per_page)
        log = await self.db.fetchall(sql, args)
        if not log:
            self.set_status(204)
        else:
            self.set_header('X-Per-Page', per_page)
            if not after_id:
                self.write_object(list(reversed(log)))
            else:
                self.write_object(list(log))

class User_stats_handler(Api_handler):

    async def get(self, channel_id):
        user = self.get_argument('user')
        sql = '''
            SELECT 
                bans, timeouts, purges, chat_messages, 
                last_viewed_stream_date, streams, streams_row,
                streams_row_peak, streams_row_peak_date
            FROM
                twitch_usernames u
                LEFT JOIN twitch_user_chat_stats us ON (us.user_id = u.user_id AND us.channel_id=%s)
                LEFT JOIN twitch_user_stats s ON (s.user_id = u.user_id AND s.channel_id=%s)
            WHERE                
                u.user = %s 
        '''
        stats = await self.db.fetchone(sql, [channel_id, channel_id, user])
        if stats:
            self.write_object(stats)
        else:
            self.set_status(204)