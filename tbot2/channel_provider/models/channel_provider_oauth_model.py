import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MChannelProviderOAuth(Base):
    __tablename__ = 'channel_providers_oauth'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_provider_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('channel_providers.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )
    access_token: Mapped[str | None] = mapped_column(sa.String(2000), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(sa.String(2000), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(UtcDateTime(), nullable=False)
