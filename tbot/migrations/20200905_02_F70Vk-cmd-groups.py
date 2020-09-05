"""
cmd groups
"""

from yoyo import step

__depends__ = {'20200905_01_1kQmN-twitch-gambling-stats'}

steps = [
    step('''
        ALTER TABLE `twitch_commands` 
        ADD COLUMN `group_name` VARCHAR(50) NULL AFTER `cmd`;
    ''')
]
