"""Refactor twitch_commands

Revision ID: fbdb194d24b3
Revises: 189219e5576e
Create Date: 2025-03-16 11:44:36.138169

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fbdb194d24b3'
down_revision: Union[str, None] = '189219e5576e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'commands',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('cmd', sa.String(100), nullable=False),
        sa.Column('response', sa.String(500), nullable=False),
        sa.Column('group_name', sa.String(100), nullable=False, server_default=''),
        sa.Column('global_cooldown', sa.Integer, nullable=False, server_default='0'),
        sa.Column('chatter_cooldown', sa.Integer, nullable=False, server_default='0'),
        sa.Column('mod_cooldown', sa.Integer, nullable=False, server_default='0'),
        sa.Column(
            'enabled_status', sa.SmallInteger, nullable=False, server_default='0'
        ),
        sa.Column('enabled', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('public', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('access_level', sa.SmallInteger, nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.execute("""
        INSERT INTO commands (id, channel_id, cmd, response, group_name, global_cooldown, chatter_cooldown, mod_cooldown, enabled_status, enabled, public, access_level, created_at, updated_at)
        SELECT 
            uuid_v7(), 
            c.id as channel_id, 
            t.cmd,
            t.response, 
            ifnull(t.group_name, ''),
            t.global_cooldown,
            t.user_cooldown as chatter_cooldown,
            t.mod_cooldown,
            t.enabled_status,
            t.enabled,
            t.public,
            t.user_level as access_level,
            t.created_at,
            t.updated_at
        FROM 
            twitch_commands t, 
            channels c
        WHERE 
            t.channel_id = c.twitch_id;
    """)

    op.create_table(
        'command_templates',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('commands', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    pass
