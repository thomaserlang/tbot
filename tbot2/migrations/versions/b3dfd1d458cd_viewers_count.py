"""viewers count

Revision ID: b3dfd1d458cd
Revises: ab788b06664f
Create Date: 2025-05-16 14:47:49.943038

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b3dfd1d458cd'
down_revision: str | None = 'ab788b06664f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'channel_providers',
        sa.Column(
            'stream_viewers_count',
            sa.Integer(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    pass
