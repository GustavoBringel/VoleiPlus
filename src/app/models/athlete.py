"""Modelo de Atleta."""
from datetime import datetime, date, timezone
from typing import List, Optional

from sqlalchemy import DateTime, Date, ForeignKey, String, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Athlete(Base):
    """Modelo de atleta vinculado a uma equipe."""
    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    position: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # levantador, ponteiro, etc.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
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
    team: Mapped["Team"] = relationship("Team", back_populates="athletes")
    attendances: Mapped[List["Attendance"]] = relationship(
        "Attendance", back_populates="athlete", cascade="all, delete-orphan"
    )
    evaluations: Mapped[List["Evaluation"]] = relationship(
        "Evaluation", back_populates="athlete", cascade="all, delete-orphan"
    )

    # Constraint: um atleta pertence a uma equipe por vez (RN-01)
    # Garantido pelo team_id único por atleta (um atleta = uma linha = uma equipe)

    def __repr__(self) -> str:
        return f"<Athlete(id={self.id}, name={self.name}, team_id={self.team_id})>"