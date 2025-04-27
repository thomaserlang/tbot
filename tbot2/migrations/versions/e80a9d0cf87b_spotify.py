"""Spotify

Revision ID: e80a9d0cf87b
Revises: b1b200f61564
Create Date: 2025-01-04 16:48:14.822396

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e80a9d0cf87b'
down_revision: str | None = 'b1b200f61564'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'spotify_oauth',
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='cascade', ondelete='cascade'),
            primary_key=True,
        ),
        sa.Column('access_token', sa.String(255), nullable=False),
        sa.Column('refresh_token', sa.String(255), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

    op.execute("""
        INSERT INTO spotify_oauth (channel_id, access_token, refresh_token, name)
        select c.id, s.token, s.refresh_token, s.user
        from twitch_spotify s, channels c 
        where s.channel_id = c.twitch_id
    """)


def downgrade() -> None:
    pass
