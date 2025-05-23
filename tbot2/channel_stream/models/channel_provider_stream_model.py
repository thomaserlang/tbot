import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import Provider
from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MChannelProviderStream(Base):
    __tablename__ = 'channel_provider_streams'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    channel_id: Mapped[UUID] = mapped_column(sa.UUID)
    channel_stream_id: Mapped[UUID] = mapped_column(
        sa.UUID, sa.ForeignKey('channel_streams.id', ondelete='CASCADE'), nullable=False
    )
    provider: Mapped[Provider] = mapped_column(sa.String(255))
    provider_channel_id: Mapped[str] = mapped_column(sa.String(255))
    provider_stream_id: Mapped[str] = mapped_column(sa.String(255))
    started_at: Mapped[datetime] = mapped_column(UtcDateTime())
    ended_at: Mapped[datetime | None] = mapped_column(UtcDateTime(), nullable=True)
    avg_viewer_count: Mapped[int | None] = mapped_column(sa.Integer(), nullable=True)
    peak_viewer_count: Mapped[int | None] = mapped_column(sa.Integer(), nullable=True)