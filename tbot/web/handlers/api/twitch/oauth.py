import logging, asyncio
from tornado import httpclient
from urllib import parse
from tbot import config, utils
from ..base import Base_handler
from .eventsubs.eventsub import create_eventsubs

class Handler(Base_handler):

    async def get(self):
        code = self.get_argument('code', None)
        error = self.get_argument('error', None)
        if error:
            self.write(error)
            return
        if not code:
            self.write('Missing code argument')
            return

        http = httpclient.AsyncHTTPClient()
        response = await http.fetch('https://id.twitch.tv/oauth2/token?'+parse.urlencode({
            'client_id': config.data.twitch.client_id,
            'client_secret': config.data.twitch.client_secret,
            'code': code,            
            'redirect_uri': parse.urljoin(config.data.web.base_url, 'connect/twitch'),
            'grant_type': 'authorization_code',
        }), body='', method='POST', raise_error=False)
        if response.code != 200:
            logging.error(response.body)
            self.write('Unable to verify you at Twitch, please try again.')
            return
        token = utils.json_loads(response.body)
        
        response = await http.fetch('https://id.twitch.tv/oauth2/validate', headers={
            'Authorization': 'OAuth {}'.format(token['access_token'])
        })
        if response.code != 200:
            self.clear_cookie('twitch_user')
            self.clear_cookie('auto_login')
            self.write('Unable to verify you at Twitch, please try again')
            return
        userinfo = utils.json_loads(response.body)
        if userinfo['scopes']:
            await self.db.execute('''
                INSERT INTO twitch_channels (channel_id, name, created_at, updated_at, twitch_token, twitch_refresh_token, twitch_scope)
                VALUES (%s, %s, now(), null, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                name=VALUES(name), updated_at=now(), twitch_token=VALUES(twitch_token), 
                twitch_refresh_token=VALUES(twitch_refresh_token), twitch_scope=VALUES(twitch_scope);
            ''', (
                userinfo['user_id'],
                userinfo['login'],
                token['access_token'],
                token['refresh_token'],
                utils.json_dumps(userinfo['scopes']),
            ))
            if userinfo['scopes']:
                asyncio.create_task(create_eventsubs(self.ahttp, userinfo['user_id']))
        else:
            await self.db.execute('''
                INSERT INTO twitch_channels (channel_id, name, created_at, active)
                VALUES (%s, %s, now(), "N") ON DUPLICATE KEY UPDATE 
                name=VALUES(name);
            ''', (
                userinfo['user_id'],
                userinfo['login'],
            ))

        self.set_secure_cookie('twitch_user', utils.json_dumps({
            'user_id': userinfo['user_id'],
            'user': userinfo['login'],
        }), expires_days=1)

        _next = self.get_secure_cookie('next')
        self.clear_cookie('next')
        if _next:
            self.redirect(_next)
        else:
            self.redirect('/twitch/dashboard')

class Login_handler(Base_handler):
    
    def get(self):
        if self.get_argument('redirect', None):
            self.redirect('https://id.twitch.tv/oauth2/authorize?'+parse.urlencode({
                    'client_id': config.data.twitch.client_id,
                    'response_type': 'code',                    
                    'redirect_uri': parse.urljoin(config.data.web.base_url, 'connect/twitch'),
                    'scope': ' '.join(config.data.twitch.request_scope) \
                        if self.get_argument('request_extra_auth', None) else '',
                })
            )
        else:
            _next = self.get_argument('next', None)
            self.clear_cookie('next')
            if _next:
                self.set_secure_cookie('next', _next, expires_days=None)
            self.render('twitch_login.html')

class Logout_handler(Base_handler):
    
    def get(self):
        self.clear_cookie('twitch_user')
        self.redirect('/')