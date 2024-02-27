"""

"""

from yoyo import step

__depends__ = {'20240227_02_S1sXT'}

steps = [
    step('''
        ALTER TABLE `twitch_subs` ADD COLUMN `created_at` datetime NOT NULL AFTER `is_gift`;
    ''')
]
