"""Channel Activities

Revision ID: 7e66c977cfbf
Revises: 6ad5d53cb956
Create Date: 2025-05-20 21:05:02.885296

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7e66c977cfbf'
down_revision: str | None = '6ad5d53cb956'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_activities',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('sub_type', sa.String(255), nullable=False),
        sa.Column('channel_id', sa.UUID(), nullable=False),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('provider_message_id', sa.String(255), nullable=False, unique=True),
        sa.Column('provider_user_id', sa.String(255), nullable=False),
        sa.Column('provider_viewer_id', sa.String(255), nullable=False),
        sa.Column('viewer_name', sa.String(255), nullable=False),
        sa.Column('viewer_display_name', sa.String(255), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.Column('count_decimal_place', sa.Integer(), nullable=False),
        sa.Column('count_currency', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('gifted_viewers', sa.JSON(), nullable=True),
        sa.Column('system_message', sa.String(1000), nullable=True),
        sa.Column('message', sa.String(2000), nullable=True),
        sa.Column('message_parts', sa.JSON(), nullable=True),
        sa.Column('read', sa.Boolean(), default=False, nullable=False),
        sa.Index(
            'ix_channel_activities_channel_id_type', 'channel_id', 'type', 'created_at'
        ),
    )


def downgrade() -> None:
    pass
