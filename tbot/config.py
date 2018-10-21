import os, yaml

config = {
    'debug': False,
    'web': {
        'port': 8001,
        'cookie_secret': '',
        'name': 'TBot',
    },
    'twitch': {
        'user': '',
        'token': '',
        'client_id': '',
        'client_secret': '',
        'redirect_uri': '',        
        'irc_host': 'irc.chat.twitch.tv',
        'irc_port': 6697,
        'irc_use_ssl': True,
        'check_channels_every': 60, # seconds
        'delay_offline': 0, # seconds
        'pubsub_url': 'wss://pubsub-edge.twitch.tv',
    },
    'discord': {
        'client_id': None,
        'client_secret': None,
        'redirect_uri': None,
        'permissions': 268486656,
        'token': None,
        'bot': True,
        'user_token': None,
        'twitch_sync_every': 3600,
    },
    'spotify': {
        'client_id': None,
        'client_secret': None,
        'redirect_uri': None,
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
    }
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
        data = yaml.load(f)
    for key in data:
        if key in config:
            if isinstance(config[key], dict):
                config[key].update(data[key])
            else:
                config[key] = data[key]