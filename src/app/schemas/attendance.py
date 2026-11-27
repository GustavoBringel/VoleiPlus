"""Schemas Pydantic para Presença."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class AttendanceBase(BaseModel):
    """Campos base da presença."""
    training_id: int
    athlete_id: int
    present: bool


class AttendanceCreate(AttendanceBase):
    """Schema para criação de presença."""
    pass


class AttendanceUpdate(BaseModel):
    """Schema para atualização de presença."""
    present: Optional[bool] = None


class AttendanceResponse(AttendanceBase):
    """Schema de resposta da presença."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class AttendanceBulkCreate(BaseModel):
    """Schema para registro de presença em lote (chamada)."""
    training_id: int
    attendances: List[AttendanceCreate]


class AttendanceBulkResponse(BaseModel):
    """Resposta do registro de presença em lote."""
    training_id: int
    saved: int
    updated: int