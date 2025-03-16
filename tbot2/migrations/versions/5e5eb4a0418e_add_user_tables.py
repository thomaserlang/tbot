"""add_user_tables

Revision ID: 5e5eb4a0418e
Revises: 17c3698a1737
Create Date: 2025-03-09 22:03:58.193267

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5e5eb4a0418e'
down_revision: Union[str, None] = '17c3698a1737'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=True, unique=True),
        sa.Column('display_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('twitch_id', sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    # Drop users table
    op.drop_table('users')
