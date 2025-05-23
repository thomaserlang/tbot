"""user settings

Revision ID: 0924203739df
Revises: 7e66c977cfbf
Create Date: 2025-05-23 13:27:26.894527

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0924203739df'
down_revision: str | None = '7e66c977cfbf'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'user_settings',
        sa.Column(
            'user_id',
            sa.UUID(),
            sa.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
            primary_key=True,
        ),
        sa.Column('settings', sa.JSON(), nullable=False, default={}),
    )
    op.execute(
        "insert into user_settings (user_id, settings) select id, '{}' from users"
    )


def downgrade() -> None:
    pass
