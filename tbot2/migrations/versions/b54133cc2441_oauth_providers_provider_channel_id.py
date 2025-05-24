"""oauth_providers provider_channel_id

Revision ID: b54133cc2441
Revises: 0a87d9983960
Create Date: 2025-05-24 16:12:35.136843

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b54133cc2441'
down_revision: str | None = '0a87d9983960'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'user_oauth_providers',
        'provider_user_id',
        existing_type=sa.String(255),
        nullable=False,
        new_column_name='provider_channel_id',
    )


def downgrade() -> None:
    pass
