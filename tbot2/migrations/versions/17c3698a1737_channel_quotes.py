"""Channel quotes

Revision ID: 17c3698a1737
Revises: e80a9d0cf87b
Create Date: 2025-03-08 13:14:54.025629

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from uuid6 import uuid7

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
        sa.Column('provider', sa.String(36), nullable=False),
        sa.Column('created_by_chatter_id', sa.String(36), nullable=False),
        sa.Column('created_by_display_name', sa.String(200), nullable=False),
        sa.Column('message', sa.String(500), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    conn = op.get_bind()
    query = conn.execute(
        sa.text("""
            SELECT 
                c.id as channel_id, t.message, t.created_by_user_id,
                t.created_by_user, t.created_at, t.updated_at, t.number
            FROM 
                twitch_quotes t, 
                channels c
            WHERE 
                t.channel_id = c.twitch_id;
        """)
    )
    results = query.fetchall()
    for result in results:
        conn.execute(
            sa.text("""
                INSERT INTO channel_quotes (
                    id, channel_id, provider, created_by_chatter_id,
                    created_by_display_name, message, number, created_at, updated_at
                )
                VALUES (:id, :channel_id, :provider, :created_by_chatter_id,
                    :created_by_display_name, :message, :number, :created_at, 
                    :updated_at
                """),
            {
                'id': uuid7(),
                'channel_id': result[0],
                'provider': 'twitch',
                'created_by_chatter_id': result[2],
                'created_by_display_name': result[3],
                'message': result[1],
                'number': result[6],
                'created_at': result[4],
                'updated_at': result[5],
            },
        )


def downgrade() -> None:
    pass
