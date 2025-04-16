import sys
from datetime import date
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tbot2.model_base import Base

from ...channel_stream.models.channel_provider_stream_model import (
    MChannelProviderStream,
)


class MChannelViewerStats(Base):
    __tablename__ = 'channel_provider_viewer_stats'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    channel_id: Mapped[UUID] = mapped_column(sa.UUID, nullable=False)
    provider: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    provider_viewer_id: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    streams: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default='0')
    streams_row: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    streams_row_peak: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    streams_row_peak_date: Mapped[date | None] = mapped_column(sa.Date, nullable=True)
    watchtime: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    last_channel_provider_stream_id: Mapped[str | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey(
            'channel_provider_streams.id', onupdate='CASCADE', ondelete='CASCADE'
        ),
        nullable=True,
    )
    last_channel_provider_stream: Mapped[MChannelProviderStream | None] = relationship(
        MChannelProviderStream,
        lazy='joined',
        innerjoin=False,
        viewonly=True,
    )
