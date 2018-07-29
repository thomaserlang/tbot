from .base import Base_handler
from tornado.web import authenticated

class Handler(Base_handler):

    @authenticated
    async def get(self):
        apps = await self.db.fetchone('''
            SELECT 
                if(isnull(c.twitch_token), 'N', 'Y') as twitch,
                if(isnull(c.discord_server_id), 'N', 'Y') as discord,
                if(isnull(s.channel_id), 'N', 'Y') as spotify
            FROM
                channels c
                LEFT JOIN spotify s on (s.channel_id=c.channel_id)
            WHERE
                c.channel_id=%s;
        ''', (self.current_user['user_id']))
        success_msg = self.get_secure_cookie('connect_success')
        self.clear_cookie('connect_success')
        self.render('connect.html', apps=apps, success_msg=success_msg)