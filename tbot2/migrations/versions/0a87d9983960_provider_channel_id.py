"""provider_channel_id

Revision ID: 0a87d9983960
Revises: e1dd62eb671e
Create Date: 2025-05-24 11:08:19.326408

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0a87d9983960'
down_revision: str | None = 'e1dd62eb671e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'bot_providers',
        'provider_user_id',
        existing_type=sa.String(255),
        nullable=False,
        new_column_name='provider_channel_id',
    )

    op.alter_column(
        'channel_activities',
        'provider_user_id',
        existing_type=sa.String(255),
        nullable=False,
        new_column_name='provider_channel_id',
    )

    op.alter_column(
        'channel_providers',
        'provider_user_id',
        existing_type=sa.String(255),
        nullable=True,
        new_column_name='provider_channel_id',
    )
    op.alter_column(
        'channel_providers',
        'provider_user_name',
        existing_type=sa.String(255),
        nullable=True,
        new_column_name='provider_channel_name',
    )
    op.alter_column(
        'channel_providers',
        'provider_user_display_name',
        existing_type=sa.String(255),
        nullable=True,
        new_column_name='provider_channel_display_name',
    )

    op.alter_column(
        'channel_provider_streams',
        'provider_user_id',
        existing_type=sa.String(255),
        nullable=False,
        new_column_name='provider_channel_id',
    )


def downgrade() -> None:
    pass
