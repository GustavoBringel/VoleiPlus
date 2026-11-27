"""Schemas Pydantic para Atleta."""
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class AthleteBase(BaseModel):
    """Campos base do atleta."""
    name: str = Field(..., min_length=1, max_length=150)
    birth_date: date
    position: Optional[str] = Field(None, max_length=50)


class AthleteCreate(AthleteBase):
    """Schema para criação de atleta."""
    team_id: int


class AthleteUpdate(BaseModel):
    """Schema para atualização de atleta."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    birth_date: Optional[date] = None
    position: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    team_id: Optional[int] = None


class AthleteResponse(AthleteBase):
    """Schema de resposta do atleta."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    team_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AthleteWithDetails(AthleteResponse):
    """Atleta com detalhes de presença e avaliações."""
    attendances_count: int = 0
    evaluations_count: int = 0
    attendance_percentage: Optional[float] = None


class AthleteProfile(AthleteResponse):
    """Perfil completo do atleta para tela de evolução."""
    team: Optional["TeamResponse"] = None
    attendances: List["AttendanceResponse"] = []
    evaluations: List["EvaluationResponse"] = []


# Forward references
from app.schemas.team import TeamResponse
from app.schemas.attendance import AttendanceResponse
from app.schemas.evaluation import EvaluationResponse
AthleteProfile.model_rebuild()