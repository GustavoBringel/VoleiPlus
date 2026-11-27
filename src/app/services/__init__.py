"""Services package - camada de negócio."""
from app.services.auth_service import AuthService
from app.services.team_service import TeamService
from app.services.athlete_service import AthleteService
from app.services.training_service import TrainingService
from app.services.attendance_service import AttendanceService
from app.services.evaluation_service import EvaluationService

__all__ = [
    "AuthService",
    "TeamService",
    "AthleteService",
    "TrainingService",
    "AttendanceService",
    "EvaluationService",
]