"""Chat message notice

Revision ID: ab788b06664f
Revises: ff0b753c86d0
Create Date: 2025-05-14 15:33:24.473910

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ab788b06664f'
down_revision: str | None = 'ff0b753c86d0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'chatlogs',
        sa.Column('notice_message', sa.String(2000), nullable=False, server_default=''),
    )
    op.add_column(
        'chatlogs',
        sa.Column('notice_parts', sa.JSON(), nullable=False, server_default='[]'),
    )
    op.execute("""
        update 
            chatlogs 
        set 
            type = "status", notice_message=message, message="", 
               notice_parts=parts, parts="[]" 
        where type = "mod_action"
    """)


def downgrade() -> None:
    pass
