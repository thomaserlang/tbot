import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.common import TProvider
from tbot2.model_base import Base


class MBotProvider(Base):
    __tablename__ = 'bot_providers'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    provider: Mapped[TProvider] = mapped_column(sa.String(255), nullable=False)
    system_default: Mapped[bool | None] = mapped_column(sa.Boolean(), nullable=True)
    provider_user_id: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    access_token: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(sa.DateTime(), nullable=True)
    scope: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    name: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
