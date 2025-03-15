from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.database import Base


class MChannelStreamViewerWatchtime(Base):
    __tablename__ = "channel_stream_viewer_watchtime"

    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey("channels.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    provider: Mapped[str] = mapped_column(
        sa.String(100), primary_key=True
    )
    stream_id: Mapped[str] = mapped_column(
        sa.String(100), primary_key=True
    )
    viewer_id: Mapped[str] = mapped_column(
        sa.String(36), primary_key=True
    )
    watchtime: Mapped[int] = mapped_column(
        sa.Integer, server_default="0", nullable=False
    )
