import os, yaml

config = {
    'debug': False,
    'sentry_dsn': None,
    'web': {
        'port': 8001,
        'cookie_secret': '',
        'name': 'TBot',
        'base_url': 'https://botashell.com'
    },
    'twitch': {
        'username': '',
        'chat_token': '',
        'client_id': '',
        'client_secret': '',
        'irc_host': 'irc.chat.twitch.tv',
        'irc_port': 6697,
        'irc_use_ssl': True,
        'irc_rate_limit': 80, # messages every 30 second
        'check_channels_every': 60, # seconds,
        'check_timers_every': 30, # seconds
        'delay_offline': 0, # seconds
        # Only reset streams in a row if the stream was longer than `stream_min_length`.
        'stream_min_length': 1800,# seconds
        'pubsub_url': 'wss://pubsub-edge.twitch.tv',
        'request_scope':['channel_subscriptions',
                        'channel_check_subscription',
                        'channel_editor',
                        'bits:read',
                        'clips:edit',
                        'user:edit:broadcast',
                        'channel:read:subscriptions',
                        'moderation:read',
                        'channel:edit:commercial',
                        'user:read:broadcast',],
    },
    'discord': {
        'client_id': None,
        'client_secret': None,
        'permissions': 470019158,
        'token': None,
        'bot': True,
        'user_token': None,
        'twitch_sync_every': 3600,
    },
    'spotify': {
        'client_id': None,
        'client_secret': None,
    },
    'logging': {
        'level': 'warning',
        'path': None,
        'max_size': 100 * 1000 * 1000,# ~ 95 mb
        'num_backups': 10,
    },
    'mysql': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'tbot',
    },
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'pool_min_size': 5,
        'pool_max_size': 20,
    },
    'openweathermap_apikey': None,
    'faceit_apikey': None,
    'lol_apikey': None,
    'tft_apikey': None,
    'rtmp_keys': [],
}

def load(path=None):
    default_paths = [
        '~/tbot.yaml',
        './tbot.yaml',
        '../tbot.yaml',
        '/etc/tbot/tbot.yaml',
        '/etc/tbot.yaml',
    ]
    if not path:
        path = os.environ.get('TBOT_CONFIG', None)
        if not path:
            for p in default_paths:
                p = os.path.expanduser(p)
                if os.path.isfile(p):
                    path = p
                    break
    if not path:
        raise Exception('No config file specified.')
    if not os.path.isfile(path):
        raise Exception('Config: "{}" could not be found.'.format(path))
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    for key in data:
        if key in config:
            if isinstance(config[key], dict):
                config[key].update(data[key])
            else:
                config[key] = data[key]