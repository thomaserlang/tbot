"""
twitch user chat deleted counter
"""

from yoyo import step

__depends__ = {'20190125_01_00zOx-init'}

steps = [
    step('''
        UPDATE twitch_user_chat_stats c SET bans=(SELECT count(m.id) FROM twitch_modlog m WHERE m.channel_id=c.channel_id AND m.target_user_id=c.user_id AND command='ban');
    '''),
    step('''
        UPDATE twitch_user_chat_stats c SET timeouts=(SELECT count(m.id) FROM twitch_modlog m WHERE m.channel_id=c.channel_id AND m.target_user_id=c.user_id AND command='timeout');
    '''),
    step('''
        UPDATE twitch_user_chat_stats SET purges=0;
    '''),
    step('''
        UPDATE twitch_user_chat_stats SET chat_messages=0 WHERE chat_messages is null;
    '''),
    step('''
        ALTER TABLE `twitch_user_chat_stats` 
        ADD COLUMN `deletes` INT(10) UNSIGNED NOT NULL DEFAULT 0 AFTER `chat_messages`,
        CHANGE COLUMN `bans` `bans` INT(10) UNSIGNED NOT NULL DEFAULT 0 ,
        CHANGE COLUMN `timeouts` `timeouts` INT(10) UNSIGNED NOT NULL DEFAULT 0 ,
        CHANGE COLUMN `purges` `purges` INT(10) UNSIGNED NOT NULL DEFAULT 0 ,
        CHANGE COLUMN `chat_messages` `chat_messages` INT(10) UNSIGNED NOT NULL DEFAULT 0 ;
    '''),
]