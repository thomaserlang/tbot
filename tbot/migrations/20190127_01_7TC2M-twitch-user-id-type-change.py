"""
twitch user id type change
"""

from yoyo import step

__depends__ = {'20190126_02_Fnsd3-drop-twitch-chatlog-insert-trigger'}

steps = [
    step('''
    ALTER TABLE `twitch_badges` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_channel_admins` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_channel_cache` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_channel_mods` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_channels` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_chat_alerts` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NULL DEFAULT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_chatlog` 
    CHANGE COLUMN `type` `type` INT(3) UNSIGNED NOT NULL DEFAULT 1 ,
    CHANGE COLUMN `created_at` `created_at` DATETIME NOT NULL ,
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `word_count` `word_count` INT(11) NULL DEFAULT 0 ;
    '''),
    step('''
    ALTER TABLE `twitch_commands` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_discord_roles` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NULL DEFAULT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_discord_users` 
    CHANGE COLUMN `twitch_id` `twitch_id` VARCHAR(36) NULL DEFAULT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_modlog` 
    CHANGE COLUMN `created_at` `created_at` DATETIME NOT NULL ,
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `target_user_id` `target_user_id` VARCHAR(36) NULL DEFAULT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_spotify` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_stream_watchtime` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user` `user` VARCHAR(25) NULL DEFAULT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_streams` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_user_chat_stats` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_user_stats` 
    CHANGE COLUMN `channel_id` `channel_id` VARCHAR(36) NOT NULL ,
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ;
    '''),
    step('''
    ALTER TABLE `twitch_usernames` 
    CHANGE COLUMN `user_id` `user_id` VARCHAR(36) NOT NULL ;
    '''),
]
