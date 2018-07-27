import logging, json, os
from tornado import web, ioloop, httpclient, escape
from urllib import parse
from tbot import config, db

class Base_handler(web.RequestHandler):

    @property
    def db(self):
        return self.application.db
    

class Login_handler(Base_handler):

    def get(self):
        self.redirect('https://id.twitch.tv/oauth2/authorize?'+parse.urlencode({
                'client_id': config['twitch']['client_id'],
                'response_type': 'code',
                'redirect_uri': config['twitch']['redirect_uri'],
                'scope': 'channel_subscriptions',
            })
        )

class OAuth_handler(Base_handler):

    async def get(self):
        code = self.get_argument('code')
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
            self.write('Unable to verify you at Twitch, please try again.')
            return
        token = json.loads(escape.native_str(response.body))
        
        response = await http.fetch('https://id.twitch.tv/oauth2/validate', headers={
            'Authorization': 'OAuth {}'.format(token['access_token'])
        })
        if response.code != 200:
            logging.error(response.body)
            self.clear_cookie('data')
            self.clear_cookie('auto_login')
            self.write('Unable to verify you at Twitch')
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

        self.write('Done, you can close this page')

def App():
    return web.Application(
        [
            (r'/register', Login_handler),
            (r'/register/oauth', OAuth_handler),
        ], 
        debug=config['debug'], 
        cookie_secret=config['cookie_secret'],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        autoescape=None,
    )

def main():
    app = App()
    app.listen(config['web_port'])
    loop = ioloop.IOLoop.current()
    loop.add_callback(db_connect, app)
    loop.start()

async def db_connect(app):
    app.db = await db.Db().connect(None)

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load()
    logger.set_logger('web.log')
    main()