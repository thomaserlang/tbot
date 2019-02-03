"""
Twitch timers
"""

from yoyo import step

__depends__ = {'20190202_02_oT9XA-more-filters'}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_timers` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `channel_id` VARCHAR(36) NOT NULL,
          `name` VARCHAR(100) NULL DEFAULT NULL,
          `enabled` INT(1) NOT NULL DEFAULT 1,
          `interval` INT(10) UNSIGNED NOT NULL DEFAULT 5,
          `next_run` DATETIME NULL DEFAULT NULL,
          `enabled_status` INT(1) NOT NULL DEFAULT 0,
          `messages` TEXT NULL DEFAULT NULL,
          `last_sent_message` INT(10) UNSIGNED NOT NULL DEFAULT 0,
          `send_message_order` INT(1) NULL DEFAULT 1,
          `created_at` DATETIME NULL DEFAULT NULL,
          `updated_at` DATETIME NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX `ix_twitch_timers_channel_id` (`channel_id` ASC),
          INDEX `ix_twitch_timers_enabled_next_run` (`enabled` ASC, `next_run` ASC))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    ''')
]
