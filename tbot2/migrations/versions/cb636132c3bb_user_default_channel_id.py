"""User default_channel_id

Revision ID: cb636132c3bb
Revises: 58408699aa1e
Create Date: 2025-03-29 18:13:43.480607

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cb636132c3bb'
down_revision: Union[str, None] = '58408699aa1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'default_channel_id',
            sa.UUID,
            sa.ForeignKey('channels.id', ondelete='set null', onupdate='cascade'),
            nullable=True,
        ),
    )
    op.execute(
        'UPDATE users SET default_channel_id = (SELECT channel_id FROM channel_user_access_levels WHERE user_id = users.id and access_level=9)'
    )


def downgrade() -> None:
    pass
