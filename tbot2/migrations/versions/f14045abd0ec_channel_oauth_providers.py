"""Channel oauth providers

Revision ID: f14045abd0ec
Revises: cb636132c3bb
Create Date: 2025-03-30 12:15:41.959220

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f14045abd0ec'
down_revision: str | None = 'cb636132c3bb'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'channel_oauth_providers',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column(
            'channel_id',
            sa.UUID(),
            sa.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE'),
            nullable=False,
        ),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('provider_user_id', sa.String(255), nullable=True),
        sa.Column('access_token', sa.String(2000), nullable=True),
        sa.Column('refresh_token', sa.String(2000), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('scope', sa.String(2000), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Index(
            'ix_channel_oauth_providers_channel_id_provider', 'channel_id', 'provider'
        ),
    )

    op.execute("""
        insert into channel_oauth_providers
            (id, channel_id, provider, provider_user_id, access_token, refresh_token, name, scope)
        select uuid_v7(), c.id, 'twitch', t.channel_id, t.twitch_token, t.twitch_refresh_token, t.name, t.twitch_scope
        from twitch_channels t, channels c 
        where c.twitch_id = t.channel_id
    """)
    op.execute("""
        insert into channel_oauth_providers
            (id, channel_id, provider, access_token, refresh_token, name)
        select uuid_v7(), c.id, 'youtube', y.token, y.refresh_token, y.handle
        from twitch_youtube y, channels c where c.twitch_id=y.channel_id
    """)
    op.execute("""
        insert into channel_oauth_providers
            (id, channel_id, provider, provider_user_id, name)
        select uuid_v7(), c.id, 'discord', t.discord_server_id, t.discord_server_name
        from twitch_channels t, channels c
        where c.twitch_id = t.channel_id and not isnull(t.discord_server_id)
    """)
    op.execute("""
        insert into channel_oauth_providers
            (id, channel_id, provider, name, access_token, refresh_token)
        select uuid_v7(), s.channel_id, 'spotify', s.name, s.access_token, s.refresh_token
        from spotify_oauth s
    """)


def downgrade() -> None:
    pass
