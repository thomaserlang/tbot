import logging
from tornado import web
from ..base import Api_handler
from dateutil.parser import parse


class Handler(Api_handler):

    async def get(self, channel_id):
        await has_mod(self, channel_id)

        args = [channel_id]
        sql = 'SELECT * FROM twitch_chatlog WHERE channel_id=%s  AND type IN (1,100) '

        user = self.get_argument('user', None)
        if user:
            u = await self.db.fetchone('SELECT user_id FROM twitch_usernames WHERE user=%s', [user])
            if not u:
                self.set_status(204)
                return
            sql += ' AND user_id=%s'
            args.append(u['user_id'])

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
        await has_mod(self, channel_id)

        user = self.get_argument('user')
        u = await self.db.fetchone('SELECT user_id FROM twitch_usernames WHERE user=%s', [user])
        if not u:
            self.set_status(404)
            return
        user_id = u['user_id']
        sql = '''
            SELECT 
                bans, timeouts, purges, chat_messages, 
                last_viewed_stream_date, streams, streams_row,
                streams_row_peak, streams_row_peak_date, sw.watchtime, sw.first_viewed_stream_date
            FROM
                twitch_user_stats s
                LEFT JOIN twitch_user_chat_stats us ON (us.user_id = s.user_id AND us.channel_id=s.channel_id)
                LEFT JOIN (SELECT tw.user_id, sum(tw.time) as watchtime, min(ts.started_at) as first_viewed_stream_date FROM twitch_stream_watchtime tw, twitch_streams ts WHERE tw.channel_id=%s AND tw.user_id=%s AND tw.stream_id=ts.stream_id) sw ON (sw.user_id=s.user_id)
            WHERE              
                s.channel_id = %s AND  
                s.user_id = %s
        '''
        stats = await self.db.fetchone(sql, (channel_id, user_id, channel_id, user_id))
        if stats:
            stats['watchtime'] = int(stats['watchtime']) if stats['watchtime'] != None else None
            self.write_object(stats)
        else:
            self.set_status(204)


class User_streams_watched_handler(Api_handler):

    async def get(self, channel_id):
        await has_mod(self, channel_id)        
        user = self.get_argument('user')
        args = [user, channel_id]
        sql = '''
            select 
                s.started_at, s.uptime, sw.`time` as watchtime,
                s.stream_id
            from 
                twitch_usernames u,
                twitch_streams s,
                twitch_stream_watchtime sw
            where 
                u.user=%s AND
                sw.channel_id=%s AND
                sw.user_id=u.user_id AND
                s.stream_id = sw.stream_id
        '''
        after_id = self.get_argument('after_id', None)
        if after_id:
            sql += ' AND started_at < %s'
            args.append(parse(after_id))
        sql += ' ORDER BY s.started_at DESC LIMIT 5'
        streams = await self.db.fetchall(sql, args)
        self.write_object(list(streams))


async def has_mod(handler, channel_id):
    # TODO: Add setting to allow or disallow non mods to view the logs
    # For the moment only mods or admins are allowed to view them
    if not handler.current_user:
        raise web.HTTPError(401, 'Authentication required')
    mod = await handler.db.fetchone('''
        SELECT 
            c.channel_id
        FROM
            twitch_channels c
            LEFT JOIN twitch_channel_mods m ON (m.user_id = %s AND m.channel_id = c.channel_id)
            LEFT JOIN twitch_channel_admins a ON (a.user_id = %s AND a.channel_id = c.channel_id)
        WHERE
            c.channel_id = %s AND 
            c.active = 'Y' AND 
            c.chatlog_enabled = 'Y' AND 
            (not isnull(m.user_id) OR not isnull(a.user_id))
    ''',
        (handler.current_user['user_id'], handler.current_user['user_id'], channel_id))
    if not mod:
        raise web.HTTPError(403, 'You can not view chat logs for this channel')