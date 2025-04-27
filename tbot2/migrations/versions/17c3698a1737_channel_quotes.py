"""Channel quotes

Revision ID: 17c3698a1737
Revises: e80a9d0cf87b
Create Date: 2025-03-08 13:14:54.025629

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '17c3698a1737'
down_revision: str | None = 'e80a9d0cf87b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_quotes',
        sa.Column('id', sa.UUID(), nullable=False, primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('created_by_provider_viewer_id', sa.String(255), nullable=False),
        sa.Column('created_by_display_name', sa.String(200), nullable=False),
        sa.Column('message', sa.String(600), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.execute(
        """
            INSERT INTO channel_quotes (
                id, channel_id, provider, created_by_provider_viewer_id,
                created_by_display_name, message, number, created_at, updated_at
            ) 
            SELECT 
                uuid_v7(), c.id as channel_id, 'twitch', t.created_by_user_id,
                t.created_by_user, t.message, t.number, t.created_at, t.updated_at
            FROM 
                twitch_quotes t, 
                channels c
            WHERE 
                t.channel_id = c.twitch_id;
        """
    )


def downgrade() -> None:
    pass
