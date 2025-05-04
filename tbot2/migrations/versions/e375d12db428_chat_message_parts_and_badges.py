"""Chat message parts and badges

Revision ID: e375d12db428
Revises: 9ec95dd569a5
Create Date: 2025-05-04 11:29:54.705632

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e375d12db428'
down_revision: str | None = '9ec95dd569a5'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'chatlogs',
        sa.Column(
            'parts',
            sa.JSON,
            server_default='[]',
            nullable=False,
        ),
    )
    op.add_column(
        'chatlogs',
        sa.Column(
            'badges',
            sa.JSON,
            server_default='[]',
            nullable=False,
        ),
    )


def downgrade() -> None:
    pass
