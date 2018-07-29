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
        data = json.loads(escape.native_str(response.body))
        await self.db.execute('''
            INSERT INTO spotify (channel_id, token, refresh_token) VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE token=VALUES(token), refresh_token=VALUES(refresh_token)
            ''',
            (self.current_user['user_id'], data['access_token'], data['refresh_token'])
        )
        self.redirect('/connect')