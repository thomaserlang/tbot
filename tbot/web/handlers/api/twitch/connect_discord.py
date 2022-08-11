import  json, base64
from tornado import httpclient, escape
from urllib import parse
from tbot import config, utils, logger
from ..base import Base_handler, Api_handler, Level

class Handler(Api_handler):

    @Level(3)
    async def get(self, channel_id):
        r = await self.db.fetchone(
            'SELECT discord_server_id, discord_server_name FROM twitch_channels WHERE channel_id=%s',
            (channel_id,)
        )
        self.write_object({
            'connected': True if r['discord_server_id'] else False,
            'name': r['discord_server_name'] if r else None,
        })

    @Level(3)
    async def delete(self, channel_id):
        r = await self.db.fetchone(
            'UPDATE twitch_channels SET discord_server_id=null WHERE channel_id=%s',
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
        self.redirect('https://discordapp.com/api/oauth2/authorize?'+parse.urlencode({
            'client_id': config.data.discord.client_id,
            'permissions': config.data.discord.permissions,
            'redirect_uri': parse.urljoin(config.data.web.base_url, 'connect/discord'),
            'scope': 'bot',
            'response_type': 'code',
            'state': base64.b64encode(utils.json_dumps({
                'channel_id': channel_id,
                'channel_name': r['name'],
            }).encode('utf-8')),
        }))

class Receive_handler(Base_handler):

    async def get(self):
        code = self.get_argument('code', None)
        state = utils.json_loads(base64.b64decode(self.get_argument('state')))
        await self.check_access(state['channel_id'])

        http = httpclient.AsyncHTTPClient()
        response = await http.fetch('https://discordapp.com/api/oauth2/token', body=parse.urlencode({
            'client_id': config.data.discord.client_id,
            'client_secret': config.data.discord.client_secret,
            'code': code,
            'redirect_uri': parse.urljoin(config.data.web.base_url, 'connect/discord'),
            'grant_type': 'authorization_code',
        }), method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, raise_error=False)
        if response.code != 200:
            logger.error(escape.native_str(response.body))
            self.write('Unable to verify you at Discord, please try again.')
            return
        data = json.loads(escape.native_str(response.body))
        if 'guild' not in data:
            e = 'oAuth2 grant is not enabled for the bot. Enable it here: https://discordapp.com/developers/applications/{}/bots'.format(\
                config.data.discord.client_id
            )
            logger.error(e)
            self.write(e)
            return
        await self.db.execute('UPDATE twitch_channels SET discord_server_id=%s, discord_server_name=%s WHERE channel_id=%s',
            (data['guild']['id'], data['guild']['name'], state['channel_id'])
        )
        if state['channel_name']:
            self.redirect('/twitch/{}/discord'.format(state['channel_name']))
        else:
            self.redirect('/twitch/dashboard')

    @Level(3)
    async def check_access(self, channel_id):
        pass