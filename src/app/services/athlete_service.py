"""Serviço de atletas."""
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.athlete import Athlete
from app.models.team import Team
from app.schemas.athlete import AthleteCreate, AthleteUpdate


class AthleteService:
    """Serviço para operações de atletas."""

    def __init__(self, db: Session):
        self.db = db

    def _verify_team_ownership(self, team_id: int, coach_id: int) -> Optional[Team]:
        """Verifica se a equipe pertence ao treinador."""
        return (
            self.db.query(Team)
            .filter(Team.id == team_id, Team.coach_id == coach_id)
            .first()
        )

    def create_athlete(self, athlete_data: AthleteCreate, coach_id: int) -> Optional[Athlete]:
        """Cadastra atleta em uma equipe do treinador."""
        team = self._verify_team_ownership(athlete_data.team_id, coach_id)
        if not team:
            return None

        athlete = Athlete(
            team_id=athlete_data.team_id,
            name=athlete_data.name,
            birth_date=athlete_data.birth_date,
            position=athlete_data.position,
        )
        self.db.add(athlete)
        self.db.commit()
        self.db.refresh(athlete)
        return athlete

    def get_athlete(self, athlete_id: int, coach_id: int) -> Optional[Athlete]:
        """Busca atleta por ID (verificando se pertence a equipe do treinador)."""
        return (
            self.db.query(Athlete)
            .join(Team, Athlete.team_id == Team.id)
            .filter(Athlete.id == athlete_id, Team.coach_id == coach_id)
            .first()
        )

    def get_athletes(
        self,
        coach_id: int,
        team_id: Optional[int] = None,
        active_only: bool = True,
        search: Optional[str] = None,
    ) -> List[Athlete]:
        """Lista atletas das equipes do treinador."""
        query = (
            self.db.query(Athlete)
            .join(Team, Athlete.team_id == Team.id)
            .filter(Team.coach_id == coach_id)
        )

        if team_id:
            query = query.filter(Athlete.team_id == team_id)

        if active_only:
            query = query.filter(Athlete.is_active == True)

        if search:
            query = query.filter(Athlete.name.ilike(f"%{search}%"))

        return query.order_by(Athlete.name).all()

    def update_athlete(
        self, athlete_id: int, coach_id: int, athlete_data: AthleteUpdate
    ) -> Optional[Athlete]:
        """Atualiza atleta."""
        athlete = self.get_athlete(athlete_id, coach_id)
        if not athlete:
            return None

        # Se mudar de equipe, verifica se nova equipe pertence ao treinador
        if athlete_data.team_id is not None and athlete_data.team_id != athlete.team_id:
            new_team = self._verify_team_ownership(athlete_data.team_id, coach_id)
            if not new_team:
                return None

        update_data = athlete_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(athlete, field, value)

        self.db.commit()
        self.db.refresh(athlete)
        return athlete

    def deactivate_athlete(self, athlete_id: int, coach_id: int) -> bool:
        """Inativa atleta (RN-05: mantém histórico, some da chamada)."""
        athlete = self.get_athlete(athlete_id, coach_id)
        if not athlete:
            return False

        athlete.is_active = False
        self.db.commit()
        return True

    def get_athlete_with_details(self, athlete_id: int, coach_id: int) -> Optional[dict]:
        """Retorna atleta com contagens de presença e avaliações."""
        athlete = self.get_athlete(athlete_id, coach_id)
        if not athlete:
            return None

        from app.models.attendance import Attendance
        from app.models.evaluation import Evaluation
        from app.models.training import Training

        # Contagens
        attendances_count = (
            self.db.query(func.count(Attendance.id))
            .filter(Attendance.athlete_id == athlete_id)
            .scalar()
        )
        evaluations_count = (
            self.db.query(func.count(Evaluation.id))
            .filter(Evaluation.athlete_id == athlete_id)
            .scalar()
        )

        # Percentual de presença
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

        return {
            "athlete": athlete,
            "attendances_count": attendances_count,
            "evaluations_count": evaluations_count,
            "attendance_percentage": attendance_percentage,
        }