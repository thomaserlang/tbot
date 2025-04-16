"""Channels table

Revision ID: a96a1d4bfa03
Revises: cdb4011c1026
Create Date: 2024-11-08 16:24:50.409107

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from uuid6 import uuid7

# revision identifiers, used by Alembic.
revision: str = 'a96a1d4bfa03'
down_revision: str | None = 'cdb4011c1026'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channels',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column('display_name', sa.String(200), nullable=False),
        sa.Column('twitch_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('bot_active', sa.Boolean(), nullable=False),
        sa.Column('bot_muted', sa.Boolean(), nullable=False),
        sa.Column('bot_chatlog_enabled', sa.Boolean(), nullable=False),
    )

    conn = op.get_bind()
    query = conn.execute(
        sa.text(
            'SELECT channel_id, name, active, created_at, muted, chatlog_enabled '
            'FROM twitch_channels'
        )
    )
    results = query.fetchall()
    for result in results:
        conn.execute(
            sa.text(
                'INSERT INTO channels (id, display_name, twitch_id, created_at, '
                'bot_active, bot_muted, bot_chatlog_enabled) VALUES (:id, \
                    :display_name, :twitch_id, :created_at, :bot_active, :bot_muted, '
                ':bot_chatlog_enabled)'
            ),
            {
                'id': uuid7(),
                'display_name': result[1],
                'twitch_id': result[0],
                'created_at': result[3],
                'bot_active': result[2] == 'Y',
                'bot_muted': result[4] == 'Y',
                'bot_chatlog_enabled': result[5] == 'Y',
            },
        )

    op.alter_column(
        'chatlogs',
        'user_id',
        existing_type=sa.String(255),
        new_column_name='chatter_id',
    )
    op.alter_column(
        'chatlogs',
        'user',
        existing_type=sa.String(25),
        new_column_name='chatter_name',
        type_=sa.String(200),
    )
    op.alter_column(
        'chatlogs',
        'user_display_name',
        existing_type=sa.String(255),
        new_column_name='chatter_display_name',
        type_=sa.String(200),
    )
    op.alter_column(
        'chatlogs',
        'user_color',
        existing_type=sa.String(7),
        new_column_name='chatter_color',
    )
    op.alter_column(
        'chatlogs',
        'channel_id',
        existing_type=sa.String(255),
        new_column_name='provider_id',
    )
    op.add_column('chatlogs', sa.Column('channel_id', sa.UUID, nullable=True))
    op.execute(
        'UPDATE chatlogs SET channel_id = (SELECT id FROM channels WHERE twitch_id = '
        'chatlogs.provider_id)'
    )
    op.alter_column(
        'chatlogs',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.create_index('ix_chatlogs_channel_id', 'chatlogs', ['channel_id'])

    op.alter_column(
        'chatlog_chatter_stats',
        'user_id',
        new_column_name='provider_viewer_id',
        existing_type=sa.String(255),
    )
    op.alter_column(
        'chatlog_chatter_stats',
        'channel_id',
        existing_type=sa.String(255),
        new_column_name='provider_id',
    )
    op.add_column(
        'chatlog_chatter_stats', sa.Column('channel_id', sa.UUID, nullable=True)
    )
    op.execute(
        'UPDATE chatlog_chatter_stats SET channel_id = '
        '(SELECT id FROM channels WHERE '
        'twitch_id = chatlog_chatter_stats.provider_id)'
    )

    op.drop_constraint(
        'chatlog_chatter_stats_pkey',
        'chatlog_chatter_stats',
        type_='primary',
    )
    op.add_column(
        'chatlog_chatter_stats',
        sa.Column('provider', sa.String(255), nullable=False, server_default='twitch'),
    )
    op.create_primary_key(
        'chatlog_chatter_stats_pkey',
        'chatlog_chatter_stats',
        ['channel_id', 'provider', 'provider_viewer_id'],
    )

    op.alter_column(
        'chatlog_chatter_stats',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.drop_column('chatlog_chatter_stats', 'provider_id')

    op.alter_column(
        'provider_viewer_name_history',
        'user_id',
        new_column_name='provider_viewer_id',
        existing_type=sa.String(255),
    )
    op.alter_column(
        'provider_viewer_name_history',
        'user',
        existing_type=sa.String(25),
        new_column_name='name',
        type_=sa.String(200),
    )
    op.add_column(
        'provider_viewer_name_history', sa.Column('display_name', sa.String(200))
    )
    op.execute('UPDATE provider_viewer_name_history SET display_name = name')
    op.alter_column(
        'provider_viewer_name_history',
        'display_name',
        existing_type=sa.String(200),
        nullable=False,
    )
    op.drop_constraint('viewers_pkey', 'provider_viewer_name_history', type_='primary')
    op.create_primary_key(
        'provider_viewer_name_history_pkey',
        'provider_viewer_name_history',
        ['provider', 'provider_viewer_id', 'name'],
    )
    op.create_index(
        'channel_provider_ix_display_name',
        'provider_viewer_name_history',
        ['display_name'],
    )


def downgrade() -> None:
    pass
