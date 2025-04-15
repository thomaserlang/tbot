"""Timers refactor

Revision ID: ed3a31bb7fb6
Revises: f14045abd0ec
Create Date: 2025-04-04 19:28:41.440782

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ed3a31bb7fb6'
down_revision: str | None = 'f14045abd0ec'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_timers',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('messages', sa.JSON(), nullable=False),
        sa.Column('interval', sa.SmallInteger(), nullable=False, comment='minutes'),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('next_run_at', sa.DateTime(), nullable=False),
        sa.Column('provider', sa.String(255), nullable=False, server_default='all'),
        sa.Column('pick_mode', sa.String(255), nullable=False, server_default='order'),
        sa.Column(
            'active_mode', sa.String(255), nullable=False, server_default='always'
        ),
        sa.Column('last_message_index', sa.SmallInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Index('ix_channel_timers_enabled_next_run_at', 'enabled', 'next_run_at'),
    )

    op.execute("""
        INSERT INTO channel_timers (id, channel_id, name, messages, `interval`, enabled,
                created_at, updated_at, last_message_index, pick_mode, 
               active_mode, next_run_at)
        SELECT 
            uuid_v7(), 
            c.id as channel_id, 
            t.name,
            CONCAT('["', REPLACE(t.messages, '\n', '","'), '"]'),
            t.interval,
            t.enabled,
            t.created_at,
            t.updated_at,
            t.last_sent_message,
            if(t.send_message_order=1, 'order', 'random'),
            case t.enabled_status 
                when 0 then 'always'
                when 1 then 'online'
                when 2 then 'offline'
            end as active_mode,
            t.next_run
        FROM twitch_timers t, channels c where c.twitch_id = t.channel_id
    """)


def downgrade() -> None:
    pass
