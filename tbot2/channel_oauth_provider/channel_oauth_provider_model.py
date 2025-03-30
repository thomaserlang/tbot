import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MChannelOAuthProvider(Base):
    __tablename__ = 'channel_oauth_providers'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID, sa.ForeignKey('channels.id', ondelete='CASCADE', onupdate='CASCADE')
    )
    provider: Mapped[str] = mapped_column(sa.String(255))
    provider_user_id: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    access_token: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(sa.DateTime(), nullable=True)
    scope: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    name: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
