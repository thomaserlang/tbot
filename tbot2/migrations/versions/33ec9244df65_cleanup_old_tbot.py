"""Cleanup old tbot

Revision ID: 33ec9244df65
Revises: f015ac4ddd38
Create Date: 2025-04-22 14:20:27.711920

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '33ec9244df65'
down_revision: str | None = 'f015ac4ddd38'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_table('discord_chatlog')
    op.drop_table('discord_chatlog_versions')
    op.drop_table('discord_commands')
    op.drop_table('discord_server_join_log')
    op.drop_table('discord_voice_join_log')
    op.drop_table('spotify_oauth')
    op.drop_table('twitch_badges')
    op.drop_table('twitch_channels')
    op.drop_table('twitch_channel_admins')
    op.drop_table('twitch_channel_cache')
    op.drop_table('twitch_channel_mods')
    op.drop_table('twitch_chat_alerts')
    op.drop_table('twitch_commands')
    op.drop_table('twitch_discord_live_notification')
    op.drop_table('twitch_discord_roles')
    op.drop_table('twitch_discord_users')
    op.drop_table('twitch_filters')
    op.drop_table('twitch_filter_banned_words')
    op.drop_table('twitch_filter_caps')
    op.drop_table('twitch_filter_emote')
    op.drop_table('twitch_filter_link')
    op.drop_table('twitch_filter_non_latin')
    op.drop_table('twitch_filter_paragraph')
    op.drop_table('twitch_filter_symbol')
    op.drop_table('twitch_modlog')
    op.drop_table('twitch_quotes')
    op.drop_table('twitch_spotify')
    op.drop_table('twitch_streams')
    op.drop_table('twitch_stream_watchtime')
    op.drop_table('twitch_subs')
    op.drop_table('twitch_sub_log')
    op.drop_table('twitch_timers')
    op.drop_table('twitch_user_stats')
    op.drop_table('twitch_widget_keys')
    op.drop_table('twitch_youtube')
    op.drop_table('yoyo_lock', if_exists=True)
    op.drop_table('_yoyo_log', if_exists=True)
    op.drop_table('_yoyo_migration', if_exists=True)
    op.drop_table('_yoyo_version', if_exists=True)


def downgrade() -> None:
    pass
