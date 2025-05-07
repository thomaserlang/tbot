import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import Provider
from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MQueueViewer(Base):
    __tablename__ = 'channel_queue_viewers'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID(), primary_key=True)
    channel_queue_id: Mapped[UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('channel_queues.id', onupdate='cascade', ondelete='cascade'),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    provider: Mapped[Provider] = mapped_column(sa.String(255), nullable=False)
    provider_viewer_id: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime, nullable=False)
