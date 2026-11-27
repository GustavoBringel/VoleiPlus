"""Modelo de Avaliação de Fundamentos."""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Evaluation(Base):
    """Avaliação de fundamentos de um atleta."""
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    athlete_id: Mapped[int] = mapped_column(
        ForeignKey("athletes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    evaluator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    # Fundamentos - escala 1 a 5 (RN-03)
    pass_rating: Mapped[int] = mapped_column(Integer, nullable=False)      # passe
    serve_rating: Mapped[int] = mapped_column(Integer, nullable=False)     # saque
    attack_rating: Mapped[int] = mapped_column(Integer, nullable=False)    # ataque
    block_rating: Mapped[int] = mapped_column(Integer, nullable=False)     # bloqueio
    defense_rating: Mapped[int] = mapped_column(Integer, nullable=False)   # defesa
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
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="evaluations")
    evaluator: Mapped["User"] = relationship("User", back_populates="evaluations")

    # Constraints: notas entre 1 e 5 (RN-03)
    __table_args__ = (
        CheckConstraint("pass_rating BETWEEN 1 AND 5", name="ck_pass_rating_range"),
        CheckConstraint("serve_rating BETWEEN 1 AND 5", name="ck_serve_rating_range"),
        CheckConstraint("attack_rating BETWEEN 1 AND 5", name="ck_attack_rating_range"),
        CheckConstraint("block_rating BETWEEN 1 AND 5", name="ck_block_rating_range"),
        CheckConstraint("defense_rating BETWEEN 1 AND 5", name="ck_defense_rating_range"),
    )

    def __repr__(self) -> str:
        return f"<Evaluation(id={self.id}, athlete_id={self.athlete_id}, date={self.date})>"