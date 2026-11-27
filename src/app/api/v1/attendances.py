"""Rotas de presença (Issue #19)."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_coach
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceBulkCreate,
    AttendanceBulkResponse,
)
from app.services.attendance_service import AttendanceService
from app.models.user import User

router = APIRouter(prefix="/attendances", tags=["Presença"])


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def register_attendance(
    attendance_data: AttendanceCreate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Registra presença de um atleta em um treino (RF-15, RN-02: upsert).
    """
    service = AttendanceService(db)
    attendance = service.register_attendance(attendance_data, current_user.id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino ou atleta não encontrado",
        )
    return attendance


@router.post("/bulk", response_model=AttendanceBulkResponse)
def bulk_register_attendance(
    bulk_data: AttendanceBulkCreate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Registra presença em lote (chamada) - mobile first (RF-15, RF-16, RNF-01).
    """
    service = AttendanceService(db)
    result = service.bulk_register_attendance(bulk_data, current_user.id)
    if "errors" in result and result["errors"] and result["saved"] == 0 and result["updated"] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["errors"][0])
    return AttendanceBulkResponse(
        training_id=bulk_data.training_id,
        saved=result["saved"],
        updated=result["updated"],
    )


@router.get("/training/{training_id}", response_model=List[AttendanceResponse])
def list_training_attendances(
    training_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Lista presenças de um treino.
    """
    service = AttendanceService(db)
    attendances = service.get_training_attendances(training_id, current_user.id)
    return attendances


@router.put("/{training_id}/athletes/{athlete_id}", response_model=AttendanceResponse)
def update_attendance(
    training_id: int,
    athlete_id: int,
    attendance_data: AttendanceUpdate,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Corrige presença já registrada (RF-17).
    """
    service = AttendanceService(db)
    attendance = service.update_attendance(training_id, athlete_id, current_user.id, attendance_data)
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de presença não encontrado")
    return attendance


@router.get("/athlete/{athlete_id}/stats")
def get_athlete_attendance_stats(
    athlete_id: int,
    current_user: User = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    """
    Estatísticas de presença do atleta - percentual por período (RF-18).
    """
    service = AttendanceService(db)
    stats = service.get_athlete_attendance_stats(athlete_id, current_user.id)
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return stats