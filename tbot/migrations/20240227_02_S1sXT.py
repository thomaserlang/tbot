"""

"""

from yoyo import step

__depends__ = {'20240227_01_tVr5L'}

steps = [
    step('''
        CREATE TABLE `twitch_subs` (
            `channel_id` VARCHAR(32) NOT NULL,
            `user_id` VARCHAR(32) NOT NULL,
            `tier` VARCHAR(45) NOT NULL,
            `gifter_id` VARCHAR(32) NULL,
            `is_gift` TINYINT NULL,
            `updated_at` DATETIME NULL,
            PRIMARY KEY (`channel_id`, `user_id`));  
    ''')
]
