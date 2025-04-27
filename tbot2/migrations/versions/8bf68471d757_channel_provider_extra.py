"""Channel provider extra

Revision ID: 8bf68471d757
Revises: a59a0ba7ad26
Create Date: 2025-04-19 19:50:03.893751

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8bf68471d757'
down_revision: str | None = 'a59a0ba7ad26'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'channel_providers',
        sa.Column('stream_title', sa.String(255), nullable=True),
    )
    op.add_column(
        'channel_providers',
        sa.Column('stream_id', sa.String(255), nullable=True),
    )
    op.add_column(
        'channel_providers',
        sa.Column('stream_live', sa.Boolean(), nullable=False, server_default='0'),
    )
    op.add_column(
        'channel_providers',
        sa.Column('stream_live_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    pass
