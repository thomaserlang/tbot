"""
twitch gambling stats
"""

from yoyo import step

__depends__ = {'20200818_01_A601F-gambling'}

steps = [
    step('''
      CREATE TABLE `twitch_gambling_stats` (
        `channel_id` VARCHAR(36) NOT NULL,
        `user_id` VARCHAR(36) NOT NULL,
        `slots_wins` INT UNSIGNED NULL DEFAULT 0,
        `slots_loses` INT UNSIGNED NULL DEFAULT 0,
        `roulette_wins` INT UNSIGNED NULL DEFAULT 0,
        `roulette_loses` INT UNSIGNED NULL DEFAULT 0,
        PRIMARY KEY (`channel_id`, `user_id`));
    ''')
]
