"""Rotas de avaliações (Issue #22, #23)."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_coach
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationResponse,
    AthleteEvolution,
)
from app.services.evaluation_service import EvaluationService
from app.models.user import User

router = APIRouter(prefix="/evaluations", tags=["Avaliações"])


@router.post("", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
def create_evaluation(
    evaluation_data: EvaluationCreate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Registra avaliação de fundamentos (RF-19, RN-03: notas 1-5).
    """
    service = EvaluationService(db)
    evaluation = service.create_evaluation(evaluation_data, current_user.id)
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta não encontrado ou não pertence a você",
        )
    return evaluation


@router.get("/athlete/{athlete_id}", response_model=List[EvaluationResponse])
def list_athlete_evaluations(
    athlete_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Lista histórico de avaliações do atleta (RF-21).
    """
    service = EvaluationService(db)
    evaluations = service.get_athlete_evaluations(athlete_id, current_user.id)
    return evaluations


@router.get("/athlete/{athlete_id}/evolution", response_model=AthleteEvolution)
def get_athlete_evolution(
    athlete_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Dados para gráfico de evolução do atleta (RF-24).
    """
    service = EvaluationService(db)
    evolution = service.get_athlete_evolution(athlete_id, current_user.id)
    if not evolution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return evolution


@router.put("/{evaluation_id}", response_model=EvaluationResponse)
def update_evaluation(
    evaluation_id: int,
    evaluation_data: EvaluationUpdate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Atualiza avaliação (RF-22).
    """
    service = EvaluationService(db)
    evaluation = service.update_evaluation(evaluation_id, current_user.id, evaluation_data)
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada")
    return evaluation


@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evaluation(
    evaluation_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Exclui avaliação (RF-22).
    """
    service = EvaluationService(db)
    success = service.delete_evaluation(evaluation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada")
    return None