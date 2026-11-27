"""Serviço de avaliações."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.evaluation import Evaluation
from app.models.athlete import Athlete
from app.models.team import Team
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate, EvaluationSummary, AthleteEvolution


class EvaluationService:
    """Serviço para operações de avaliações."""

    def __init__(self, db: Session):
        self.db = db

    def _verify_athlete_ownership(self, athlete_id: int, coach_id: int) -> Optional[Athlete]:
        """Verifica se o atleta pertence a uma equipe do treinador."""
        return (
            self.db.query(Athlete)
            .join(Team, Athlete.team_id == Team.id)
            .filter(Athlete.id == athlete_id, Team.coach_id == coach_id)
            .first()
        )

    def create_evaluation(self, evaluation_data: EvaluationCreate, coach_id: int) -> Optional[Evaluation]:
        """Registra avaliação de fundamentos (RN-03: notas 1-5)."""
        athlete = self._verify_athlete_ownership(evaluation_data.athlete_id, coach_id)
        if not athlete:
            return None

        evaluation = Evaluation(
            athlete_id=evaluation_data.athlete_id,
            evaluator_id=coach_id,
            date=datetime.utcnow(),
            pass_rating=evaluation_data.pass_rating,
            serve_rating=evaluation_data.serve_rating,
            attack_rating=evaluation_data.attack_rating,
            block_rating=evaluation_data.block_rating,
            defense_rating=evaluation_data.defense_rating,
            notes=evaluation_data.notes,
        )
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def get_evaluation(self, evaluation_id: int, coach_id: int) -> Optional[Evaluation]:
        """Busca avaliação por ID."""
        return (
            self.db.query(Evaluation)
            .join(Athlete, Evaluation.athlete_id == Athlete.id)
            .join(Team, Athlete.team_id == Team.id)
            .filter(Evaluation.id == evaluation_id, Team.coach_id == coach_id)
            .first()
        )

    def get_athlete_evaluations(self, athlete_id: int, coach_id: int) -> List[Evaluation]:
        """Lista avaliações de um atleta (histórico - RF-21)."""
        athlete = self._verify_athlete_ownership(athlete_id, coach_id)
        if not athlete:
            return []

        return (
            self.db.query(Evaluation)
            .filter(Evaluation.athlete_id == athlete_id)
            .order_by(Evaluation.date.desc())
            .all()
        )

    def update_evaluation(
        self, evaluation_id: int, coach_id: int, evaluation_data: EvaluationUpdate
    ) -> Optional[Evaluation]:
        """Atualiza avaliação (RF-22)."""
        evaluation = self.get_evaluation(evaluation_id, coach_id)
        if not evaluation:
            return None

        update_data = evaluation_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(evaluation, field, value)

        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def delete_evaluation(self, evaluation_id: int, coach_id: int) -> bool:
        """Exclui avaliação (RF-22)."""
        evaluation = self.get_evaluation(evaluation_id, coach_id)
        if not evaluation:
            return False

        self.db.delete(evaluation)
        self.db.commit()
        return True

    def get_athlete_evolution(self, athlete_id: int, coach_id: int) -> Optional[AthleteEvolution]:
        """Dados para gráfico de evolução (RF-24)."""
        athlete = self._verify_athlete_ownership(athlete_id, coach_id)
        if not athlete:
            return None

        evaluations = self.get_athlete_evaluations(athlete_id, coach_id)

        eval_summaries = [
            EvaluationSummary(
                date=e.date,
                pass_rating=e.pass_rating,
                serve_rating=e.serve_rating,
                attack_rating=e.attack_rating,
                block_rating=e.block_rating,
                defense_rating=e.defense_rating,
                average=round(
                    (e.pass_rating + e.serve_rating + e.attack_rating + e.block_rating + e.defense_rating) / 5, 2
                ),
            )
            for e in evaluations
        ]

        # Percentual de presença
        from app.models.attendance import Attendance
        from app.models.training import Training

        total_trainings = (
            self.db.query(func.count(Training.id))
            .filter(Training.team_id == athlete.team_id)
            .scalar()
        )
        present_count = (
            self.db.query(func.count(Attendance.id))
            .filter(Attendance.athlete_id == athlete_id, Attendance.present == True)
            .scalar()
        )
        attendance_percentage = None
        if total_trainings and total_trainings > 0:
            attendance_percentage = round((present_count / total_trainings) * 100, 1)

        return AthleteEvolution(
            athlete_id=athlete.id,
            athlete_name=athlete.name,
            evaluations=eval_summaries,
            attendance_percentage=attendance_percentage,
        )