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
        'channel_streams',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('started_at', sa.DateTime, nullable=False),
        sa.Index(
            'ix_channel_streams_channel_id_started_at',
            'channel_id',
            'started_at',
        ),
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
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('provider_id', sa.String(255), nullable=False),
        sa.Column('provider_stream_id', sa.String(255), nullable=False),
        sa.Column('started_at', sa.DateTime, nullable=False),
        sa.Column('ended_at', sa.DateTime, nullable=True),
        sa.UniqueConstraint(
            'provider',
            'provider_stream_id',
            name='provider_streams_uq',
        ),
        sa.Index(
            'ix_channel_id_provider_ended_at', 'channel_id', 'provider', 'ended_at'
        ),
        sa.Index('ix_ended_at', 'ended_at'),
    )

    op.execute(
        """
        INSERT INTO channel_provider_streams (id, channel_stream_id, channel_id, 
            provider, provider_id, provider_stream_id, started_at, ended_at)
        SELECT UUID_v7(), s.id, c.id, "twitch", twitch_streams.channel_id, stream_id, 
            s.started_at, s.started_at + INTERVAL uptime SECOND
        FROM twitch_streams, channels c, channel_streams s where 
            c.twitch_id = twitch_streams.channel_id and 
            s.channel_id = c.id and s.started_at = twitch_streams.started_at
            and s.started_at = twitch_streams.started_at
        """
    )

    op.create_table(
        'channel_provider_stream_viewer_watchtime',
        sa.Column(
            'channel_provider_stream_id',
            sa.UUID(),
            sa.ForeignKey(
                'channel_provider_streams.id',
                onupdate='CASCADE',
                ondelete='CASCADE',
            ),
            primary_key=True,
        ),
        sa.Column(
            'provider_viewer_id', sa.String(255), nullable=False, primary_key=True
        ),
        sa.Column(
            'watchtime',
            sa.Integer,
            nullable=False,
            server_default='0',
            comment='Seconds',
        ),
    )
    op.execute(
        """
        INSERT INTO channel_provider_stream_viewer_watchtime 
            (channel_provider_stream_id, provider_viewer_id, watchtime)
        SELECT p.provider_stream_id, user_id, time
        FROM twitch_stream_watchtime, channels c, channel_provider_streams p 
        where 
            c.twitch_id = twitch_stream_watchtime.channel_id and 
            twitch_stream_watchtime.stream_id = p.provider_stream_id;
        """
    )

    op.create_table(
        'channel_provider_viewer_stats',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('provider_viewer_id', sa.String(255), nullable=False),
        sa.Column('streams', sa.Integer, nullable=False, server_default='0'),
        sa.Column('streams_row', sa.Integer, nullable=False, server_default='0'),
        sa.Column('streams_row_peak', sa.Integer, nullable=False, server_default='0'),
        sa.Column('streams_row_peak_date', sa.Date, nullable=True),
        sa.Column('watchtime', sa.Integer, nullable=False, server_default='0'),
        sa.Column(
            'last_channel_provider_stream_id',
            sa.UUID(),
            sa.ForeignKey(
                'channel_provider_streams.id', onupdate='CASCADE', ondelete='CASCADE'
            ),
            nullable=True,
        ),
        sa.UniqueConstraint(
            'channel_id',
            'provider',
            'provider_viewer_id',
            name='channel_provider_viewer_stats_pkey',
        ),
    )
    op.execute(
        """
        INSERT INTO channel_provider_viewer_stats (
            id,
            channel_id, provider, provider_viewer_id, streams, 
            streams_row, streams_row_peak, streams_row_peak_date, 
                last_channel_provider_stream_id)
        SELECT uuid_v7(), c.id, "twitch", user_id, streams, streams_row, 
            streams_row_peak, 
            streams_row_peak_date, p.id
        FROM twitch_user_stats, channels c, channel_provider_streams p where 
            c.twitch_id = twitch_user_stats.channel_id and 
            twitch_user_stats.last_viewed_stream_id = p.provider_stream_id
        """
    )

    op.execute("""
        update channel_provider_viewer_stats s
            set watchtime = (select sum(watchtime) 
                from channel_provider_stream_viewer_watchtime w 
                where 
                    w.provider_viewer_id = s.provider_viewer_id)
    """)


def downgrade() -> None:
    pass
