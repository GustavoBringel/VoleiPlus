"""Serviço de treinos."""
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.training import Training
from app.models.team import Team
from app.schemas.training import TrainingCreate, TrainingUpdate


class TrainingService:
    """Serviço para operações de treinos."""

    def __init__(self, db: Session):
        self.db = db

    def _verify_team_ownership(self, team_id: int, coach_id: int) -> Optional[Team]:
        """Verifica se a equipe pertence ao treinador."""
        return (
            self.db.query(Team)
            .filter(Team.id == team_id, Team.coach_id == coach_id)
            .first()
        )

    def create_training(self, training_data: TrainingCreate, coach_id: int) -> Optional[Training]:
        """Registra novo treino para uma equipe do treinador."""
        team = self._verify_team_ownership(training_data.team_id, coach_id)
        if not team:
            return None

        training = Training(
            team_id=training_data.team_id,
            date=training_data.date,
            theme=training_data.theme,
            notes=training_data.notes,
        )
        self.db.add(training)
        self.db.commit()
        self.db.refresh(training)
        return training

    def get_training(self, training_id: int, coach_id: int) -> Optional[Training]:
        """Busca treino por ID (verificando equipe do treinador)."""
        return (
            self.db.query(Training)
            .join(Team, Training.team_id == Team.id)
            .filter(Training.id == training_id, Team.coach_id == coach_id)
            .first()
        )

    def get_trainings(
        self,
        coach_id: int,
        team_id: Optional[int] = None,
    ) -> List[Training]:
        """Lista treinos das equipes do treinador, em ordem cronológica."""
        query = (
            self.db.query(Training)
            .join(Team, Training.team_id == Team.id)
            .filter(Team.coach_id == coach_id)
        )

        if team_id:
            query = query.filter(Training.team_id == team_id)

        return query.order_by(Training.date.desc()).all()

    def update_training(
        self, training_id: int, coach_id: int, training_data: TrainingUpdate
    ) -> Optional[Training]:
        """Atualiza treino."""
        training = self.get_training(training_id, coach_id)
        if not training:
            return None

        update_data = training_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(training, field, value)

        self.db.commit()
        self.db.refresh(training)
        return training

    def delete_training(self, training_id: int, coach_id: int) -> bool:
        """Exclui treino."""
        training = self.get_training(training_id, coach_id)
        if not training:
            return False

        self.db.delete(training)
        self.db.commit()
        return True

    def get_training_with_attendance(self, training_id: int, coach_id: int) -> Optional[dict]:
        """Retorna treino com resumo de presença."""
        training = self.get_training(training_id, coach_id)
        if not training:
            return None

        from app.models.attendance import Attendance
        from app.models.athlete import Athlete

        total_athletes = (
            self.db.query(func.count(Athlete.id))
            .filter(Athlete.team_id == training.team_id, Athlete.is_active == True)
            .scalar()
        )
        attendances_count = (
            self.db.query(func.count(Attendance.id))
            .filter(Attendance.training_id == training_id)
            .scalar()
        )
        present_count = (
            self.db.query(func.count(Attendance.id))
            .filter(Attendance.training_id == training_id, Attendance.present == True)
            .scalar()
        )

        return {
            "training": training,
            "total_athletes": total_athletes,
            "attendances_count": attendances_count,
            "present_count": present_count,
        }