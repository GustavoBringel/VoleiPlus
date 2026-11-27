"""Serviço de equipes."""
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.team import Team
from app.models.athlete import Athlete
from app.schemas.team import TeamCreate, TeamUpdate


class TeamService:
    """Serviço para operações de equipes."""

    def __init__(self, db: Session):
        self.db = db

    def create_team(self, team_data: TeamCreate, coach_id: int) -> Team:
        """Cria nova equipe para um treinador."""
        team = Team(
            name=team_data.name,
            category=team_data.category,
            coach_id=coach_id,
        )
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def get_team(self, team_id: int, coach_id: int) -> Optional[Team]:
        """Busca equipe por ID (apenas se pertencer ao treinador)."""
        return (
            self.db.query(Team)
            .filter(Team.id == team_id, Team.coach_id == coach_id)
            .first()
        )

    def get_teams(self, coach_id: int, active_only: bool = True) -> List[Team]:
        """Lista equipes do treinador."""
        query = self.db.query(Team).filter(Team.coach_id == coach_id)
        if active_only:
            query = query.filter(Team.is_active == True)
        return query.order_by(Team.created_at.desc()).all()

    def update_team(self, team_id: int, coach_id: int, team_data: TeamUpdate) -> Optional[Team]:
        """Atualiza equipe."""
        team = self.get_team(team_id, coach_id)
        if not team:
            return None

        update_data = team_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(team, field, value)

        self.db.commit()
        self.db.refresh(team)
        return team

    def delete_team(self, team_id: int, coach_id: int) -> bool:
        """Exclui (inativa) equipe. Se tiver treinos, apenas inativa (RN-06)."""
        team = self.get_team(team_id, coach_id)
        if not team:
            return False

        # Verifica se tem treinos
        trainings_count = self.db.query(func.count(Athlete.id)).join(Athlete.team).filter(Team.id == team_id).scalar()
        # Na verdade, verifica trainings diretamente:
        from app.models.training import Training
        trainings_count = self.db.query(func.count(Training.id)).filter(Training.team_id == team_id).scalar()

        if trainings_count > 0:
            # RN-06: Equipe com treinos registrados -> inativar
            team.is_active = False
            self.db.commit()
        else:
            # Sem treinos, pode excluir
            self.db.delete(team)
            self.db.commit()
        return True

    def get_team_with_athletes_count(self, team_id: int, coach_id: int) -> Optional[dict]:
        """Retorna equipe com contagem de atletas."""
        team = self.get_team(team_id, coach_id)
        if not team:
            return None

        athletes_count = (
            self.db.query(func.count(Athlete.id))
            .filter(Athlete.team_id == team_id, Athlete.is_active == True)
            .scalar()
        )
        return {
            "team": team,
            "athletes_count": athletes_count,
        }