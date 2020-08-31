"""
Gambling
"""

from yoyo import step

__depends__ = {'20200521_01_e1QpU-twitch-quotes'}

steps = [
    step('''
        CREATE TABLE `twitch_user_channel_points` (
          `channel_id` VARCHAR(36) NOT NULL,
          `user_id` VARCHAR(36) NOT NULL,
          `user` VARCHAR(36) NOT NULL,
          `points` INT(9) UNSIGNED NULL,
          PRIMARY KEY (`channel_id`, `user_id`));
    '''),
    step('''
        CREATE TABLE `twitch_channel_point_settings` (
          `channel_id` VARCHAR(36) NOT NULL,
          `enabled` TINYINT UNSIGNED NULL DEFAULT 0,
          `points_name` VARCHAR(45) NULL DEFAULT 'points',
          `points_per_min` SMALLINT UNSIGNED NULL DEFAULT '10',
          `points_per_min_sub_multiplier` TINYINT UNSIGNED NULL DEFAULT '2',
          `points_per_sub` SMALLINT UNSIGNED NULL DEFAULT '1000',
          `points_per_cheer` SMALLINT UNSIGNED NULL DEFAULT '2',
          `ignore_users` JSON NULL DEFAULT '[]',
          PRIMARY KEY (`channel_id`));
    '''),
    step('''
        CREATE TABLE `twitch_gambling_slots_settings` (
          `channel_id` VARCHAR(36) NOT NULL,
          `emotes` VARCHAR(500) NULL DEFAULT '[]',
          `emote_pool_size` TINYINT UNSIGNED NULL DEFAULT 3,
          `payout_percent` TINYINT UNSIGNED NULL DEFAULT 100,
          `win_message` VARCHAR(250) NULL,
          `lose_message` VARCHAR(250) NULL,
          `allin_win_message` VARCHAR(250) NULL,
          `allin_lose_message` VARCHAR(250) NULL,
          `min_bet` INT NULL DEFAULT '5',
          `max_bet` INT NULL DEFAULT '0',
          PRIMARY KEY (`channel_id`));
    '''),
    step('''
        CREATE TABLE `twitch_gambling_roulette_settings` (
          `channel_id` VARCHAR(36) NOT NULL,
          `win_chance` TINYINT UNSIGNED NULL DEFAULT '50',
          `win_message` VARCHAR(250) NULL,
          `lose_message` VARCHAR(250) NULL,
          `allin_win_message` VARCHAR(250) NULL,
          `allin_lose_message` VARCHAR(250) NULL,
          `min_bet` INT NULL DEFAULT '5',
          `max_bet` INT NULL DEFAULT '0',
          PRIMARY KEY (`channel_id`));
    '''),
]
