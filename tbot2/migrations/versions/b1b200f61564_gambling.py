"""Gambling

Revision ID: b1b200f61564
Revises: a96a1d4bfa03
Create Date: 2024-12-14 18:56:38.860866

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mysql import INTEGER

# revision identifiers, used by Alembic.
revision: str = 'b1b200f61564'
down_revision: Union[str, None] = 'a96a1d4bfa03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('twitch_channel_point_settings', 'channel_point_settings')
    op.alter_column(
        'channel_point_settings',
        'channel_id',
        existing_type=sa.String(36),
        new_column_name='provider_id',
    )
    op.add_column(
        'channel_point_settings',
        sa.Column(
            'channel_id',
            sa.UUID,
            nullable=True,
        ),
    )
    op.execute(
        'UPDATE channel_point_settings SET channel_id = (SELECT id FROM channels WHERE twitch_id = channel_point_settings.provider_id)'
    )
    op.alter_column(
        'channel_point_settings',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.drop_constraint(
        'channel_point_settings_pkey', 'channel_point_settings', type_='primary'
    )
    op.create_primary_key(
        'channel_point_settings_pkey',
        'channel_point_settings',
        [
            'channel_id',
        ],
    )
    op.create_foreign_key(
        'channel_point_settings_ibfk_1',
        'channel_point_settings',
        'channels',
        ['channel_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE',
    )
    op.drop_column('channel_point_settings', 'provider_id')
    op.alter_column(
        'channel_point_settings',
        'enabled',
        existing_type=sa.Integer,
        type_=sa.Boolean,
        nullable=False,
        server_default='0',
    )

    op.rename_table(
        'twitch_gambling_roulette_settings', 'channel_gambling_roulette_settings'
    )
    op.alter_column(
        'channel_gambling_roulette_settings',
        'channel_id',
        existing_type=sa.String(36),
        new_column_name='provider_id',
    )
    op.add_column(
        'channel_gambling_roulette_settings',
        sa.Column(
            'channel_id',
            sa.UUID,
            nullable=True,
        ),
    )
    op.execute(
        'UPDATE channel_gambling_roulette_settings SET channel_id = (SELECT id FROM channels WHERE twitch_id = channel_gambling_roulette_settings.provider_id)'
    )
    op.alter_column(
        'channel_gambling_roulette_settings',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.drop_constraint(
        'channel_gambling_roulette_settings_pkey',
        'channel_gambling_roulette_settings',
        type_='primary',
    )
    op.create_primary_key(
        'channel_gambling_roulette_settings_pkey',
        'channel_gambling_roulette_settings',
        [
            'channel_id',
        ],
    )
    op.create_foreign_key(
        'channel_gambling_roulette_settings_ibfk_1',
        'channel_gambling_roulette_settings',
        'channels',
        ['channel_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE',
    )
    op.drop_column('channel_gambling_roulette_settings', 'provider_id')

    op.rename_table('twitch_gambling_slots_settings', 'channel_gambling_slots_settings')
    op.alter_column(
        'channel_gambling_slots_settings',
        'channel_id',
        existing_type=sa.String(36),
        new_column_name='provider_id',
    )
    op.add_column(
        'channel_gambling_slots_settings',
        sa.Column(
            'channel_id',
            sa.UUID,
            nullable=True,
        ),
    )
    op.execute(
        'UPDATE channel_gambling_slots_settings SET channel_id = (SELECT id FROM channels WHERE twitch_id = channel_gambling_slots_settings.provider_id)'
    )
    op.alter_column(
        'channel_gambling_slots_settings',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.drop_constraint(
        'channel_gambling_slots_settings_pkey',
        'channel_gambling_slots_settings',
        type_='primary',
    )
    op.create_primary_key(
        'channel_gambling_slots_settings_pkey',
        'channel_gambling_slots_settings',
        [
            'channel_id',
        ],
    )
    op.create_foreign_key(
        'channel_gambling_slots_settings_ibfk_1',
        'channel_gambling_slots_settings',
        'channels',
        ['channel_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE',
    )
    op.drop_column('channel_gambling_slots_settings', 'provider_id')

    op.rename_table('twitch_gambling_stats', 'channel_chatter_gambling_stats')
    op.alter_column(
        'channel_chatter_gambling_stats',
        'slots_loses',
        new_column_name='slots_losses',
        existing_type=INTEGER,
    )
    op.alter_column(
        'channel_chatter_gambling_stats',
        'roulette_loses',
        new_column_name='roulette_losses',
        existing_type=INTEGER,
    )
    op.alter_column(
        'channel_chatter_gambling_stats',
        'channel_id',
        existing_type=sa.String(36),
        new_column_name='provider_id',
    )
    op.add_column(
        'channel_chatter_gambling_stats',
        sa.Column(
            'channel_id',
            sa.UUID,
            nullable=True,
        ),
    )
    op.execute(
        'UPDATE channel_chatter_gambling_stats SET channel_id = (SELECT id FROM channels WHERE twitch_id = channel_chatter_gambling_stats.provider_id)'
    )
    op.alter_column(
        'channel_chatter_gambling_stats',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.add_column(
        'channel_chatter_gambling_stats', sa.Column('provider', sa.String(100))
    )
    op.execute('UPDATE channel_chatter_gambling_stats SET provider="twitch"')
    op.alter_column(
        'channel_chatter_gambling_stats',
        'provider',
        existing_type=sa.String(100),
        nullable=False,
    )
    op.alter_column(
        'channel_chatter_gambling_stats',
        'user_id',
        new_column_name='chatter_id',
        existing_type=sa.String(36),
    )
    op.drop_constraint(
        'channel_chatter_gambling_stats_pkey',
        'channel_chatter_gambling_stats',
        type_='primary',
    )
    op.create_primary_key(
        'channel_chatter_gambling_stats_pkey',
        'channel_chatter_gambling_stats',
        [
            'channel_id',
            'provider',
            'chatter_id',
        ],
    )
    op.create_foreign_key(
        'channel_chatter_gambling_stats_ibfk_1',
        'channel_chatter_gambling_stats',
        'channels',
        ['channel_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE',
    )
    op.drop_column('channel_chatter_gambling_stats', 'provider_id')

    op.rename_table('twitch_user_channel_points', 'channel_chatter_points')
    op.alter_column(
        'channel_chatter_points',
        'channel_id',
        existing_type=sa.String(36),
        new_column_name='provider_id',
    )
    op.add_column(
        'channel_chatter_points',
        sa.Column(
            'channel_id',
            sa.UUID,
            nullable=True,
        ),
    )
    op.execute(
        'UPDATE channel_chatter_points SET channel_id = (SELECT id FROM channels WHERE twitch_id = channel_chatter_points.provider_id)'
    )
    op.alter_column(
        'channel_chatter_points',
        'channel_id',
        nullable=False,
        existing_type=sa.UUID,
    )
    op.add_column('channel_chatter_points', sa.Column('provider', sa.String(100)))
    op.execute('UPDATE channel_chatter_points SET provider="twitch"')
    op.alter_column(
        'channel_chatter_points',
        'provider',
        existing_type=sa.String(100),
        nullable=False,
    )
    op.alter_column(
        'channel_chatter_points',
        'user_id',
        new_column_name='chatter_id',
        existing_type=sa.String(36),
    )
    op.drop_constraint(
        'channel_chatter_points_pkey', 'channel_chatter_points', type_='primary'
    )
    op.create_primary_key(
        'channel_chatter_points_pkey',
        'channel_chatter_points',
        ['channel_id', 'provider', 'chatter_id'],
    )
    op.create_foreign_key(
        'channel_chatter_points_ibfk_1',
        'channel_chatter_points',
        'channels',
        ['channel_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE',
    )
    op.alter_column(
        'channel_chatter_points',
        'points',
        existing_type=INTEGER(unsigned=False),
        nullable=False,
        server_default='0',
    )
    op.drop_column('channel_chatter_points', 'provider_id')
    op.drop_column('channel_chatter_points', 'user')


def downgrade() -> None:
    pass
