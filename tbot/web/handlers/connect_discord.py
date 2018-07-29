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
            self.redirect('https://discordapp.com/api/oauth2/authorize?'+parse.urlencode({
                    'client_id': config['discord']['client_id'],
                    'permissions': config['discord']['permissions'],
                    'redirect_uri': config['discord']['redirect_uri'],
                    'scope': 'bot',
                    'response_type': 'code',
                }))
            return
        http = httpclient.AsyncHTTPClient()
        response = await http.fetch('https://discordapp.com/api/oauth2/token', body=parse.urlencode({
            'client_id': config['discord']['client_id'],
            'client_secret': config['discord']['client_secret'],
            'code': code,
            'redirect_uri': config['discord']['redirect_uri'],
            'grant_type': 'authorization_code',
        }), method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, raise_error=False)
        if response.code != 200:
            logging.error(escape.native_str(response.body))
            self.write('Unable to verify you at Discord, please try again.')
            return
        data = json.loads(escape.native_str(response.body))
        await self.db.execute('UPDATE channels SET discord_server_id=%s WHERE channel_id=%s',
            (data['guild']['id'], self.current_user['user_id'])
        )
        self.set_secure_cookie('connect_success', 'Discord was successfully connected.')
        self.redirect('/connect')