"""Refactor twitch_user_stats

Revision ID: 189219e5576e
Revises: d8a6ec05016f
Create Date: 2025-03-15 14:24:37.875777

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '189219e5576e'
down_revision: str | None = 'd8a6ec05016f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_viewer_stats',
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(100), nullable=False),
        sa.Column('viewer_id', sa.String(36), nullable=False),
        sa.Column('streams', sa.Integer, nullable=False, server_default='0'),
        sa.Column('streams_row', sa.Integer, nullable=False, server_default='0'),
        sa.Column('streams_row_peak', sa.Integer, nullable=False, server_default='0'),
        sa.Column('streams_row_peak_date', sa.Date, nullable=True),
        sa.Column('last_stream_id', sa.String(100), nullable=True),
        sa.Column('last_stream_at', sa.DateTime, nullable=True),
        sa.PrimaryKeyConstraint(
            'channel_id', 'provider', 'viewer_id', name='channel_viewer_stats_pkey'
        ),
    )
    op.execute(
        """
        INSERT INTO channel_viewer_stats (channel_id, provider, viewer_id, streams, 
            streams_row, streams_row_peak, streams_row_peak_date, 
                last_stream_id, last_stream_at)
        SELECT c.id, "twitch", user_id, streams, streams_row, streams_row_peak, 
            streams_row_peak_date, last_viewed_stream_id, last_viewed_stream_date
        FROM twitch_user_stats, channels c where 
            c.twitch_id = twitch_user_stats.channel_id
        """
    )
    op.drop_table('twitch_user_stats')

    op.create_table(
        'channel_stream_viewer_watchtime',
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(100), nullable=False),
        sa.Column('stream_id', sa.String(100), nullable=False),
        sa.Column('viewer_id', sa.String(36), nullable=False),
        sa.Column('watchtime', sa.Integer, nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint(
            'channel_id',
            'provider',
            'viewer_id',
            'stream_id',
            name='channel_stream_viewer_watchtime_pkey',
        ),
    )
    op.execute(
        """
        INSERT INTO channel_stream_viewer_watchtime (channel_id, provider, stream_id, 
            viewer_id, watchtime)
        SELECT c.id, "twitch", stream_id, user_id, time
        FROM twitch_stream_watchtime, channels c where c.twitch_id = 
            twitch_stream_watchtime.channel_id
        """
    )
    op.drop_table('twitch_stream_watchtime')

    op.create_table(
        'channel_streams',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('started_at', sa.DateTime, nullable=False),
    )
    op.execute(
        """
        INSERT INTO channel_streams (id, channel_id, started_at)
        SELECT UUID_v7(), c.id, started_at
        FROM twitch_streams, channels c where c.twitch_id = twitch_streams.channel_id
        """
    )

    op.create_table(
        'channel_provider_streams',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column(
            'channel_stream_id',
            sa.UUID(),
            sa.ForeignKey('channel_streams.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(100), nullable=False),
        sa.Column('provider_stream_id', sa.String(100), nullable=False),
        sa.Column('started_at', sa.DateTime, nullable=False),
        sa.Column('ended_at', sa.DateTime, nullable=True),
        sa.UniqueConstraint(
            'provider',
            'provider_stream_id',
            name='provider_streams_uq',
        ),
    )

    op.execute(
        """
        INSERT INTO channel_provider_streams (id, channel_stream_id, channel_id, 
            provider, provider_stream_id, started_at, ended_at)
        SELECT UUID_v7(), s.id, c.id, "twitch", stream_id, s.started_at, 
            s.started_at + INTERVAL uptime MINUTE
        FROM twitch_streams, channels c, channel_streams s where 
            c.twitch_id = twitch_streams.channel_id and 
            s.channel_id = c.id and s.started_at = twitch_streams.started_at
            and s.started_at = twitch_streams.started_at
        """
    )


def downgrade() -> None:
    pass
