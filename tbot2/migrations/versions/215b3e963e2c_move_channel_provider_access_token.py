"""Move channel provider access token

Revision ID: 215b3e963e2c
Revises: 8bf68471d757
Create Date: 2025-04-20 21:09:54.695759

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '215b3e963e2c'
down_revision: str | None = '8bf68471d757'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_providers_oauth',
        sa.Column(
            'channel_provider_id',
            sa.UUID(),
            sa.ForeignKey(
                'channel_providers.id', onupdate='cascade', ondelete='cascade'
            ),
            primary_key=True,
        ),
        sa.Column('access_token', sa.String(2000), nullable=False),
        sa.Column('refresh_token', sa.String(2000), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
    )
    op.execute("""
        INSERT INTO channel_providers_oauth 
               (channel_provider_id, access_token, refresh_token, expires_at)
        SELECT channel_providers.id, access_token, refresh_token, 
               ifnull(expires_at, now())
        FROM channel_providers
        WHERE access_token IS NOT NULL
        AND refresh_token IS NOT NULL
    """)

    op.drop_column('channel_providers', 'access_token')
    op.drop_column('channel_providers', 'refresh_token')
    op.drop_column('channel_providers', 'expires_at')


def downgrade() -> None:
    pass
