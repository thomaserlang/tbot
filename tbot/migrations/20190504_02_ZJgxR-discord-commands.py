"""
discord_commands
"""

from yoyo import step

__depends__ = {'20190504_01_rueSL-discord-log'}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `discord_commands` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `server_id` VARCHAR(30) NOT NULL,
          `title` VARCHAR(45) NULL DEFAULT NULL,
          `cmd` VARCHAR(20) NOT NULL,
          `response` VARCHAR(500) NOT NULL,
          `enabled` INT(1) NOT NULL DEFAULT '1',
          `public` INT(1) NULL DEFAULT '1',
          `roles` VARCHAR(600) NULL DEFAULT NULL,
          `permissions` VARCHAR(600) NULL DEFAULT NULL,
          `created_at` DATETIME NULL DEFAULT NULL,
          `updated_at` DATETIME NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX `ix_discord_commands_server_id_cmd` (`server_id` ASC, `cmd` ASC));
    ''')
]
