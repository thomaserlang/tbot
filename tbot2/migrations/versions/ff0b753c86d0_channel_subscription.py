"""Channel subscription

Revision ID: ff0b753c86d0
Revises: 95f46c607f42
Create Date: 2025-05-09 21:35:41.803979

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ff0b753c86d0'
down_revision: str | None = '95f46c607f42'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('channels', sa.Column('subscription', sa.String(100), nullable=True))
    op.drop_column('channels', 'bot_active')
    op.drop_column('channels', 'bot_muted')
    op.drop_column('channels', 'bot_chatlog_enabled')


def downgrade() -> None:
    pass
