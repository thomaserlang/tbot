"""
More filters
"""

from yoyo import step

__depends__ = {'20190127_01_7TC2M-twitch-user-id-type-change'}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filter_paragraph` (
          `channel_id` VARCHAR(36) NOT NULL,
          `max_length` INT(11) NOT NULL DEFAULT 350,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filter_symbol` (
          `channel_id` VARCHAR(36) NOT NULL,
          `max_symbols` INT(10) UNSIGNED NOT NULL DEFAULT 15,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    ''')
]
