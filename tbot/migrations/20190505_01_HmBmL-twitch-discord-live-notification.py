"""
twitch_discord_live_notification
"""

from yoyo import step

__depends__ = {'20190504_02_ZJgxR-discord-commands'}

steps = [
    step('''
    CREATE TABLE `twitch_discord_live_notification` (
        `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
        `channel_id` VARCHAR(36) NOT NULL,
        `webhook_url` VARCHAR(500) NOT NULL,
        `message` VARCHAR(500) NOT NULL,
        PRIMARY KEY (`id`),
        INDEX `channel_id` (`channel_id`)
    );
    ''')
]
