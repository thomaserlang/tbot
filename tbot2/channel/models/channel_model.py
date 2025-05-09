import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import SubscriptionType
from tbot2.model_base import Base


class MChannel(Base):
    __tablename__ = 'channels'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    display_name: Mapped[str] = mapped_column(sa.String(200))
    subscription: Mapped[SubscriptionType | None] = mapped_column(
        sa.String(100), nullable=True
    )
    created_at: Mapped[datetime]
