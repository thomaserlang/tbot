"""
drop twitch_chatlog insert trigger
"""

from yoyo import step

__depends__ = {'20190126_01_zvBuo-twitch-user-chat-deleted-counter'}

steps = [
    step('''
        DROP TRIGGER IF EXISTS `twitch_chatlog_AFTER_INSERT`
    ''')
]
