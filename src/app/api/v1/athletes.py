"""Rotas de atletas (Issue #13)."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_coach
from app.schemas.athlete import (
    AthleteCreate,
    AthleteUpdate,
    AthleteResponse,
    AthleteWithDetails,
    AthleteProfile,
)
from app.services.athlete_service import AthleteService
from app.models.user import User

router = APIRouter(prefix="/athletes", tags=["Atletas"])


@router.post("", response_model=AthleteResponse, status_code=status.HTTP_201_CREATED)
def create_athlete(
    athlete_data: AthleteCreate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Cadastra atleta em uma equipe (RF-07, RF-09, RN-01).
    """
    service = AthleteService(db)
    athlete = service.create_athlete(athlete_data, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipe não encontrada ou não pertence a você",
        )
    return athlete


@router.get("", response_model=List[AthleteResponse])
def list_athletes(
    team_id: Optional[int] = Query(None, description="Filtrar por equipe"),
    active_only: bool = Query(True, description="Apenas atletas ativos"),
    search: Optional[str] = Query(None, description="Buscar por nome"),
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Lista atletas das equipes do treinador (RF-08, RF-10 opcional).
    """
    service = AthleteService(db)
    athletes = service.get_athletes(
        coach_id=current_user.id,
        team_id=team_id,
        active_only=active_only,
        search=search,
    )
    return athletes


@router.get("/{athlete_id}", response_model=AthleteWithDetails)
def get_athlete(
    athlete_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Busca atleta com detalhes (contagens, percentual de presença).
    """
    service = AthleteService(db)
    result = service.get_athlete_with_details(athlete_id, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    athlete = result["athlete"]
    return AthleteWithDetails(
        id=athlete.id,
        team_id=athlete.team_id,
        name=athlete.name,
        birth_date=athlete.birth_date,
        position=athlete.position,
        is_active=athlete.is_active,
        created_at=athlete.created_at,
        updated_at=athlete.updated_at,
        attendances_count=result["attendances_count"],
        evaluations_count=result["evaluations_count"],
        attendance_percentage=result["attendance_percentage"],
    )


@router.get("/{athlete_id}/profile", response_model=AthleteProfile)
def get_athlete_profile(
    athlete_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Perfil completo do atleta para tela de evolução (RF-23).
    """
    # Este endpoint será expandido quando integrar com attendance/evaluation services
    service = AthleteService(db)
    result = service.get_athlete_with_details(athlete_id, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    athlete = result["athlete"]
    # TODO: buscar attendances e evaluations completos
    return AthleteProfile(
        id=athlete.id,
        team_id=athlete.team_id,
        name=athlete.name,
        birth_date=athlete.birth_date,
        position=athlete.position,
        is_active=athlete.is_active,
        created_at=athlete.created_at,
        updated_at=athlete.updated_at,
        attendances_count=result["attendances_count"],
        evaluations_count=result["evaluations_count"],
        attendance_percentage=result["attendance_percentage"],
        team=None,
        attendances=[],
        evaluations=[],
    )


@router.put("/{athlete_id}", response_model=AthleteResponse)
def update_athlete(
    athlete_id: int,
    athlete_data: AthleteUpdate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Atualiza atleta (RF-08).
    """
    service = AthleteService(db)
    athlete = service.update_athlete(athlete_id, current_user.id, athlete_data)
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return athlete


@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_athlete(
    athlete_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Inativa atleta (RN-05: mantém histórico, some da chamada).
    """
    service = AthleteService(db)
    success = service.deactivate_athlete(athlete_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return None