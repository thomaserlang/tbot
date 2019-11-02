"""
support filter groups
"""

from yoyo import step

__depends__ = {'20191004_01_SbFhm-added-min-amount-to-twitch-chat-alerts'}

steps = [
    step('''
        ALTER TABLE `twitch_filters` 
        ADD COLUMN `id` INT UNSIGNED NOT NULL AUTO_INCREMENT FIRST,
        ADD COLUMN `unique` INT(1) NULL AFTER `type`,
        DROP PRIMARY KEY,
        ADD PRIMARY KEY (`id`),
        ADD UNIQUE INDEX `twitch_filters_unique` (`channel_id` ASC, `type` ASC, `unique` ASC);
    '''),
    step('''
        ALTER TABLE `twitch_filters` 
        ADD COLUMN `name` VARCHAR(100) NULL AFTER `unique`;
    '''),
    step('''
        CREATE TABLE `twitch_filter_banned_words` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `channel_id` VARCHAR(36) NOT NULL,
          `filter_id` INT UNSIGNED NOT NULL,
          `banned_words` VARCHAR(1000) NULL,
          PRIMARY KEY (`id`),
          INDEX `ix_twitch_filter_banned_words_channel_id_filter_id` (`channel_id` ASC, `filter_id` ASC));
    ''')
]
