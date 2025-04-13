import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MChannelProviderStreamViewerWatchtime(Base):
    __tablename__ = 'channel_provider_stream_viewer_watchtime'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_provider_stream_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey(
            'channel_provider_streams.id', onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True,
    )
    provider_viewer_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    watchtime: Mapped[int] = mapped_column(
        sa.Integer, server_default='0', nullable=False, comment='Seconds'
    )
