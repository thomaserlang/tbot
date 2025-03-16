"""Add channel user access level

Revision ID: 0264fe26cc59
Revises: fbdb194d24b3
Create Date: 2025-03-16 18:01:07.146292

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0264fe26cc59'
down_revision: Union[str, None] = 'fbdb194d24b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'channel_user_access_levels',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column(
            'user_id',
            sa.UUID(),
            sa.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('auth_level', sa.SmallInteger, nullable=False),
    )
    op.drop_table('twitch_channel_admins')

    op.execute("""
        INSERT INTO users (id, username, display_name, created_at, twitch_id)
        SELECT 
            uuid_v7(), 
            c.display_name, 
            c.display_name,
            c.created_at,
            c.twitch_id  
        FROM channels c
    """)

    op.execute("""
        INSERT INTO channel_user_access_levels (id, channel_id, user_id, auth_level)
        SELECT 
            uuid_v7(), 
            c.id as channel_id, 
            u.id as user_id,
            9 as auth_level
        FROM channels c, users u where u.twitch_id = c.twitch_id
    """)

    op.execute(""""
        INSERT INTO user_oauth_providers (id, user_id, provider, provider_user_id, created_at)
        SELECT 
            uuid_v7(), 
            u.id as user_id,
            'twitch' as provider,
            u.twitch_id as provider_user_id,
            u.created_at
        FROM users u
    """)


def downgrade() -> None:
    pass
