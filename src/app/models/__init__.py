"""Models package - todos os modelos SQLAlchemy."""
from app.models.user import User, UserRole
from app.models.team import Team
from app.models.athlete import Athlete
from app.models.training import Training
from app.models.attendance import Attendance
from app.models.evaluation import Evaluation

__all__ = [
    "User",
    "UserRole",
    "Team",
    "Athlete",
    "Training",
    "Attendance",
    "Evaluation",
]