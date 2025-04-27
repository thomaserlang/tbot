"""User access invite

Revision ID: 9ec95dd569a5
Revises: 33ec9244df65
Create Date: 2025-04-25 17:33:22.121285

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9ec95dd569a5'
down_revision: str | None = '33ec9244df65'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_user_invites',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE'),
            nullable=False,
        ),
        sa.Column('access_level', sa.SmallInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    pass
