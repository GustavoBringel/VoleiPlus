"""Schemas Pydantic para Treino."""
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class TrainingBase(BaseModel):
    """Campos base do treino."""
    team_id: int
    date: date
    theme: str = Field(..., min_length=1, max_length=200)
    notes: Optional[str] = None


class TrainingCreate(TrainingBase):
    """Schema para criação de treino."""
    pass


class TrainingUpdate(BaseModel):
    """Schema para atualização de treino."""
    date: Optional[date] = None
    theme: Optional[str] = Field(None, min_length=1, max_length=200)
    notes: Optional[str] = None


class TrainingResponse(TrainingBase):
    """Schema de resposta do treino."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class TrainingWithAttendance(TrainingResponse):
    """Treino com informações de presença."""
    attendances_count: int = 0
    present_count: int = 0