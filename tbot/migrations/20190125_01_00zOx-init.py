"""
yoyo new ./migrations -m "message" -b

Init
"""

from yoyo import step

__depends__ = {}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_badges` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `user_id` INT(11) UNSIGNED NOT NULL,
          `sub` INT(10) UNSIGNED NULL DEFAULT NULL,
          `bits` INT(10) UNSIGNED NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`, `user_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_channel_admins` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `user_id` INT(11) UNSIGNED NOT NULL,
          `user` VARCHAR(25) NULL DEFAULT NULL,
          `level` INT(11) NOT NULL,
          `created_at` DATETIME NULL DEFAULT NULL,
          `updated_at` DATETIME NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`, `user_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_channel_cache` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `data` TEXT NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_channel_mods` (
          `channel_id` INT(10) UNSIGNED NOT NULL,
          `user_id` INT(10) UNSIGNED NOT NULL,
          PRIMARY KEY (`channel_id`, `user_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_channels` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `name` VARCHAR(25) NOT NULL,
          `active` ENUM('Y', 'N') NULL DEFAULT 'N',
          `created_at` DATETIME NOT NULL,
          `updated_at` DATETIME NULL DEFAULT NULL,
          `twitch_token` VARCHAR(200) NULL DEFAULT NULL,
          `twitch_refresh_token` VARCHAR(200) NULL DEFAULT NULL,
          `twitch_scope` VARCHAR(500) NULL DEFAULT NULL,
          `discord_server_id` VARCHAR(30) NULL DEFAULT NULL,
          `discord_server_name` VARCHAR(200) NULL DEFAULT NULL,
          `muted` ENUM('Y', 'N') NULL DEFAULT 'N',
          `chatlog_enabled` ENUM('Y', 'N') NULL DEFAULT 'Y',
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_chat_alerts` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `channel_id` INT(11) UNSIGNED NULL DEFAULT NULL,
          `type` VARCHAR(45) NULL DEFAULT NULL,
          `message` VARCHAR(200) NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          UNIQUE INDEX `ix_type_value` (`channel_id` ASC, `type` ASC))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_chatlog` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `type` INT(3) UNSIGNED NULL DEFAULT NULL,
          `created_at` DATETIME NULL DEFAULT NULL,
          `channel_id` INT(10) UNSIGNED NULL DEFAULT NULL,
          `user_id` INT(10) UNSIGNED NULL DEFAULT NULL,
          `user` VARCHAR(25) NULL DEFAULT NULL,
          `message` VARCHAR(600) NULL DEFAULT NULL,
          `word_count` INT(11) NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX `ix_twitch_chatlog_channel_id_type_user_id_created_at` (`channel_id` ASC, `type` ASC, `user_id` ASC, `created_at` ASC),
          INDEX `ix_twitch_chatlog_channel_id_type_created_at` (`channel_id` ASC, `type` ASC, `created_at` ASC))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_commands` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `title` VARCHAR(45) NULL DEFAULT NULL,
          `cmd` VARCHAR(20) NOT NULL,
          `response` VARCHAR(500) NOT NULL,
          `global_cooldown` INT(10) UNSIGNED NOT NULL DEFAULT '5',
          `user_cooldown` INT(10) UNSIGNED NOT NULL DEFAULT '15',
          `mod_cooldown` INT(10) UNSIGNED NOT NULL DEFAULT '0',
          `enabled_status` INT(1) UNSIGNED NOT NULL DEFAULT '0',
          `user_level` INT(1) UNSIGNED NOT NULL DEFAULT '0',
          `enabled` INT(1) NOT NULL DEFAULT '1',
          `public` INT(1) NULL DEFAULT '1',
          `created_at` DATETIME NULL DEFAULT NULL,
          `updated_at` DATETIME NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX `ix_commands_channel_id_cmd` (`channel_id` ASC, `cmd` ASC))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_discord_roles` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `channel_id` INT(11) UNSIGNED NULL DEFAULT NULL,
          `role_id` VARCHAR(30) NULL DEFAULT NULL,
          `role_name` VARCHAR(45) NULL DEFAULT NULL,
          `type` VARCHAR(45) NULL DEFAULT NULL,
          `value` VARCHAR(45) NULL DEFAULT NULL,
          PRIMARY KEY (`id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_discord_users` (
          `id` INT(11) NOT NULL AUTO_INCREMENT,
          `twitch_id` INT(11) NULL DEFAULT NULL,
          `discord_id` VARCHAR(30) NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          UNIQUE INDEX `twitch_user_id_UNIQUE` (`twitch_id` ASC),
          UNIQUE INDEX `discord_id_UNIQUE` (`discord_id` ASC))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_modlog` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `created_at` DATETIME NULL DEFAULT NULL,
          `channel_id` INT(10) UNSIGNED NULL DEFAULT NULL,
          `user_id` INT(11) NULL DEFAULT NULL,
          `user` VARCHAR(25) NULL DEFAULT NULL,
          `command` VARCHAR(100) NULL DEFAULT NULL,
          `args` VARCHAR(200) NULL DEFAULT NULL,
          `target_user_id` INT(10) UNSIGNED NULL DEFAULT NULL,
          `target_user` VARCHAR(25) NULL DEFAULT NULL,
          PRIMARY KEY (`id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_spotify` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `token` VARCHAR(200) NOT NULL,
          `refresh_token` VARCHAR(200) NOT NULL,
          `user` VARCHAR(45) NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_stream_watchtime` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `stream_id` VARCHAR(75) NOT NULL,
          `user_id` INT(11) UNSIGNED NOT NULL,
          `user` VARCHAR(45) NULL DEFAULT NULL,
          `time` INT(11) NULL DEFAULT NULL,
          PRIMARY KEY (`stream_id`, `user_id`, `channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_streams` (
          `stream_id` VARCHAR(75) NOT NULL,
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `started_at` DATETIME NULL DEFAULT NULL,
          `uptime` INT(10) UNSIGNED NULL DEFAULT NULL,
          PRIMARY KEY (`stream_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_user_chat_stats` (
          `channel_id` INT(10) UNSIGNED NOT NULL,
          `user_id` INT(10) UNSIGNED NOT NULL,
          `bans` INT(10) UNSIGNED NULL DEFAULT NULL,
          `timeouts` INT(10) UNSIGNED NULL DEFAULT NULL,
          `purges` INT(10) UNSIGNED NULL DEFAULT NULL,
          `chat_messages` INT(10) UNSIGNED NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`, `user_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_user_stats` (
          `channel_id` INT(11) UNSIGNED NOT NULL,
          `user_id` INT(11) UNSIGNED NOT NULL,
          `user` VARCHAR(25) NULL DEFAULT NULL,
          `streams` INT(10) UNSIGNED NOT NULL DEFAULT '0',
          `streams_row` INT(10) UNSIGNED NOT NULL DEFAULT '0',
          `streams_row_peak` INT(10) UNSIGNED NOT NULL DEFAULT '0',
          `streams_row_peak_date` DATE NULL DEFAULT NULL,
          `last_viewed_stream_id` VARCHAR(75) NULL DEFAULT NULL,
          `last_viewed_stream_date` DATE NULL DEFAULT NULL,
          PRIMARY KEY (`user_id`, `channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_usernames` (
          `user` VARCHAR(25) NOT NULL,
          `user_id` INT(10) UNSIGNED NOT NULL,
          `expires` DATETIME NULL DEFAULT NULL,
          PRIMARY KEY (`user`, `user_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filters` (
          `channel_id` VARCHAR(36) NOT NULL,
          `type` VARCHAR(20) NOT NULL,
          `enabled` ENUM('Y', 'N') NOT NULL DEFAULT 'Y',
          `exclude_user_level` INT(1) NULL DEFAULT 1,
          `warning_enabled` ENUM('Y', 'N') NOT NULL DEFAULT 'Y',
          `warning_message` VARCHAR(200) NULL DEFAULT NULL,
          `warning_expire` INT(11) UNSIGNED NOT NULL DEFAULT 3600,
          `timeout_message` VARCHAR(200) NULL DEFAULT NULL,
          `timeout_duration` INT(11) UNSIGNED NOT NULL DEFAULT 60,
          PRIMARY KEY (`channel_id`, `type`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_filter_link` (
          `channel_id` VARCHAR(36) NOT NULL,
          `whitelist` TEXT NULL DEFAULT NULL,
          PRIMARY KEY (`channel_id`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),
    step('DROP TRIGGER IF EXISTS `twitch_chatlog_AFTER_INSERT`;'),
    step('''
        CREATE
        TRIGGER `twitch_chatlog_AFTER_INSERT`
        AFTER INSERT ON `twitch_chatlog`
        FOR EACH ROW
        BEGIN
            INSERT IGNORE INTO twitch_usernames (user_id, user, expires) VALUES (new.user_id, new.user, now()+INTERVAL 3 MONTH);
            CASE
                WHEN new.`type` = 1 THEN
                BEGIN
                    insert into twitch_user_chat_stats (channel_id, user_id, chat_messages) VALUES (new.channel_id, new.user_id, 1) ON DUPLICATE KEY UPDATE chat_messages=chat_messages+1;
                END;
                WHEN new.`type` = 2 THEN insert into twitch_user_chat_stats (channel_id, user_id, bans) VALUES (new.channel_id, new.user_id, 1) ON DUPLICATE KEY UPDATE bans=bans+1;
                WHEN new.`type` = 3 THEN insert into twitch_user_chat_stats (channel_id, user_id, timeouts) VALUES (new.channel_id, new.user_id, 1) ON DUPLICATE KEY UPDATE timeouts=timeouts+1;
                WHEN new.`type` = 4 THEN insert into twitch_user_chat_stats (channel_id, user_id, purges) VALUES (new.channel_id, new.user_id, 1) ON DUPLICATE KEY UPDATE purges=purges+1;
                ELSE BEGIN END;
            END CASE;
        END
    '''),
    step('DROP TRIGGER IF EXISTS `twitch_stream_watchtime_AFTER_INSERT`;'),
    step('''
        CREATE
        TRIGGER `twitch_stream_watchtime_AFTER_INSERT`
        AFTER INSERT ON `twitch_stream_watchtime`
        FOR EACH ROW
        BEGIN
            INSERT INTO twitch_user_stats 
                (channel_id, user_id, user, streams, streams_row, streams_row_peak, 
                streams_row_peak_date, last_viewed_stream_id, 
                last_viewed_stream_date)
            VALUES
                (new.channel_id, new.user_id, new.user, 1, 1, 1, date(now()), new.stream_id, date(now()))
            ON DUPLICATE KEY UPDATE 
                user=new.user,
                streams=streams+1,
                streams_row=streams_row+1,
                last_viewed_stream_id=new.stream_id,
                last_viewed_stream_date=date(now());
        END
    '''),
    step('DROP TRIGGER IF EXISTS `twitch_user_stats_BEFORE_UPDATE`;'),
    step('''
        CREATE
        TRIGGER `twitch_user_stats_BEFORE_UPDATE`
        BEFORE UPDATE ON `twitch_user_stats`
        FOR EACH ROW
        BEGIN
            if new.streams_row > new.streams_row_peak then
                set new.streams_row_peak = new.streams_row;
                set new.streams_row_peak_date = date(now());
            end if;
        END
    '''),
]
