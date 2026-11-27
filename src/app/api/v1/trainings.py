"""Rotas de treinos (Issue #18)."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_coach
from app.schemas.training import TrainingCreate, TrainingUpdate, TrainingResponse, TrainingWithAttendance
from app.services.training_service import TrainingService
from app.models.user import User

router = APIRouter(prefix="/trainings", tags=["Treinos"])


@router.post("", response_model=TrainingResponse, status_code=status.HTTP_201_CREATED)
def create_training(
    training_data: TrainingCreate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Registra novo treino (RF-12).
    """
    service = TrainingService(db)
    training = service.create_training(training_data, current_user.id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipe não encontrada ou não pertence a você",
        )
    return training


@router.get("", response_model=List[TrainingResponse])
def list_trainings(
    team_id: Optional[int] = None,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Lista treinos das equipes do treinador em ordem cronológica (RF-14).
    """
    service = TrainingService(db)
    trainings = service.get_trainings(current_user.id, team_id)
    return trainings


@router.get("/{training_id}", response_model=TrainingWithAttendance)
def get_training(
    training_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Busca treino com resumo de presença.
    """
    service = TrainingService(db)
    result = service.get_training_with_attendance(training_id, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treino não encontrado")

    training = result["training"]
    return TrainingWithAttendance(
        id=training.id,
        team_id=training.team_id,
        date=training.date,
        theme=training.theme,
        notes=training.notes,
        created_at=training.created_at,
        updated_at=training.updated_at,
        attendances_count=result["attendances_count"],
        present_count=result["present_count"],
    )


@router.put("/{training_id}", response_model=TrainingResponse)
def update_training(
    training_id: int,
    training_data: TrainingUpdate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Atualiza treino (RF-13).
    """
    service = TrainingService(db)
    training = service.update_training(training_id, current_user.id, training_data)
    if not training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treino não encontrado")
    return training


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training(
    training_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Exclui treino (RF-13).
    """
    service = TrainingService(db)
    success = service.delete_training(training_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treino não encontrado")
    return None