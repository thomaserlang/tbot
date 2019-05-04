"""
discord_log
"""

from yoyo import step

__depends__ = {'20190202_03_8ebYl-twitch-timers'}

steps = [
    step('''
    CREATE TABLE IF NOT EXISTS `discord_chatlog` (
      `id` varchar(30) NOT NULL,
      `server_id` varchar(30) DEFAULT NULL,
      `channel_id` varchar(30) DEFAULT NULL,
      `created_at` datetime DEFAULT NULL,
      `updated_at` datetime DEFAULT NULL,
      `message` text,
      `attachments` text,
      `user` varchar(32) DEFAULT NULL,
      `user_id` varchar(30) DEFAULT NULL,
      `user_discriminator` varchar(10) DEFAULT NULL,
      `deleted` enum('Y','N') DEFAULT 'N',
      `deleted_at` datetime DEFAULT NULL,
      `member_nick` varchar(32) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8mb4;
    '''),
    step('''
    CREATE TABLE IF NOT EXISTS `discord_chatlog_versions` (
      `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
      `entry_id` varchar(30) DEFAULT NULL,
      `created_at` datetime DEFAULT NULL,
      `message` text,
      `attachments` text,
      PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8mb4;
    '''),
    step('''
    CREATE TABLE IF NOT EXISTS `discord_server_join_log` (
        `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
        `server_id` VARCHAR(30) NOT NULL,
        `action` TINYINT UNSIGNED NOT NULL COMMENT '0 is leave 1 is joined',
        `user_id` VARCHAR(30) NOT NULL,
        `user` VARCHAR(32) NOT NULL,
        `user_discriminator` VARCHAR(10) NOT NULL,
        `member_nick` VARCHAR(32) DEFAULT NULL,
        `created_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`)
    ) COLLATE='utf8mb4_unicode_ci';
    '''),
    step('''
    CREATE TABLE IF NOT EXISTS `discord_voice_join_log` (
        `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
        `server_id` VARCHAR(30) NOT NULL,
        `user` VARCHAR(32) NOT NULL,
        `user_id` VARCHAR(30) NOT NULL,
        `user_discriminator` VARCHAR(10) NOT NULL,
        `member_nick` VARCHAR(32) DEFAULT NULL,
        `action` TINYINT NOT NULL COMMENT '0 is leave 1 is joined',
        `channel_id` VARCHAR(30) NOT NULL,
        `channel_name` VARCHAR(32) NOT NULL,
        `created_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`)
    ) COLLATE='utf8mb4_unicode_ci';
    ''')
]
