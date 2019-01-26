"""
twitch user chat deleted counter
"""

from yoyo import step

__depends__ = {'20190125_01_00zOx-init'}

steps = [
    step('''
        UPDATE twitch_user_chat_stats SET bans=0 WHERE bans is null
    '''),
    step('''
        UPDATE twitch_user_chat_stats SET timeouts=0 WHERE timeouts is null
    '''),
    step('''
        UPDATE twitch_user_chat_stats SET purges=0 WHERE purges is null
    '''),
    step('''
        UPDATE twitch_user_chat_stats SET chat_messages=0 WHERE chat_messages is null
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