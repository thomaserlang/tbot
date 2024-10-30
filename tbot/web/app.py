import asyncio
import logging
import os
import signal
from functools import partial

import aiohttp
import aioredis
from tornado import web

from tbot import config, db
from tbot.web import handlers
from tbot.web.io_sighandler import sig_handler


def App():
    return web.Application(
        [            
            (r'/static/(.*)', web.StaticFileHandler, 
                {'path': os.path.join(os.path.dirname(__file__), 'static')}),
            (r'/(favicon.ico)', web.StaticFileHandler, 
                {"path": os.path.join(os.path.dirname(__file__), 'static')}),

            (r'/health', handlers.health.Handler),
            (r'/twitch/login', handlers.api.twitch.oauth.Login_handler),
            (r'/twitch/logout', handlers.api.twitch.oauth.Logout_handler),
            (r'/connect/twitch', handlers.api.twitch.oauth.Handler),
            (r'/connect/spotify', handlers.api.twitch.connect_spotify.Receive_handler),
            (r'/connect/discord', handlers.api.twitch.connect_discord.Receive_handler),
            (r'/connect/youtube', handlers.api.twitch.connect_youtube.Receive_handler),
            (r'/api/twitch/user/mod-of', handlers.api.twitch.mod_of.Handler),
            (r'/api/twitch/user/admin-of', handlers.api.twitch.admin_of.Handler),
            (r'/api/twitch/channel/([a-zA-Z0-9_]+)', handlers.api.twitch.channels.Single_handle),
            (r'/api/twitch/channels', handlers.api.twitch.channels.Handler),
            (r'/api/twitch/channels/([0-9]+)/chatlog', handlers.api.twitch.chatlog.Handler),
            (r'/api/twitch/channels/([0-9]+)/user-chatstats', handlers.api.twitch.chatlog.User_stats_handler),
            (r'/api/twitch/channels/([0-9]+)/user-streams-watched', handlers.api.twitch.chatlog.User_streams_watched_handler),
            (r'/api/twitch/channels/([0-9]+)/user-akas', handlers.api.twitch.chatlog.User_akas_handler),
            (r'/api/twitch/channels/([0-9]+)/users', handlers.api.twitch.channel_users.Handler),
            (r'/api/twitch/channels/([0-9]+)/bot-join', handlers.api.twitch.control_bot.Join_handler),
            (r'/api/twitch/channels/([0-9]+)/bot-mute', handlers.api.twitch.control_bot.Mute_handler),
            (r'/api/twitch/channels/([0-9]+)/bot-enable-chatlog', handlers.api.twitch.control_bot.Enable_chatlog_handler),
            (r'/api/twitch/channels/([0-9]+)/bot-settings', handlers.api.twitch.control_bot.Settings_handler),
            (r'/api/twitch/channels/([0-9]+)/commands', handlers.api.twitch.commands.Collection_handler),
            (r'/api/twitch/channels/([0-9]+)/commands/([0-9]+)', handlers.api.twitch.commands.Handler),
            (r'/api/twitch/channels/([0-9]+)/commands-public', handlers.api.twitch.commands.Public_collection),
            (r'/api/twitch/template-commands', handlers.api.twitch.commands.Template_collection),
            (r'/api/twitch/channels/([0-9]+)/quotes', handlers.api.twitch.quotes.Collection_handler),
            (r'/api/twitch/channels/([0-9]+)/quotes/([0-9]+)', handlers.api.twitch.quotes.Handler),
            (r'/api/twitch/channels/([0-9]+)/admins', handlers.api.twitch.admin_of.Channel_admins),
            (r'/api/twitch/channels/([0-9]+)/admins/([0-9]+)', handlers.api.twitch.admin_of.Channel_admins),
            (r'/api/twitch/channels/([0-9]+)/filters', handlers.api.twitch.filters.Filters),
            (r'/api/twitch/channels/([0-9]+)/filters/link', handlers.api.twitch.filters.Filter_link),
            (r'/api/twitch/channels/([0-9]+)/filters/paragraph', handlers.api.twitch.filters.Filter_paragraph),
            (r'/api/twitch/channels/([0-9]+)/filters/symbol', handlers.api.twitch.filters.Filter_symbol),
            (r'/api/twitch/channels/([0-9]+)/filters/caps', handlers.api.twitch.filters.Filter_caps),
            (r'/api/twitch/channels/([0-9]+)/filters/emote', handlers.api.twitch.filters.Filter_emote),
            (r'/api/twitch/channels/([0-9]+)/filters/non-latin', handlers.api.twitch.filters.Filter_non_latin),
            (r'/api/twitch/channels/([0-9]+)/filters/action', handlers.api.twitch.filters.Filter_action),
            (r'/api/twitch/channels/([0-9]+)/filters/banned-words-groups', handlers.api.twitch.filter_banned_words.Groups_handler),
            (r'/api/twitch/channels/([0-9]+)/filters/banned-words-groups/([0-9]+)', handlers.api.twitch.filter_banned_words.Group_handler),
            (r'/api/twitch/channels/([0-9]+)/filters/banned-words-groups/([0-9]+)/banned-words', handlers.api.twitch.filter_banned_words.Banned_words_handler),
            (r'/api/twitch/channels/([0-9]+)/filters/banned-words-groups/([0-9]+)/banned-words/([0-9]+)', handlers.api.twitch.filter_banned_words.Banned_words_handler),
            (r'/api/twitch/channels/([0-9]+)/filters/banned-words-groups/([0-9]+)/test', handlers.api.twitch.filter_banned_words.Banned_words_test_handler),
            (r'/api/twitch/channels/([0-9]+)/timers', handlers.api.twitch.timers.Collection_handler),
            (r'/api/twitch/channels/([0-9]+)/timers/([0-9]+)', handlers.api.twitch.timers.Handler),
            (r'/api/twitch/channels/([0-9]+)/chat-alerts', handlers.api.twitch.chat_alerts.Handler),            
            (r'/api/twitch/channels/([0-9]+)/points-settings', handlers.api.twitch.gambling.Points_settings_handler),
            (r'/api/twitch/channels/([0-9]+)/gambling-slots-settings', handlers.api.twitch.gambling.Slots_handler),
            (r'/api/twitch/channels/([0-9]+)/gambling-roulette-settings', handlers.api.twitch.gambling.Roulette_handler),            
            (r'/api/twitch/channels/([0-9]+)/spotify', handlers.api.twitch.connect_spotify.Handler),
            (r'/api/twitch/channels/([0-9]+)/discord', handlers.api.twitch.connect_discord.Handler),
            (r'/api/twitch/channels/([0-9]+)/youtube', handlers.api.twitch.connect_youtube.Handler),
            (r'/api/twitch/channels/([0-9]+)/discord-live-notification', handlers.api.twitch.discord_live_notification.Handler),            
            (r'/api/twitch/channels/([0-9]+)/check-extra-auth', handlers.api.twitch.check_extra_auth.Handler),
            (r'/api/twitch/channels/([0-9]+)/commercial', handlers.api.twitch.commercial.Handler),
            (r'/api/twitch/channels/([0-9]+)/self-subs', handlers.api.twitch.self_subs.Handler),
            (r'/api/live-chat/([0-9]+)', handlers.api.live_chat.LiveChatHandler),
            
            (r'/api/rtmp-auth', handlers.api.rtmp_auth.Handler),
            (r'/api/srt-auth', handlers.api.srt_auth.Handler),
            
            (r'/api/twitch/webhooks/channel.subscribe', handlers.api.twitch.eventsubs.channel_subscribe.Handler),
            (r'/api/twitch/webhooks/channel.subscribe.end', handlers.api.twitch.eventsubs.channel_subscribe_end.Handler),
            
            (r"/api/twitch/widget-ws", handlers.api.twitch.widgets.widget_ws.Handler),
            
            (r"/twitch/widgets/goal/([a-zA-Z0-9]+)", handlers.twitch.widgets.goal.Handler),

            (r'/(.*)', handlers.react.Handler),
        ], 
        login_url='/twitch-login',
        debug=config.data.debug, 
        cookie_secret=config.data.web.cookie_secret,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        autoescape=None,
    )

async def main():
    app = App()
    server = app.listen(config.data.web.port)

    app.db = await db.Db().connect()
    app.redis = await aioredis.create_redis_pool(
        f'redis://{config.data.redis.host}:{config.data.redis.port}',
        minsize=config.data.redis.pool_min_size, 
        maxsize=config.data.redis.pool_max_size,
    )
    app.ahttp = aiohttp.ClientSession() 

    signal.signal(signal.SIGTERM, partial(sig_handler, server, app))
    signal.signal(signal.SIGINT, partial(sig_handler, server, app))

    logging.getLogger('tornado.access').setLevel(config.data.logging.level.upper())
    log = logging.getLogger('main')
    log.setLevel('INFO')
    log.info(f'Web server started on port: {config.data.web.port}')
    await asyncio.Event().wait()
    log.info('Web server stopped')