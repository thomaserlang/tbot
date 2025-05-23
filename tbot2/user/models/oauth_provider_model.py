import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MUserOAuthProvider(Base):
    __tablename__ = 'user_oauth_providers'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(
        sa.UUID, sa.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE')
    )
    provider: Mapped[str] = mapped_column(sa.String(255))  # 'google', 'github', etc
    provider_channel_id: Mapped[str] = mapped_column(sa.String(255))
    created_at: Mapped[datetime] = mapped_column(UtcDateTime())
    updated_at: Mapped[datetime | None] = mapped_column(UtcDateTime(), nullable=True)
