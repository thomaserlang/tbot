import os, yaml

config = {
    'debug': False,
    'check_channels_every': 60, # seconds
    'delay_offline': 0, # seconds
    'user': '',
    'token': '',
    'sql_url': '',
    'client_id': '',
    'client_secret': '',
    'redirect_uri': '',
    'cookie_secret': '',
    'web_port': 8001,
    'irc': {
        'host': 'irc.chat.twitch.tv',
        'port': 6697,
        'use_ssl': True,
    },
    'discord': {
        'token': None,
        'bot': True,
        'user_token': None,
        'twitch_sync_every': 3600,
    },
    'logging': {
        'level': 'warning',
        'path': None,
        'max_size': 100 * 1000 * 1000,# ~ 95 mb
        'num_backups': 10,
    },
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