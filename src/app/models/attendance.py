"""Modelo de Presença."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Attendance(Base):
    """Registro de presença de atleta em um treino."""
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    training_id: Mapped[int] = mapped_column(
        ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    athlete_id: Mapped[int] = mapped_column(
        ForeignKey("athletes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    present: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
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
    training: Mapped["Training"] = relationship("Training", back_populates="attendances")
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="attendances")

    # Constraints
    # RN-02: Um atleta tem no máximo um registro de presença por treino
    __table_args__ = (
        UniqueConstraint("training_id", "athlete_id", name="uq_attendance_training_athlete"),
        Index("ix_attendance_training_athlete", "training_id", "athlete_id"),
    )

    def __repr__(self) -> str:
        return f"<Attendance(training_id={self.training_id}, athlete_id={self.athlete_id}, present={self.present})>"