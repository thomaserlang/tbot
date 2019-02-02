"""
More filters
"""

from yoyo import step

__depends__ = {'20190202_01_76v6L-twitch-chatlog-msg-id'}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filter_caps` (
          `channel_id` VARCHAR(36) NOT NULL,
          `min_length` INT(11) NULL DEFAULT 20,
          `max_percent` INT(11) NULL DEFAULT 60,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filter_emote` (
          `channel_id` VARCHAR(36) NOT NULL,
          `max_emotes` INT(11) NOT NULL DEFAULT 30,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filter_non_latin` (
          `channel_id` VARCHAR(36) NOT NULL,
          `min_length` INT(11) NULL DEFAULT 5,
          `max_percent` INT(11) NULL DEFAULT 90,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),    
]
