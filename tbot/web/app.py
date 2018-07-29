import logging, os
from tornado import web, ioloop
from tbot import config, db
from tbot.web import handlers

def App():
    return web.Application(
        [
            (r'/connect', handlers.connect.Handler),
            (r'/connect/twitch', handlers.connect_twitch.Handler),
            (r'/connect/discord', handlers.connect_discord.Handler),
        ], 
        login_url='/connect/twitch',
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