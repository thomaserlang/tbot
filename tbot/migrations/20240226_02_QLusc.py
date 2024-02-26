"""

"""

from yoyo import step

__depends__ = {'20240226_01_mF9Rj'}

steps = [
    step('''
        CREATE TABLE `twitch_subs` (
            `channel_id` VARCHAR(32) NOT NULL,
            `user_id` VARCHAR(32) NOT NULL,
            `plan_name` VARCHAR(45) NULL,
            `tier` VARCHAR(45) NOT NULL,
            `gifter_id` VARCHAR(32) NULL,
            `is_gift` TINYINT NULL,
            `updated_at` DATETIME NULL,
            PRIMARY KEY (`channel_id`, `user_id`));
    '''),
    
    step('drop table twitch_sub_log'),
    
    step('''
        CREATE TABLE `twitch_sub_log` (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            `channel_id` VARCHAR(32) NOT NULL,
            `message_id` uuid NULL,
            `created_at` DATETIME(6) NOT NULL,
            `user_id` VARCHAR(32) NULL,
            `plan_name` VARCHAR(45) NULL,
            `tier` VARCHAR(45) NULL,
            `gifter_id` VARCHAR(32) NULL,
            `is_gift` BOOLEAN NOT NULL DEFAULT 0,
            `total` INT NULL,
            UNIQUE INDEX `message_id_UNIQUE` (`message_id` ASC))
    '''),
]
