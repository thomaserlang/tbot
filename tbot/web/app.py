import logging, os
from tornado import web, ioloop
from tbot import config, db
from tbot.web import handlers

def App():
    return web.Application(
        [            
            (r'/static/(.*)', web.StaticFileHandler, 
                {'path': os.path.join(os.path.dirname(__file__), 'static/app/dist')}),
            (r'/twitch-login', handlers.connect_twitch.Login_handler),
            (r'/twitch-oauth-login', handlers.connect_twitch.Oauth_redirect_handler),
            (r'/connect', handlers.connect.Handler),
            (r'/connect/twitch', handlers.connect_twitch.Handler),
            (r'/connect/discord', handlers.connect_discord.Handler),
            (r'/connect/spotify', handlers.connect_spotify.Handler),

            (r'/api/twitch/user/mod-of', handlers.api.twitch.mod_of.Handler),
            (r'/api/twitch/channels', handlers.api.twitch.channels.Handler),
            (r'/api/twitch/channels/([0-9]+)/chatlog', handlers.api.twitch.chatlog.Handler),
            (r'/api/twitch/channels/([0-9]+)/user-chatstats', handlers.api.twitch.chatlog.User_stats_handler),
            (r'/api/twitch/channels/([0-9]+)/users', handlers.api.twitch.channel_users.Handler),

            (r'/(.*)', handlers.react.Handler),
        ], 
        login_url='/twitch-login',
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
    config_load('../../tbot.yaml')
    logger.set_logger('web.log')
    main()