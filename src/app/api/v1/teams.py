"""Rotas de equipes (Issue #12)."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_coach
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse, TeamWithAthletes
from app.services.team_service import TeamService
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["Equipes"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Cria nova equipe (RF-05).
    """
    service = TeamService(db)
    team = service.create_team(team_data, current_user.id)
    return team


@router.get("", response_model=List[TeamWithAthletes])
def list_teams(
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Lista equipes do treinador (RF-06).
    """
    service = TeamService(db)
    teams = service.get_teams(current_user.id)
    result = []
    for team in teams:
        athletes_count = service.get_team_with_athletes_count(team.id, current_user.id)
        result.append(
            TeamWithAthletes(
                id=team.id,
                name=team.name,
                category=team.category,
                coach_id=team.coach_id,
                is_active=team.is_active,
                created_at=team.created_at,
                updated_at=team.updated_at,
                athletes_count=athletes_count["athletes_count"] if athletes_count else 0,
            )
        )
    return result


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Busca equipe por ID.
    """
    service = TeamService(db)
    team = service.get_team(team_id, current_user.id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipe não encontrada")
    return team


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Atualiza equipe (RF-05).
    """
    service = TeamService(db)
    team = service.update_team(team_id, current_user.id, team_data)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipe não encontrada")
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Exclui ou inativa equipe (RF-05, RN-06).
    """
    service = TeamService(db)
    success = service.delete_team(team_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipe não encontrada")
    return None