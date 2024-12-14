"""Init

Revision ID: dba3882e4560
Revises:
Create Date: 2024-11-07 21:49:36.509925

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dba3882e4560'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE IF NOT EXISTS
    `discord_chatlog` (
        `id` varchar(30) NOT NULL,
        `server_id` varchar(30) DEFAULT NULL,
        `channel_id` varchar(30) DEFAULT NULL,
        `created_at` datetime DEFAULT NULL,
        `updated_at` datetime DEFAULT NULL,
        `message` text DEFAULT NULL,
        `attachments` text DEFAULT NULL,
        `user` varchar(32) DEFAULT NULL,
        `user_id` varchar(30) DEFAULT NULL,
        `user_discriminator` varchar(10) DEFAULT NULL,
        `deleted` enum('Y', 'N') DEFAULT 'N',
        `deleted_at` datetime DEFAULT NULL,
        `member_nick` varchar(32) DEFAULT NULL,
        PRIMARY KEY (`id`)
    )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `discord_chatlog_versions` (
            `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `entry_id` varchar(30) DEFAULT NULL,
            `created_at` datetime DEFAULT NULL,
            `message` text DEFAULT NULL,
            `attachments` text DEFAULT NULL,
            PRIMARY KEY (`id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `discord_commands` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `server_id` varchar(30) NOT NULL,
            `title` varchar(45) DEFAULT NULL,
            `cmd` varchar(20) NOT NULL,
            `response` varchar(500) NOT NULL,
            `enabled` int(1) NOT NULL DEFAULT 1,
            `public` int(1) DEFAULT 1,
            `roles` varchar(600) DEFAULT NULL,
            `permissions` varchar(600) DEFAULT NULL,
            `created_at` datetime DEFAULT NULL,
            `updated_at` datetime DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `ix_discord_commands_server_id_cmd` (`server_id`, `cmd`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
            `discord_server_join_log` (
                `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `server_id` varchar(30) NOT NULL,
                `action` tinyint(3) unsigned NOT NULL COMMENT '0 is leave 1 is joined',
                `user_id` varchar(30) NOT NULL,
                `user` varchar(32) NOT NULL,
                `user_discriminator` varchar(10) NOT NULL,
                `member_nick` varchar(32) DEFAULT NULL,
                `created_at` datetime NOT NULL,
                PRIMARY KEY (`id`)
            )            
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `discord_voice_join_log` (
            `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `server_id` varchar(30) NOT NULL,
            `user` varchar(32) NOT NULL,
            `user_id` varchar(30) NOT NULL,
            `user_discriminator` varchar(10) NOT NULL,
            `member_nick` varchar(32) DEFAULT NULL,
            `action` tinyint(4) NOT NULL COMMENT '0 is leave 1 is joined',
            `channel_id` varchar(30) NOT NULL,
            `channel_name` varchar(32) NOT NULL,
            `created_at` datetime NOT NULL,
            PRIMARY KEY (`id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_badges` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `sub` int(10) unsigned DEFAULT NULL,
            `bits` int(10) unsigned DEFAULT NULL,
            PRIMARY KEY (`channel_id`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_channels` (
            `channel_id` varchar(36) NOT NULL,
            `name` varchar(25) NOT NULL,
            `active` enum('Y', 'N') DEFAULT 'N',
            `created_at` datetime NOT NULL,
            `updated_at` datetime DEFAULT NULL,
            `twitch_token` varchar(200) DEFAULT NULL,
            `twitch_refresh_token` varchar(200) DEFAULT NULL,
            `twitch_scope` varchar(1000) DEFAULT NULL,
            `discord_server_id` varchar(30) DEFAULT NULL,
            `discord_server_name` varchar(200) DEFAULT NULL,
            `muted` enum('Y', 'N') DEFAULT 'N',
            `chatlog_enabled` enum('Y', 'N') DEFAULT 'Y',
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_channel_admins` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `user` varchar(25) DEFAULT NULL,
            `level` int(11) NOT NULL,
            `created_at` datetime DEFAULT NULL,
            `updated_at` datetime DEFAULT NULL,
            PRIMARY KEY (`channel_id`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_channel_cache` (
            `channel_id` varchar(36) NOT NULL,
            `data` text DEFAULT NULL,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_channel_mods` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            PRIMARY KEY (`channel_id`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_channel_point_settings` (
            `channel_id` varchar(36) NOT NULL,
            `enabled` tinyint(3) unsigned DEFAULT 0,
            `points_name` varchar(45) DEFAULT 'points',
            `points_per_min` smallint(5) unsigned DEFAULT 10,
            `points_per_min_sub_multiplier` tinyint(3) unsigned DEFAULT 2,
            `points_per_sub` smallint(5) unsigned DEFAULT 1000,
            `points_per_cheer` smallint(5) unsigned DEFAULT 2,
            `ignore_users` longtext DEFAULT '[]' CHECK (json_valid(`ignore_users`)),
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_chatlog` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `type` int(3) unsigned NOT NULL DEFAULT 1,
            `created_at` datetime NOT NULL,
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `user` varchar(25) DEFAULT NULL,
            `message` varchar(600) DEFAULT NULL,
            `word_count` int(11) DEFAULT 0,
            `msg_id` varchar(36) DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `ix_twitch_chatlog_channel_id_type_user_id_created_at` (`channel_id`, `type`, `user_id`, `created_at`),
            KEY `ix_twitch_chatlog_channel_id_type_created_at` (`channel_id`, `type`, `created_at`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_chat_alerts` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) DEFAULT NULL,
            `type` varchar(45) DEFAULT NULL,
            `message` varchar(200) DEFAULT NULL,
            `min_amount` int(11) DEFAULT NULL,
            PRIMARY KEY (`id`)
        )    
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_commands` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) NOT NULL,
            `title` varchar(45) DEFAULT NULL,
            `cmd` varchar(20) NOT NULL,
            `group_name` varchar(50) DEFAULT NULL,
            `response` varchar(500) NOT NULL,
            `global_cooldown` int(10) unsigned NOT NULL DEFAULT 5,
            `user_cooldown` int(10) unsigned NOT NULL DEFAULT 15,
            `mod_cooldown` int(10) unsigned NOT NULL DEFAULT 0,
            `enabled_status` int(1) unsigned NOT NULL DEFAULT 0,
            `user_level` int(1) unsigned NOT NULL DEFAULT 0,
            `enabled` int(1) NOT NULL DEFAULT 1,
            `public` int(1) DEFAULT 1,
            `created_at` datetime DEFAULT NULL,
            `updated_at` datetime DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `ix_commands_channel_id_cmd` (`channel_id`, `cmd`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_discord_live_notification` (
            `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) NOT NULL,
            `webhook_url` varchar(500) NOT NULL,
            `message` varchar(500) NOT NULL,
            PRIMARY KEY (`id`),
            KEY `channel_id` (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_discord_roles` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) DEFAULT NULL,
            `role_id` varchar(30) DEFAULT NULL,
            `role_name` varchar(45) DEFAULT NULL,
            `type` varchar(45) DEFAULT NULL,
            `value` varchar(45) DEFAULT NULL,
            PRIMARY KEY (`id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_discord_users` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `twitch_id` varchar(36) DEFAULT NULL,
            `discord_id` varchar(30) DEFAULT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `twitch_user_id_UNIQUE` (`twitch_id`),
            UNIQUE KEY `discord_id_UNIQUE` (`discord_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filters` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) NOT NULL,
            `type` varchar(20) NOT NULL,
            `unique` int(1) DEFAULT NULL,
            `name` varchar(100) DEFAULT NULL,
            `enabled` enum('Y', 'N') NOT NULL DEFAULT 'Y',
            `exclude_user_level` int(1) DEFAULT 1,
            `warning_enabled` enum('Y', 'N') NOT NULL DEFAULT 'Y',
            `warning_message` varchar(200) DEFAULT NULL,
            `warning_expire` int(11) unsigned NOT NULL DEFAULT 3600,
            `timeout_message` varchar(200) DEFAULT NULL,
            `timeout_duration` int(11) unsigned NOT NULL DEFAULT 60,
            PRIMARY KEY (`id`),
            UNIQUE KEY `twitch_filters_unique` (`channel_id`, `type`, `unique`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_banned_words` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) NOT NULL,
            `filter_id` int(10) unsigned NOT NULL,
            `banned_words` varchar(1000) DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `ix_twitch_filter_banned_words_channel_id_filter_id` (`channel_id`, `filter_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_caps` (
            `channel_id` varchar(36) NOT NULL,
            `min_length` int(11) DEFAULT 20,
            `max_percent` int(11) DEFAULT 60,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_emote` (
            `channel_id` varchar(36) NOT NULL,
            `max_emotes` int(11) NOT NULL DEFAULT 30,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_link` (
            `channel_id` varchar(36) NOT NULL,
            `whitelist` text DEFAULT NULL,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_non_latin` (
            `channel_id` varchar(36) NOT NULL,
            `min_length` int(11) DEFAULT 5,
            `max_percent` int(11) DEFAULT 90,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_paragraph` (
            `channel_id` varchar(36) NOT NULL,
            `max_length` int(11) NOT NULL DEFAULT 350,
            PRIMARY KEY (`channel_id`)
        ) 
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_filter_symbol` (
            `channel_id` varchar(36) NOT NULL,
            `max_symbols` int(10) unsigned NOT NULL DEFAULT 15,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_gambling_roulette_settings` (
            `channel_id` varchar(36) NOT NULL,
            `win_chance` tinyint(3) unsigned DEFAULT 50,
            `win_message` varchar(250) DEFAULT NULL,
            `lose_message` varchar(250) DEFAULT NULL,
            `allin_win_message` varchar(250) DEFAULT NULL,
            `allin_lose_message` varchar(250) DEFAULT NULL,
            `min_bet` int(11) DEFAULT 5,
            `max_bet` int(11) DEFAULT 0,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_gambling_slots_settings` (
            `channel_id` varchar(36) NOT NULL,
            `emotes` varchar(500) DEFAULT '[]',
            `emote_pool_size` tinyint(3) unsigned DEFAULT 3,
            `payout_percent` tinyint(3) unsigned DEFAULT 100,
            `win_message` varchar(250) DEFAULT NULL,
            `lose_message` varchar(250) DEFAULT NULL,
            `allin_win_message` varchar(250) DEFAULT NULL,
            `allin_lose_message` varchar(250) DEFAULT NULL,
            `min_bet` int(11) DEFAULT 5,
            `max_bet` int(11) DEFAULT 0,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_gambling_stats` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `slots_wins` int(10) unsigned DEFAULT 0,
            `slots_loses` int(10) unsigned DEFAULT 0,
            `roulette_wins` int(10) unsigned DEFAULT 0,
            `roulette_loses` int(10) unsigned DEFAULT 0,
            PRIMARY KEY (`channel_id`, `user_id`)
        ) 
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_modlog` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `created_at` datetime NOT NULL,
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `user` varchar(25) DEFAULT NULL,
            `command` varchar(100) DEFAULT NULL,
            `args` varchar(200) DEFAULT NULL,
            `target_user_id` varchar(36) DEFAULT NULL,
            `target_user` varchar(25) DEFAULT NULL,
            PRIMARY KEY (`id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_quotes` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) DEFAULT NULL,
            `created_by_user_id` varchar(36) DEFAULT NULL,
            `created_by_user` varchar(25) DEFAULT NULL,
            `created_at` datetime DEFAULT NULL,
            `updated_at` datetime DEFAULT NULL,
            `number` int(10) unsigned DEFAULT NULL,
            `message` varchar(400) DEFAULT NULL,
            `enabled` int(1) unsigned DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `ix_twitch_quotes_channel_id_number` (`channel_id`, `number`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_spotify` (
            `channel_id` varchar(36) NOT NULL,
            `token` varchar(500) NOT NULL,
            `refresh_token` varchar(500) NOT NULL,
            `user` varchar(45) DEFAULT NULL,
            PRIMARY KEY (`channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_streams` (
            `stream_id` varchar(75) NOT NULL,
            `channel_id` varchar(36) NOT NULL,
            `started_at` datetime DEFAULT NULL,
            `uptime` int(10) unsigned DEFAULT NULL,
            PRIMARY KEY (`stream_id`)
        ) 
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_stream_watchtime` (
            `channel_id` varchar(36) NOT NULL,
            `stream_id` varchar(75) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `user` varchar(25) DEFAULT NULL,
            `time` int(11) DEFAULT NULL,
            PRIMARY KEY (`channel_id`, `user_id`, `stream_id`)
        ) 
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_subs` (
            `channel_id` varchar(32) NOT NULL,
            `user_id` varchar(32) NOT NULL,
            `tier` varchar(45) NOT NULL,
            `gifter_id` varchar(32) DEFAULT NULL,
            `is_gift` tinyint(4) DEFAULT NULL,
            `created_at` datetime NOT NULL,
            `updated_at` datetime DEFAULT NULL,
            PRIMARY KEY (`channel_id`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_sub_log` (
            `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(32) NOT NULL,
            `message_id` uuid DEFAULT NULL,
            `created_at` datetime(6) NOT NULL,
            `user_id` varchar(32) DEFAULT NULL,
            `message` varchar(2000) DEFAULT NULL,
            `tier` varchar(45) DEFAULT NULL,
            `gifter_id` varchar(32) DEFAULT NULL,
            `is_gift` tinyint(1) NOT NULL DEFAULT 0,
            `total` int(11) DEFAULT NULL,
            `user` varchar(200) DEFAULT NULL,
            `gifter_user` varchar(200) DEFAULT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `message_id_UNIQUE` (`message_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_timers` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `channel_id` varchar(36) NOT NULL,
            `name` varchar(100) DEFAULT NULL,
            `enabled` int(1) NOT NULL DEFAULT 1,
            `interval` int(10) unsigned NOT NULL DEFAULT 5,
            `next_run` datetime DEFAULT NULL,
            `enabled_status` int(1) NOT NULL DEFAULT 0,
            `messages` text DEFAULT NULL,
            `last_sent_message` int(10) unsigned NOT NULL DEFAULT 0,
            `send_message_order` int(1) DEFAULT 1,
            `created_at` datetime DEFAULT NULL,
            `updated_at` datetime DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `ix_twitch_timers_channel_id` (`channel_id`),
            KEY `ix_twitch_timers_enabled_next_run` (`enabled`, `next_run`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_usernames` (
            `user` varchar(25) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `expires` datetime DEFAULT NULL,
            PRIMARY KEY (`user`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_user_channel_points` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `user` varchar(36) NOT NULL,
            `points` int(9) unsigned DEFAULT NULL,
            PRIMARY KEY (`channel_id`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_user_chat_stats` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `bans` int(10) unsigned NOT NULL DEFAULT 0,
            `timeouts` int(10) unsigned NOT NULL DEFAULT 0,
            `purges` int(10) unsigned NOT NULL DEFAULT 0,
            `chat_messages` int(10) unsigned NOT NULL DEFAULT 0,
            `deletes` int(10) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY (`channel_id`, `user_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_user_stats` (
            `channel_id` varchar(36) NOT NULL,
            `user_id` varchar(36) NOT NULL,
            `user` varchar(25) DEFAULT NULL,
            `streams` int(10) unsigned NOT NULL DEFAULT 0,
            `streams_row` int(10) unsigned NOT NULL DEFAULT 0,
            `streams_row_peak` int(10) unsigned NOT NULL DEFAULT 0,
            `streams_row_peak_date` date DEFAULT NULL,
            `last_viewed_stream_id` varchar(75) DEFAULT NULL,
            `last_viewed_stream_date` date DEFAULT NULL,
            PRIMARY KEY (`user_id`, `channel_id`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_widget_keys` (
            `key` varchar(100) NOT NULL,
            `channel_id` varchar(36) DEFAULT NULL,
            `type` varchar(45) DEFAULT NULL,
            `created_at` datetime DEFAULT NULL,
            `settings` longtext DEFAULT NULL CHECK (json_valid(`settings`)),
            PRIMARY KEY (`key`)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS
        `twitch_youtube` (
            `channel_id` varchar(32) NOT NULL,
            `token` varchar(500) NOT NULL,
            `refresh_token` varchar(500) NOT NULL,
            `handle` varchar(500) DEFAULT NULL,
            PRIMARY KEY (`channel_id`)
        ) 
    """)


def downgrade() -> None:
    pass
