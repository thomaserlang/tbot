import logging, json, base64
from tornado import web, httpclient, escape
from urllib import parse
from tbot import config, utils
from ..base import Api_handler, Base_handler, Level

class Handler(Api_handler):

    @Level(3)
    async def get(self, channel_id):
        r = await self.db.fetchone(
            'SELECT user FROM twitch_spotify WHERE channel_id=%s',
            (channel_id,)
        )
        self.write_object({
            'connected': True if r else False,
            'user': r['user'] if r else None,
        })

    @Level(3)
    async def delete(self, channel_id):
        r = await self.db.fetchone(
            'DELETE FROM twitch_spotify WHERE channel_id=%s',
            (channel_id,)
        )
        self.set_status(204)

    @Level(3)
    async def post(self, channel_id):
        r = await self.db.fetchone(
            'select name from twitch_channels where channel_id=%s',
            (channel_id,)
        )
        if not r:
            raise Exception('Unknown channel {}'.format(channel_id))
        self.redirect('https://accounts.spotify.com/authorize?'+parse.urlencode({
            'client_id': config.data.spotify.client_id,
            'redirect_uri': parse.urljoin(config.data.web.base_url, 'connect/spotify'),
            'scope': 'playlist-read-private '
                     'user-read-recently-played ' 
                     'user-read-currently-playing',
            'response_type': 'code',
            'state': base64.b64encode(utils.json_dumps({
                'channel_id': channel_id,
                'channel_name': r['name'],
            }).encode('utf-8')),
        }))

class Receive_handler(Base_handler):

    async def get(self):
        code = self.get_argument('code')
        state = utils.json_loads(base64.b64decode(self.get_argument('state')))
        await self.check_access(state['channel_id'])

        http = httpclient.AsyncHTTPClient()
        response = await http.fetch('https://accounts.spotify.com/api/token', body=parse.urlencode({
            'client_id': config.data.spotify.client_id,
            'client_secret': config.data.spotify.client_secret,
            'code': code,
            'redirect_uri': parse.urljoin(config.data.web.base_url, 'connect/spotify'),
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
            self.write('Unable retrieve your Spotify profile, please try again.')
            return
        user = json.loads(escape.native_str(response.body))

        await self.db.execute('''
            INSERT INTO twitch_spotify (channel_id, token, refresh_token, user) VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE token=VALUES(token), refresh_token=VALUES(refresh_token), 
            user=VALUES(user)
            ''',
            (state['channel_id'], token['access_token'], token['refresh_token'], user['id'])
        )
        if state['channel_name']:
            self.redirect('/twitch/{}/spotify'.format(state['channel_name']))
        else:
            self.redirect('/twitch/dashboard')

    @Level(3)
    async def check_access(self, channel_id):
        pass