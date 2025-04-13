import sys
from datetime import date
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MChannelViewerStats(Base):
    __tablename__ = 'channel_provider_viewer_stats'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    provider: Mapped[str] = mapped_column(sa.String(100), primary_key=True)
    provider_viewer_id: Mapped[str] = mapped_column(sa.String(100), primary_key=True)

    streams: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default='0')
    streams_row: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    streams_row_peak: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    streams_row_peak_date: Mapped[date | None] = mapped_column(sa.Date, nullable=True)
    last_channel_provider_stream_id: Mapped[str | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey(
            'channel_provider_streams.id', onupdate='CASCADE', ondelete='CASCADE'
        ),
        nullable=True,
    )
