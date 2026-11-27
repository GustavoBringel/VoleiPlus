"""Modelo de Treino."""
from datetime import datetime, date, timezone
from typing import List, Optional

from sqlalchemy import DateTime, Date, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Training(Base):
    """Modelo de treino registrado para uma equipe."""
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    theme: Mapped[str] = mapped_column(String(200), nullable=False)  # tema/foco do treino
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamentos
    team: Mapped["Team"] = relationship("Team", back_populates="trainings")
    attendances: Mapped[List["Attendance"]] = relationship(
        "Attendance", back_populates="training", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Training(id={self.id}, team_id={self.team_id}, date={self.date})>"