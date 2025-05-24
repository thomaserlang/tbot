"""Chatlog refactor

Revision ID: e1dd62eb671e
Revises: 0924203739df
Create Date: 2025-05-24 09:55:17.791200

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e1dd62eb671e'
down_revision: str | None = '0924203739df'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.rename_table('chatlogs', 'channel_chat_messages')
    op.drop_table('chatlog_chatter_stats', if_exists=True)

    op.alter_column(
        'channel_chat_messages',
        'msg_id',
        existing_type=sa.String(255),
        new_column_name='provider_message_id',
    )
    op.drop_column('channel_chat_messages', 'twitch_fragments')
    op.drop_column('channel_chat_messages', 'twitch_badges')
    op.alter_column(
        'channel_chat_messages',
        'provider_id',
        new_column_name='provider_channel_id',
        existing_type=sa.String(255),
    )
    op.alter_column(
        'channel_chat_messages',
        'parts',
        existing_type=sa.JSON,
        nullable=False,
        new_column_name='message_parts',
    )
    op.alter_column(
        'channel_chat_messages',
        'notice_parts',
        existing_type=sa.JSON,
        nullable=True,
        new_column_name='notice_message_parts',
    )


def downgrade() -> None:
    pass
