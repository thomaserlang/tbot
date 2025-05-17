import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MChannelStream(Base):
    __tablename__ = 'channel_streams'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    channel_id: Mapped[UUID] = mapped_column(sa.UUID)
    started_at: Mapped[datetime] = mapped_column(UtcDateTime())
    avg_viewer_count: Mapped[int | None] = mapped_column(sa.Integer(), nullable=True)
    peak_viewer_count: Mapped[int | None] = mapped_column(sa.Integer(), nullable=True)
