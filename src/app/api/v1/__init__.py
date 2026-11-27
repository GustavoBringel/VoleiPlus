"""API v1 routes."""
from app.api.v1 import auth, teams, athletes, trainings, attendances, evaluations

__all__ = ["auth", "teams", "athletes", "trainings", "attendances", "evaluations"]