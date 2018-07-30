import logging, json
from tornado import web, httpclient, escape
from urllib import parse
from tbot import config
from .base import Base_handler

class Handler(Base_handler):

    @web.authenticated
    async def get(self):
        code = self.get_argument('code', None)
        if not code:
            self.redirect('https://accounts.spotify.com/authorize?'+parse.urlencode({
                    'client_id': config['spotify']['client_id'],
                    'redirect_uri': config['spotify']['redirect_uri'],
                    'scope': 'playlist-read-private '
                             'user-read-recently-played ' 
                             'user-read-currently-playing',
                    'response_type': 'code',
                }))
            return
        http = httpclient.AsyncHTTPClient()
        response = await http.fetch('https://accounts.spotify.com/api/token', body=parse.urlencode({
            'client_id': config['spotify']['client_id'],
            'client_secret': config['spotify']['client_secret'],
            'code': code,
            'redirect_uri': config['spotify']['redirect_uri'],
            'grant_type': 'authorization_code',
        }), method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, raise_error=False)
        if response.code != 200:
            logging.error(escape.native_str(response.body))
            self.write('Unable to verify you at Spotify, please try again.')
            return
        token = json.loads(escape.native_str(response.body))

        response = await http.fetch('https://api.spotify.com/v1/me', headers={
            'Authorization': 'Bearer {}'.format(token['access_token']),
        })
        if response.code != 200:
            logging.error(escape.native_str(response.body))
            self.write('Unable retrive your Spotify profile, please try again.')
            return
        user = json.loads(escape.native_str(response.body))

        await self.db.execute('''
            INSERT INTO spotify (channel_id, token, refresh_token, user) VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE token=VALUES(token), refresh_token=VALUES(refresh_token), 
            user=VALUES(user)
            ''',
            (self.current_user['user_id'], token['access_token'], token['refresh_token'], user['id'])
        )
        self.set_secure_cookie('connect_success', 'Spotify was successfully connected.')
        self.redirect('/connect')