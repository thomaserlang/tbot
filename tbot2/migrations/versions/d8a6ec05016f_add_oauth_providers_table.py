"""add_user_oauth_providers_table

Revision ID: d8a6ec05016f
Revises: 5e5eb4a0418e
Create Date: 2025-03-14 18:28:34.742076

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd8a6ec05016f'
down_revision: Union[str, None] = '5e5eb4a0418e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_oauth_providers',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('provider', sa.String(100), nullable=False),
        sa.Column('provider_user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_user_oauth_providers_provider_provider_user_id'),
        'user_oauth_providers',
        ['provider', 'provider_user_id'],
        unique=True,
    )
    op.create_index(
        op.f('ix_user_oauth_providers_user_id'),
        'user_oauth_providers',
        ['user_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_user_oauth_providers_user_id'), table_name='user_oauth_providers'
    )
    op.drop_index(
        op.f('ix_user_oauth_providers_provider_provider_user_id'),
        table_name='user_oauth_providers',
    )
    op.drop_table('user_oauth_providers')
