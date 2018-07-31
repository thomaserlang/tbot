import logging, json, os
from tornado import web, httpclient, escape
from urllib import parse
from tbot import config
from .base import Base_handler

class Handler(Base_handler):

    async def get(self):
        code = self.get_argument('code', None)
        error = self.get_argument('error', None)
        if error:
            self.write(error)
            return
        if not code:
            self.redirect('https://id.twitch.tv/oauth2/authorize?'+parse.urlencode({
                    'client_id': config['twitch']['client_id'],
                    'response_type': 'code',
                    'redirect_uri': config['twitch']['redirect_uri'],
                    'scope': 'channel_subscriptions',
                })
            )
            return

        http = httpclient.AsyncHTTPClient()
        response = await http.fetch('https://id.twitch.tv/oauth2/token?'+parse.urlencode({
            'client_id': config['twitch']['client_id'],
            'client_secret': config['twitch']['client_secret'],
            'code': code,
            'redirect_uri': config['twitch']['redirect_uri'],
            'grant_type': 'authorization_code',
        }), body='', method='POST', raise_error=False)
        if response.code != 200:
            logging.error(response.body)
            self.write('Unable to verify you at Twitch, <a href="/connect/twitch">please try again</a>.')
            return
        token = json.loads(escape.native_str(response.body))
        
        response = await http.fetch('https://id.twitch.tv/oauth2/validate', headers={
            'Authorization': 'OAuth {}'.format(token['access_token'])
        })
        if response.code != 200:
            logging.error(response.body)
            self.clear_cookie('connect_user')
            self.clear_cookie('auto_login')
            self.write('Unable to verify you at Twitch, <a href="/connect/twitch">please try again</a>')
            return
        userinfo = json.loads(escape.native_str(response.body))

        await self.db.execute('''
            INSERT INTO channels (channel_id, name, active, created_at, updated_at, twitch_token, twitch_refresh_token)
            VALUES (%s, %s, "Y", now(), null, %s, %s) ON DUPLICATE KEY UPDATE 
            name=VALUES(name), updated_at=now(), active=VALUES(active), twitch_token=VALUES(twitch_token), 
            twitch_refresh_token=VALUES(twitch_refresh_token);
        ''', (
            userinfo['user_id'],
            userinfo['login'],
            token['access_token'],
            token['refresh_token'],
        ))

        self.set_secure_cookie('connect_user', json.dumps({
            'user_id': userinfo['user_id'],
            'user': userinfo['login'],
            'access_token': token['access_token'],
        }), expires_days=None)

        _next = self.get_secure_cookie('next')
        self.clear_cookie('next')
        if _next:
            self.redirect(_next)
        else:
            self.redirect('/connect')