"""Channel provider name

Revision ID: a59a0ba7ad26
Revises: 21320533cd02
Create Date: 2025-04-19 18:48:02.604689

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a59a0ba7ad26'
down_revision: str | None = '21320533cd02'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'channel_providers',
        'name',
        existing_type=sa.String(255),
        nullable=True,
        new_column_name='provider_user_name',
    )
    op.add_column(
        'channel_providers',
        sa.Column('provider_user_display_name', sa.String(255), nullable=True),
    )
    op.execute(
        'UPDATE channel_providers SET provider_user_display_name = provider_user_name'
    )


def downgrade() -> None:
    pass
