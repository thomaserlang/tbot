"""Channel provider stream viewer count

Revision ID: 6ad5d53cb956
Revises: b3dfd1d458cd
Create Date: 2025-05-16 15:03:25.632399

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6ad5d53cb956'
down_revision: str | None = 'b3dfd1d458cd'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_provider_stream_viewer_count',
        sa.Column(
            'channel_provider_stream_id',
            sa.UUID(),
            primary_key=True,
        ),
        sa.Column('timestamp', sa.DateTime(), nullable=False, primary_key=True),
        sa.Column('viewer_count', sa.Integer(), nullable=False),
    )
    op.alter_column(
        'channel_providers',
        'stream_viewers_count',
        existing_type=sa.Integer(),
        nullable=True,
        new_column_name='stream_viewer_count',
    )

    op.add_column(
        'channel_provider_streams',
        sa.Column(
            'avg_viewer_count',
            sa.Integer(),
            nullable=True,
        ),
    )
    op.add_column(
        'channel_provider_streams',
        sa.Column(
            'peak_viewer_count',
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        'channel_streams',
        sa.Column(
            'avg_viewer_count',
            sa.Integer(),
            nullable=True,
        ),
    )
    op.add_column(
        'channel_streams',
        sa.Column(
            'peak_viewer_count',
            sa.Integer(),
            nullable=True,
        ),
    )

    op.alter_column(
        'channel_provider_streams',
        'provider_id',
        existing_type=sa.String(255),
        nullable=True,
        new_column_name='provider_user_id',
    )
    op.add_column(
        'channel_providers',
        sa.Column(
            'channel_provider_stream_id',
            sa.UUID(),
            sa.ForeignKey(
                'channel_provider_streams.id',
                ondelete='SET NULL',
                onupdate='CASCADE',
            ),
        ),
    )
    op.alter_column(
        'channel_providers',
        'stream_id',
        existing_type=sa.String(255),
        nullable=True,
        new_column_name='live_stream_id',
    )


def downgrade() -> None:
    pass
