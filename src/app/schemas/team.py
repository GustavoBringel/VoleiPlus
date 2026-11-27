"""Schemas Pydantic para Equipe."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class TeamBase(BaseModel):
    """Campos base da equipe."""
    name: str = Field(..., min_length=1, max_length=150)
    category: str = Field(..., min_length=1, max_length=50)


class TeamCreate(TeamBase):
    """Schema para criação de equipe."""
    pass


class TeamUpdate(BaseModel):
    """Schema para atualização de equipe."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None


class TeamResponse(TeamBase):
    """Schema de resposta da equipe."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    coach_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TeamWithAthletes(TeamResponse):
    """Equipe com lista de atletas."""
    athletes_count: int = 0


class TeamDetail(TeamResponse):
    """Equipe com detalhes completos."""
    athletes: List["AthleteResponse"] = []


# Forward reference resolution
from app.schemas.athlete import AthleteResponse
TeamDetail.model_rebuild()