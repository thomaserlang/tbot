import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.bot_providers import MBotProvider
from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MChannelProvider(Base):
    __tablename__ = 'channel_providers'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID, sa.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE')
    )
    provider: Mapped[str] = mapped_column(sa.String(255))
    provider_channel_id: Mapped[str | None] = mapped_column(
        sa.String(255), nullable=True
    )
    provider_channel_name: Mapped[str | None] = mapped_column(
        sa.String(255), nullable=True
    )
    provider_channel_display_name: Mapped[str | None] = mapped_column(
        sa.String(255), nullable=True
    )
    scope: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    bot_provider_id: Mapped[UUID | None] = mapped_column(
        sa.UUID,
        sa.ForeignKey('bot_providers.id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=True,
    )
    bot_provider: Mapped[MBotProvider] = sa.orm.relationship(
        'MBotProvider',
        lazy=False,
        viewonly=True,
    )
    stream_title: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    live_stream_id: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    stream_live: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False
    )
    stream_live_at: Mapped[datetime | None] = mapped_column(
        UtcDateTime(), nullable=True
    )
    stream_chat_id: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    stream_viewer_count: Mapped[int | None] = mapped_column(sa.Integer(), nullable=True)
    channel_provider_stream_id = mapped_column(
        sa.UUID,
        sa.ForeignKey(
            'channel_provider_streams.id',
            ondelete='SET NULL',
            onupdate='CASCADE',
        ),
        nullable=True,
    )
