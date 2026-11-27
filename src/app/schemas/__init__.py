"""Schemas package - todos os schemas Pydantic."""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
)
from app.schemas.team import (
    TeamBase,
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamWithAthletes,
    TeamDetail,
)
from app.schemas.athlete import (
    AthleteBase,
    AthleteCreate,
    AthleteUpdate,
    AthleteResponse,
    AthleteWithDetails,
    AthleteProfile,
)
from app.schemas.training import (
    TrainingBase,
    TrainingCreate,
    TrainingUpdate,
    TrainingResponse,
    TrainingWithAttendance,
)
from app.schemas.attendance import (
    AttendanceBase,
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceBulkCreate,
    AttendanceBulkResponse,
)
from app.schemas.evaluation import (
    EvaluationBase,
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationResponse,
    EvaluationSummary,
    AthleteEvolution,
)

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserLogin", "Token", "TokenData",
    # Team
    "TeamBase", "TeamCreate", "TeamUpdate", "TeamResponse", "TeamWithAthletes", "TeamDetail",
    # Athlete
    "AthleteBase", "AthleteCreate", "AthleteUpdate", "AthleteResponse", "AthleteWithDetails", "AthleteProfile",
    # Training
    "TrainingBase", "TrainingCreate", "TrainingUpdate", "TrainingResponse", "TrainingWithAttendance",
    # Attendance
    "AttendanceBase", "AttendanceCreate", "AttendanceUpdate", "AttendanceResponse", "AttendanceBulkCreate", "AttendanceBulkResponse",
    # Evaluation
    "EvaluationBase", "EvaluationCreate", "EvaluationUpdate", "EvaluationResponse", "EvaluationSummary", "AthleteEvolution",
]