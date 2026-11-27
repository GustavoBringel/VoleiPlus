"""Serviço de presença."""
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.attendance import Attendance
from app.models.training import Training
from app.models.athlete import Athlete
from app.models.team import Team
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceBulkCreate


class AttendanceService:
    """Serviço para operações de presença."""

    def __init__(self, db: Session):
        self.db = db

    def _verify_training_ownership(self, training_id: int, coach_id: int) -> Optional[Training]:
        """Verifica se o treino pertence a uma equipe do treinador."""
        return (
            self.db.query(Training)
            .join(Team, Training.team_id == Team.id)
            .filter(Training.id == training_id, Team.coach_id == coach_id)
            .first()
        )

    def register_attendance(self, attendance_data: AttendanceCreate, coach_id: int) -> Optional[Attendance]:
        """Registra presença de um atleta em um treino (RN-02: upsert)."""
        training = self._verify_training_ownership(attendance_data.training_id, coach_id)
        if not training:
            return None

        # Verifica se atleta pertence à equipe do treino e está ativo
        athlete = (
            self.db.query(Athlete)
            .filter(
                Athlete.id == attendance_data.athlete_id,
                Athlete.team_id == training.team_id,
                Athlete.is_active == True,
            )
            .first()
        )
        if not athlete:
            return None

        # RN-02: Upsert - atualiza se já existe, cria se não existe
        existing = (
            self.db.query(Attendance)
            .filter(
                Attendance.training_id == attendance_data.training_id,
                Attendance.athlete_id == attendance_data.athlete_id,
            )
            .first()
        )

        if existing:
            existing.present = attendance_data.present
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            attendance = Attendance(
                training_id=attendance_data.training_id,
                athlete_id=attendance_data.athlete_id,
                present=attendance_data.present,
            )
            self.db.add(attendance)
            self.db.commit()
            self.db.refresh(attendance)
            return attendance

    def bulk_register_attendance(
        self, bulk_data: AttendanceBulkCreate, coach_id: int
    ) -> dict:
        """Registra presença em lote (chamada) - RN-02: upsert para cada."""
        training = self._verify_training_ownership(bulk_data.training_id, coach_id)
        if not training:
            return {"saved": 0, "updated": 0, "errors": ["Treino não encontrado"]}

        # Busca atletas ativos da equipe
        active_athletes = (
            self.db.query(Athlete.id)
            .filter(Athlete.team_id == training.team_id, Athlete.is_active == True)
            .all()
        )
        active_athlete_ids = {a.id for a in active_athletes}

        saved = 0
        updated = 0
        errors = []

        for att_data in bulk_data.attendances:
            if att_data.athlete_id not in active_athlete_ids:
                errors.append(f"Atleta {att_data.athlete_id} não pertence à equipe ou está inativo")
                continue

            existing = (
                self.db.query(Attendance)
                .filter(
                    Attendance.training_id == bulk_data.training_id,
                    Attendance.athlete_id == att_data.athlete_id,
                )
                .first()
            )

            if existing:
                existing.present = att_data.present
                updated += 1
            else:
                attendance = Attendance(
                    training_id=bulk_data.training_id,
                    athlete_id=att_data.athlete_id,
                    present=att_data.present,
                )
                self.db.add(attendance)
                saved += 1

        self.db.commit()
        return {"saved": saved, "updated": updated, "errors": errors}

    def get_attendance(self, training_id: int, athlete_id: int, coach_id: int) -> Optional[Attendance]:
        """Busca registro de presença específico."""
        training = self._verify_training_ownership(training_id, coach_id)
        if not training:
            return None

        return (
            self.db.query(Attendance)
            .filter(
                Attendance.training_id == training_id,
                Attendance.athlete_id == athlete_id,
            )
            .first()
        )

    def get_training_attendances(self, training_id: int, coach_id: int) -> List[Attendance]:
        """Lista todas as presenças de um treino."""
        training = self._verify_training_ownership(training_id, coach_id)
        if not training:
            return []

        return (
            self.db.query(Attendance)
            .filter(Attendance.training_id == training_id)
            .all()
        )

    def update_attendance(
        self, training_id: int, athlete_id: int, coach_id: int, attendance_data: AttendanceUpdate
    ) -> Optional[Attendance]:
        """Corrige presença já registrada (RF-17)."""
        attendance = self.get_attendance(training_id, athlete_id, coach_id)
        if not attendance:
            return None

        if attendance_data.present is not None:
            attendance.present = attendance_data.present

        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def get_athlete_attendance_stats(self, athlete_id: int, coach_id: int) -> Optional[dict]:
        """Estatísticas de presença do atleta (RF-18)."""
        # Verifica se atleta pertence ao treinador
        athlete = (
            self.db.query(Athlete)
            .join(Team, Athlete.team_id == Team.id)
            .filter(Athlete.id == athlete_id, Team.coach_id == coach_id)
            .first()
        )
        if not athlete:
            return None

        total_trainings = (
            self.db.query(func.count(Training.id))
            .filter(Training.team_id == athlete.team_id)
            .scalar()
        )
        total_attendances = (
            self.db.query(func.count(Attendance.id))
            .filter(Attendance.athlete_id == athlete_id)
            .scalar()
        )
        present_count = (
            self.db.query(func.count(Attendance.id))
            .filter(Attendance.athlete_id == athlete_id, Attendance.present == True)
            .scalar()
        )

        percentage = None
        if total_trainings and total_trainings > 0:
            percentage = round((present_count / total_trainings) * 100, 1)

        return {
            "athlete_id": athlete_id,
            "total_trainings": total_trainings,
            "total_attendances": total_attendances,
            "present_count": present_count,
            "attendance_percentage": percentage,
        }