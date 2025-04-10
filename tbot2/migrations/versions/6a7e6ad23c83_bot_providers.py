"""Bot providers

Revision ID: 6a7e6ad23c83
Revises: ed3a31bb7fb6
Create Date: 2025-04-09 20:55:13.089687

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6a7e6ad23c83'
down_revision: str | None = 'ed3a31bb7fb6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'bot_providers',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('provider_user_id', sa.String(255), nullable=False),
        sa.Column('system_default', sa.Boolean(), nullable=True),
        sa.Column('access_token', sa.String(2000), nullable=True),
        sa.Column('refresh_token', sa.String(2000), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('scope', sa.String(2000), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.UniqueConstraint(
            'provider', 'provider_user_id', name='uq_bot_providers_provider_user_id'
        ),
        sa.UniqueConstraint(
            'provider', 'system_default', name='uq_bot_providers_system_default'
        ),
    )

    op.add_column(
        'channel_oauth_providers',
        sa.Column(
            'bot_provider_id',
            sa.UUID(),
            sa.ForeignKey('bot_providers.id', ondelete='SET NULL', onupdate='CASCADE'),
            nullable=True,
        ),
    )


def downgrade() -> None:
    pass
