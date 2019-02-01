import logging, os
import aioredis
from tornado import web, ioloop
from tbot import config, db
from tbot.web import handlers

def App():
    return web.Application(
        [            
            (r'/static/(.*)', web.StaticFileHandler, 
                {'path': os.path.join(os.path.dirname(__file__), 'static/app/dist')}),
            (r'/(favicon.ico)', web.StaticFileHandler, 
                {"path": os.path.join(os.path.dirname(__file__), 'static')}),

            (r'/twitch/login', handlers.api.twitch.oauth.Login_handler),
            (r'/twitch/logout', handlers.api.twitch.oauth.Logout_handler),
            (r'/connect/twitch', handlers.api.twitch.oauth.Handler),
            (r'/connect/spotify', handlers.api.twitch.connect_spotify.Receive_handler),
            (r'/connect/discord', handlers.api.twitch.connect_discord.Receive_handler),
            (r'/api/twitch/user/mod-of', handlers.api.twitch.mod_of.Handler),
            (r'/api/twitch/user/admin-of', handlers.api.twitch.admin_of.Handler),
            (r'/api/twitch/channel/([a-zA-Z0-9_]+)', handlers.api.twitch.channels.Single_handle),
            (r'/api/twitch/channels', handlers.api.twitch.channels.Handler),
            (r'/api/twitch/channels/([0-9]+)/chatlog', handlers.api.twitch.chatlog.Handler),
            (r'/api/twitch/channels/([0-9]+)/user-chatstats', handlers.api.twitch.chatlog.User_stats_handler),
            (r'/api/twitch/channels/([0-9]+)/users', handlers.api.twitch.channel_users.Handler),
            (r'/api/twitch/channels/([0-9]+)/bot-join', handlers.api.twitch.control_bot.Join_handler),
            (r'/api/twitch/channels/([0-9]+)/bot-mute', handlers.api.twitch.control_bot.Mute_handler),
            (r'/api/twitch/channels/([0-9]+)/bot-enable-chatlog', handlers.api.twitch.control_bot.Enable_chatlog_handler),
            (r'/api/twitch/channels/([0-9]+)/bot-settings', handlers.api.twitch.control_bot.Settings_handler),
            (r'/api/twitch/channels/([0-9]+)/commands', handlers.api.twitch.commands.Collection_handler),
            (r'/api/twitch/channels/([0-9]+)/commands/([0-9]+)', handlers.api.twitch.commands.Handler),
            (r'/api/twitch/channels/([0-9]+)/commands-public', handlers.api.twitch.commands.Public_collection),
            (r'/api/twitch/template-commands', handlers.api.twitch.commands.Template_collection),
            (r'/api/twitch/channels/([0-9]+)/admins', handlers.api.twitch.admin_of.Channel_admins),
            (r'/api/twitch/channels/([0-9]+)/admins/([0-9]+)', handlers.api.twitch.admin_of.Channel_admins),
            (r'/api/twitch/channels/([0-9]+)/filters', handlers.api.twitch.filters.Filters),
            (r'/api/twitch/channels/([0-9]+)/filters/link', handlers.api.twitch.filters.Filter_link),

            (r'/api/twitch/channels/([0-9]+)/spotify', handlers.api.twitch.connect_spotify.Handler),
            (r'/api/twitch/channels/([0-9]+)/discord', handlers.api.twitch.connect_discord.Handler),
            
            (r'/api/twitch/channels/([0-9]+)/check-extra-auth', handlers.api.twitch.check_extra_auth.Handler),

            (r'/(.*)', handlers.react.Handler),
        ], 
        login_url='/twitch-login',
        debug=config['debug'], 
        cookie_secret=config['web']['cookie_secret'],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        autoescape=None,
    )

def main():
    app = App()
    app.listen(config['web']['port'])
    loop = ioloop.IOLoop.current()
    loop.add_callback(db_connect, app)
    loop.start()

async def db_connect(app):
    app.db = await db.Db().connect(None)
    app.redis = await aioredis.create_redis_pool(
        'redis://{}:{}'.format(config['redis']['host'], config['redis']['port']),
        minsize=config['redis']['pool_min_size'], 
        maxsize=config['redis']['pool_max_size'],
    )

if __name__ == '__main__':
    from tbot import config_load, logger
    config_load('../../tbot.yaml')
    logger.set_logger('web.log')
    main()