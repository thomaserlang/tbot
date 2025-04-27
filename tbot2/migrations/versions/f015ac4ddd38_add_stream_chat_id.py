"""Add stream_chat_id

Revision ID: f015ac4ddd38
Revises: 215b3e963e2c
Create Date: 2025-04-21 10:30:43.505377

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f015ac4ddd38'
down_revision: str | None = '215b3e963e2c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'channel_providers',
        sa.Column(
            'stream_chat_id',
            sa.String(length=255),
            nullable=True,
        ),
    )


def downgrade() -> None:
    pass
