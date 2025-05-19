import sys
from datetime import datetime
from typing import Any
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.model_base import Base


class MCommandTemplate(Base):
    __tablename__ = 'command_templates'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    commands: Mapped[list[dict[str, Any]]] = mapped_column(sa.JSON(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)
