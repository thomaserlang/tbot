"""
twitch_widget_keys
"""

from yoyo import step

__depends__ = {'20200905_02_F70Vk-cmd-groups'}

steps = [
    step('''
        CREATE TABLE `tbot`.`twitch_widget_keys` (
        `key` VARCHAR(100) NOT NULL,
        `channel_id` VARCHAR(36) NULL,
        `type` VARCHAR(45) NULL,
        `created_at` DATETIME NULL,
        `settings` JSON NULL,
        PRIMARY KEY (`key`));
    ''')
]
