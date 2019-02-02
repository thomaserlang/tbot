"""
twitch_chatlog msg_id
"""

from yoyo import step

__depends__ = {'20190201_01_S30H5-more-filters'}

steps = [
    step('''
        ALTER TABLE `twitch_chatlog` 
        ADD COLUMN `msg_id` VARCHAR(36) NULL DEFAULT NULL AFTER `word_count`;
    ''')
]
