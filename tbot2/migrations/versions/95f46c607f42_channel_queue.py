"""Channel queue

Revision ID: 95f46c607f42
Revises: e375d12db428
Create Date: 2025-04-28 21:27:56.912463

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '95f46c607f42'
down_revision: str | None = 'e375d12db428'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_queues',
        sa.Column(
            'id',
            sa.UUID(),
            primary_key=True,
        ),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='cascade', ondelete='cascade'),
            nullable=False,
        ),
        sa.Column(
            'name',
            sa.String(255),
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Index('ix_channel_queues_channel_id', 'channel_id', 'name', unique=True),
    )

    op.create_table(
        'channel_queue_viewers',
        sa.Column(
            'id',
            sa.UUID(),
        ),
        sa.Column(
            'channel_queue_id',
            sa.UUID(),
            sa.ForeignKey('channel_queues.id', onupdate='cascade', ondelete='cascade'),
            nullable=False,
        ),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('provider_viewer_id', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Index(
            'ix_channel_queue_id_position',
            'channel_queue_id',
            'position',
            unique=True,
        ),
        sa.Index(
            'ix_channel_queue_id_provider_viewer_id',
            'channel_queue_id',
            'provider',
            'provider_viewer_id',
            unique=True,
        ),
        if_not_exists=True,
    )


def downgrade() -> None:
    pass
