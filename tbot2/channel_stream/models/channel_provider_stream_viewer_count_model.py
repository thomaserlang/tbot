import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MChannelProviderStreamViewerCount(Base):
    __tablename__ = 'channel_provider_stream_viewer_count'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_provider_stream_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        primary_key=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        UtcDateTime(), primary_key=True, nullable=False
    )
    viewer_count: Mapped[int] = mapped_column(sa.Integer(), nullable=False)
