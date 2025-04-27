"""Add channel user access level

Revision ID: 0264fe26cc59
Revises: fbdb194d24b3
Create Date: 2025-03-16 18:01:07.146292

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0264fe26cc59'
down_revision: str | None = 'fbdb194d24b3'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


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
        sa.Column('access_level', sa.SmallInteger, nullable=False),
        sa.UniqueConstraint(
            'channel_id',
            'user_id',
            name='uq_channel_user_access_levels',
        ),
    )

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
        INSERT INTO channel_user_access_levels (id, channel_id, user_id, access_level)
        SELECT 
            uuid_v7(), 
            c.id as channel_id, 
            u.id as user_id,
            9 as access_level
        FROM channels c, users u where u.twitch_id = c.twitch_id
    """)

    op.execute("""
        INSERT IGNORE INTO channel_user_access_levels 
        (id, channel_id, user_id, access_level)
        select
        uuid_v7 (),
        c.id as channel_id,
        u.id as user_id,
        a.level
        from
        twitch_channel_admins a,
        channels c,
        users u
        where
        c.twitch_id = a.channel_id
        and u.twitch_id = a.user_id;
    """)
    op.execute(
        'update channel_user_access_levels set access_level = 8 where access_level = 3'
    )
    op.execute(
        'update channel_user_access_levels set access_level = 7 where access_level = 1'
    )

    op.execute("""
        INSERT INTO user_oauth_providers (id, user_id, provider, 
               provider_user_id, created_at)
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
