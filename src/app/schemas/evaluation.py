"""Schemas Pydantic para Avaliação."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, field_validator


class EvaluationBase(BaseModel):
    """Campos base da avaliação."""
    athlete_id: int
    pass_rating: int = Field(..., ge=1, le=5)
    serve_rating: int = Field(..., ge=1, le=5)
    attack_rating: int = Field(..., ge=1, le=5)
    block_rating: int = Field(..., ge=1, le=5)
    defense_rating: int = Field(..., ge=1, le=5)
    notes: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    """Schema para criação de avaliação."""
    pass


class EvaluationUpdate(BaseModel):
    """Schema para atualização de avaliação."""
    pass_rating: Optional[int] = Field(None, ge=1, le=5)
    serve_rating: Optional[int] = Field(None, ge=1, le=5)
    attack_rating: Optional[int] = Field(None, ge=1, le=5)
    block_rating: Optional[int] = Field(None, ge=1, le=5)
    defense_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class EvaluationResponse(EvaluationBase):
    """Schema de resposta da avaliação."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    evaluator_id: int
    date: datetime
    created_at: datetime
    updated_at: datetime


class EvaluationSummary(BaseModel):
    """Resumo de avaliação para gráficos."""
    date: datetime
    pass_rating: int
    serve_rating: int
    attack_rating: int
    block_rating: int
    defense_rating: int
    average: float


class AthleteEvolution(BaseModel):
    """Dados de evolução do atleta para gráficos."""
    athlete_id: int
    athlete_name: str
    evaluations: List[EvaluationSummary]
    attendance_percentage: Optional[float] = None