"""Chatlog id uuid

Revision ID: ffddfb9d54f5
Revises: 6a7e6ad23c83
Create Date: 2025-04-14 09:15:03.765203

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mysql import DATETIME

# revision identifiers, used by Alembic.
revision: str = 'ffddfb9d54f5'
down_revision: str | None = '6a7e6ad23c83'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'chatlogs_v2',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('type', sa.String(100), nullable=False),
        sa.Column('sub_type', sa.String(100), nullable=True),
        sa.Column('created_at', DATETIME(fsp=6), nullable=False),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE'),
            nullable=False,
        ),
        sa.Column('chatter_id', sa.String(36), nullable=False),
        sa.Column('chatter_name', sa.String(200), nullable=False),
        sa.Column('chatter_display_name', sa.String(200), nullable=False),
        sa.Column('chatter_color', sa.String(7), nullable=True),
        sa.Column('message', sa.String(600), nullable=False),
        sa.Column('msg_id', sa.String(36), nullable=True),
        sa.Column('provider', sa.String(100), nullable=False),
        sa.Column('provider_id', sa.String(36), nullable=False),
        sa.Column('twitch_fragments', sa.JSON, nullable=True),
        sa.Column('twitch_badges', sa.JSON, nullable=True),
        sa.Index('ix_chatlogs_1', 'channel_id', 'created_at', 'chatter_id'),
        sa.UniqueConstraint('msg_id', name='uq_chatlogs_msg_id'),
    )
    op.execute("""
        INSERT INTO chatlogs_v2 
               (id, type, sub_type, created_at, channel_id, chatter_id, chatter_name, 
               chatter_display_name, chatter_color, message, msg_id, provider, 
               provider_id, twitch_fragments, twitch_badges)
        SELECT uuid_v7(), type, sub_type, created_at, channel_id, chatter_id, 
               chatter_name, chatter_display_name, chatter_color, message, msg_id, 
               provider, provider_id, twitch_fragments, twitch_badges
        FROM chatlogs
    """)
    op.drop_table('chatlogs')
    op.rename_table('chatlogs_v2', 'chatlogs')


def downgrade() -> None:
    pass
