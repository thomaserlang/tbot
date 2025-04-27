"""Channel provider broadcast info

Revision ID: 21320533cd02
Revises: ffddfb9d54f5
Create Date: 2025-04-19 13:04:46.207622

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '21320533cd02'
down_revision: str | None = 'ffddfb9d54f5'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.rename_table('channel_oauth_providers', 'channel_providers')

    op.create_table(
        'channel_provider_stream_activity',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column(
            'channel_provider_stream_id',
            sa.UUID(),
            sa.ForeignKey(
                'channel_provider_streams.id', ondelete='CASCADE', onupdate='CASCADE'
            ),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('action', sa.String(255), nullable=False),
        sa.Column('value', sa.String(255), nullable=False),
        sa.Index(
            'ix_channel_provider_stream_activity',
            'channel_provider_stream_id',
            'action',
            'created_at',
        )
    )


def downgrade() -> None:
    pass
