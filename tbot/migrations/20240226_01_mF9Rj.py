"""

"""

from yoyo import step

__depends__ = {'20221202_01_mHmlh-twitch-stream-watchtime-index'}

steps = [
    step('''
        CREATE TABLE `twitch_sub_log` (
            `channel_id` VARCHAR(32) NOT NULL,
            `message_id` uuid NULL,
            `created_at` DATETIME(6) NOT NULL,
            `user_id` VARCHAR(32) NULL,
            `plan_name` VARCHAR(45) NULL,
            `tier` VARCHAR(45) NULL,
            `gifter_id` VARCHAR(32) NULL,
            `is_gift` BOOLEAN NOT NULL DEFAULT 0,
            `total` INT NULL,
            PRIMARY KEY (`channel_id`),
            UNIQUE INDEX `message_id_UNIQUE` (`message_id` ASC))
    '''),

    step('''
        CREATE TABLE `twitch_sub_stats` (
            `channel_id` VARCHAR(32) NOT NULL,
            `self_sub_points` INT NOT NULL DEFAULT 0,
            `gifted_sub_points` INT NULL DEFAULT 0,
            `primes` INT NULL DEFAULT 0,
            `updated_at` DATETIME(6) NOT NULL,
            PRIMARY KEY (`channel_id`));     
    '''),
]
