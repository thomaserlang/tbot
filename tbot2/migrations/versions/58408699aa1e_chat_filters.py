"""Chat filters

Revision ID: 58408699aa1e
Revises: 0264fe26cc59
Create Date: 2025-03-21 20:14:26.219070

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '58408699aa1e'
down_revision: str | None = '0264fe26cc59'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'chat_filters',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(255), nullable=False, server_default='all'),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('enabled', sa.Boolean, nullable=False),
        sa.Column('exclude_access_level', sa.SmallInteger, nullable=False),
        sa.Column('warning_enabled', sa.Boolean, nullable=False),
        sa.Column('warning_message', sa.String(600), nullable=False),
        sa.Column(
            'warning_expire_duration', sa.Integer, nullable=False, comment='seconds'
        ),
        sa.Column('timeout_message', sa.String(600), nullable=False),
        sa.Column('timeout_duration', sa.Integer, nullable=False, comment='seconds'),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('old_id', sa.Integer, nullable=True),
        sa.Index('ix_chat_filters_channel_id_type', 'channel_id', 'type'),
    )
    op.execute("""
        insert into chat_filters 
            (id, old_id, channel_id, type, name, enabled, exclude_access_level, 
            warning_enabled, warning_message, warning_expire_duration, 
            timeout_message, timeout_duration) 
        select uuid_v7(), f.id, c.id, f.type, 
               ifnull(f.name, concat(f.type, ' filter')), 
               if(f.enabled="Y", 1, 0), 
               f.exclude_user_level, 
               if(f.warning_enabled="Y", 1, 0), f.warning_message, f.warning_expire, 
               f.timeout_message, 
               f.timeout_duration from twitch_filters f, channels c where 
               c.twitch_id = f.channel_id
    """)
    op.execute('update chat_filters set type="banned_terms" where type="banned_words"')
    op.execute('update chat_filters set type="non_latin" where type="non-latin"')
    op.execute("""
        update 
            chat_filters f, twitch_filter_caps fc, channels c
        set 
            f.settings=JSON_OBJECT('min_length', fc.min_length, 
               'max_percent', fc.max_percent) 
        where
            c.twitch_id = fc.channel_id AND f.channel_id = c.id AND f.type="caps";
    """)
    op.execute("""
        update 
            chat_filters f, twitch_filter_emote fc, channels c
        set 
            f.settings=JSON_OBJECT('max_emotes', fc.max_emotes) 
        where
            c.twitch_id = fc.channel_id AND f.channel_id = c.id AND f.type="emote";
    """)
    op.execute("""
        update 
            chat_filters f, twitch_filter_non_latin fc, channels c
        set 
            f.settings=JSON_OBJECT('min_length', fc.min_length, 
               'max_percent', fc.max_percent) 
        where
            c.twitch_id = fc.channel_id AND f.channel_id = c.id AND f.type="non_latin";
    """)
    op.execute("""
        update 
            chat_filters f, twitch_filter_paragraph fc, channels c
        set 
            f.settings=JSON_OBJECT('max_length', fc.max_length) 
        where
            c.twitch_id = fc.channel_id AND f.channel_id = c.id AND f.type="paragraph";
    """)
    op.execute("""
        update 
            chat_filters f, twitch_filter_symbol fc, channels c
        set 
            f.settings=JSON_OBJECT('max_symbols', fc.max_symbols) 
        where
            c.twitch_id = fc.channel_id AND f.channel_id = c.id AND f.type="symbol";
    """)

    op.create_table(
        'chat_filter_banned_terms',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column(
            'chat_filter_id',
            sa.UUID(),
            sa.ForeignKey('chat_filters.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('text', sa.String(2000), nullable=False),
        sa.Column('type', sa.String(255), nullable=False),
    )
    op.execute("""
        insert into chat_filter_banned_terms 
            (id, chat_filter_id, text, type) 
        select uuid_v7(), f.id, w.banned_words, 
            if(left(w.banned_words, 3) = "re:", "regex", "phrase") 
        from twitch_filter_banned_words w, chat_filters f where f.old_id = w.filter_id
    """)

    op.create_table(
        'chat_filter_link_allowlist',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column(
            'chat_filter_id',
            sa.UUID(),
            sa.ForeignKey('chat_filters.id', onupdate='CASCADE', ondelete='CASCADE'),
            primary_key=True,
        ),
        sa.Column('url', sa.String(255), nullable=False),
    )


def downgrade() -> None:
    pass
