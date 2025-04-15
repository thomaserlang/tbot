"""Chatlog changes

Revision ID: cdb4011c1026
Revises: dba3882e4560
Create Date: 2024-11-08 10:41:45.753279

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mysql import DATETIME

# revision identifiers, used by Alembic.
revision: str = 'cdb4011c1026'
down_revision: str | None = 'dba3882e4560'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.rename_table('twitch_chatlog', 'chatlogs')
    op.add_column('chatlogs', sa.Column('provider', sa.String(255)))
    op.execute('UPDATE chatlogs SET provider = "twitch"')

    op.rename_table('twitch_user_chat_stats', 'chatlog_chatter_stats')
    op.rename_table('twitch_usernames', 'chatlog_chatters')

    op.add_column('chatlog_chatters', sa.Column('provider', sa.String(255)))
    op.execute('UPDATE chatlog_chatters SET provider="twitch"')
    op.alter_column(
        'chatlog_chatters',
        'expires',
        new_column_name='last_seen_at',
        existing_type=sa.DateTime,
    )
    op.execute(
        'update chatlog_chatters set last_seen_at = last_seen_at - INTERVAL 30 DAY'
    )

    op.add_column('chatlogs', sa.Column('user_display_name', sa.String(255)))
    op.execute('UPDATE chatlogs SET user_display_name = user')
    op.add_column('chatlogs', sa.Column('user_color', sa.String(7), nullable=True))
    op.add_column('chatlogs', sa.Column('twitch_fragments', sa.JSON, nullable=True))
    op.add_column('chatlogs', sa.Column('twitch_badges', sa.JSON, nullable=True))

    op.alter_column(
        'chatlogs', 'created_at', existing_type=sa.DateTime, type_=DATETIME(fsp=6)
    )

    op.execute('update chatlogs set msg_id=uuid() where isnull(msg_id)')
    op.alter_column('chatlogs', 'msg_id', nullable=False, existing_type=sa.String(255))

    op.alter_column(
        'chatlogs',
        'type',
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.execute('update chatlogs set type="message" where type="1"')
    op.execute('update chatlogs set type="notice" where type="2"')
    op.execute('update chatlogs set type="mod_action" where type="100"')

    op.add_column('chatlogs', sa.Column('sub_type', sa.String(255), nullable=True))


def downgrade() -> None:
    pass
