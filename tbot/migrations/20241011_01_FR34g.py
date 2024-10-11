"""

"""

from yoyo import step

__depends__ = {'20240227_03_Yv2xH'}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_youtube` (
          `channel_id` VARCHAR(32) NOT NULL,
          `token` VARCHAR(500) NOT NULL,
          `refresh_token` VARCHAR(500) NOT NULL,
          `handle` VARCHAR(500) NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
]
