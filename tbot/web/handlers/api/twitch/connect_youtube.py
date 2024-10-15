import base64
import json
from urllib import parse

from tornado import escape, httpclient

from tbot import config, logger, utils

from ..base import Api_handler, Base_handler, Level


class Handler(Api_handler):
    @Level(3)
    async def get(self, channel_id):
        r = await self.db.fetchone(
            'SELECT handle FROM twitch_youtube WHERE channel_id=%s', (channel_id,)
        )
        self.write_object(
            {
                'connected': True if r else False,
                'handle': r['handle'] if r else None,
            }
        )

    @Level(3)
    async def delete(self, channel_id):
        token = await self.db.fetchone(
            'SELECT token FROM twitch_youtube WHERE channel_id=%s', (channel_id,)
        )
        await self.db.fetchone(
            'DELETE FROM twitch_youtube WHERE channel_id=%s', (channel_id,)
        )
        await self.redis.publish_json(
            'tbot:server:commands', ['youtube_disconnected', channel_id]
        )

        if token:
            http = httpclient.AsyncHTTPClient()
            await http.fetch(
                'https://oauth2.googleapis.com/revoke',
                method='POST',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                body=parse.urlencode(
                    {
                        'token': token['token'],
                    }
                ),
            )

        self.set_status(204)

    @Level(3)
    async def post(self, channel_id):
        r = await self.db.fetchone(
            'select name from twitch_channels where channel_id=%s', (channel_id,)
        )
        if not r:
            raise Exception('Unknown channel {}'.format(channel_id))
        self.redirect(
            'https://accounts.google.com/o/oauth2/v2/auth?'
            + parse.urlencode(
                {
                    'client_id': config.data.youtube.client_id,
                    'access_type': 'offline',
                    'prompt': 'consent',
                    'include_granted_scopes': 'true',
                    'redirect_uri': parse.urljoin(
                        config.data.web.base_url, 'connect/youtube'
                    ),
                    'scope': 'https://www.googleapis.com/auth/youtube',
                    'response_type': 'code',
                    'state': base64.b64encode(
                        utils.json_dumps(
                            {
                                'channel_id': channel_id,
                                'channel_name': r['name'],
                            }
                        ).encode('utf-8')
                    ),
                }
            )
        )


class Receive_handler(Base_handler):
    async def get(self):
        code = self.get_argument('code')
        state = utils.json_loads(base64.b64decode(self.get_argument('state')))
        await self.check_access(state['channel_id'])

        http = httpclient.AsyncHTTPClient()
        response = await http.fetch(
            'https://oauth2.googleapis.com/token',
            body=parse.urlencode(
                {
                    'client_id': config.data.youtube.client_id,
                    'client_secret': config.data.youtube.client_secret,
                    'code': code,
                    'redirect_uri': parse.urljoin(
                        config.data.web.base_url, 'connect/youtube'
                    ),
                    'grant_type': 'authorization_code',
                }
            ),
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            raise_error=False,
        )
        if response.code != 200:
            logger.error(escape.native_str(response.body))
            self.write('Unable to verify you at YouTube, please try again.')
            return
        token = json.loads(escape.native_str(response.body))

        response = await http.fetch(
            'https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true',
            headers={
                'Authorization': 'Bearer {}'.format(token['access_token']),
            },
            raise_error=False,
        )
        if response.code != 200:
            logger.error(escape.native_str(response.body))
            self.write('Unable retrieve your YouTube profile, please try again.')
            return
        user = json.loads(escape.native_str(response.body))

        await self.db.execute(
            """
            INSERT INTO twitch_youtube (channel_id, token, refresh_token, handle) VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE token=VALUES(token), refresh_token=VALUES(refresh_token), 
            handle=VALUES(handle)
            """,
            (
                state['channel_id'],
                token['access_token'],
                token['refresh_token'],
                ', '.join([user['snippet']['title'] for user in user['items']]),
            ),
        )
        await self.redis.publish_json(
            'tbot:server:commands', ['youtube_connected', state['channel_id']]
        )

        if state['channel_name']:
            self.redirect('/twitch/{}/youtube'.format(state['channel_name']))
        else:
            self.redirect('/twitch/dashboard')

    @Level(3)
    async def check_access(self, channel_id):
        pass
