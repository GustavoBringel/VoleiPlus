"""Testes de presença (Issue #19)."""
import pytest
from datetime import date
from fastapi.testclient import TestClient


class TestAttendances:
    """Testes de registro e consulta de presença."""

    def setup_method(self):
        """Setup para cada teste: cria treino e atletas."""
        pass  # fixtures cuidam disso

    def test_register_single_attendance(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve registrar presença de um atleta (RF-15)."""
        from app.models.training import Training
        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        response = client.post(
            "/api/v1/attendances",
            json={
                "training_id": training.id,
                "athlete_id": test_athlete.id,
                "present": True,
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["training_id"] == training.id
        assert data["athlete_id"] == test_athlete.id
        assert data["present"] is True

    def test_rn02_upsert_attendance(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """RN-02: Deve atualizar presença existente (não duplicar)."""
        from app.models.training import Training
        from app.models.attendance import Attendance

        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        # Primeira vez: presente
        response = client.post(
            "/api/v1/attendances",
            json={"training_id": training.id, "athlete_id": test_athlete.id, "present": True},
            headers=auth_headers,
        )
        assert response.status_code == 201
        first_id = response.json()["id"]

        # Segunda vez: ausente (deve atualizar o mesmo registro)
        response = client.post(
            "/api/v1/attendances",
            json={"training_id": training.id, "athlete_id": test_athlete.id, "present": False},
            headers=auth_headers,
        )
        assert response.status_code == 201
        second_id = response.json()["id"]

        # Deve ser o mesmo ID (upsert)
        assert first_id == second_id

        # Verifica no banco
        attendances = db_session.query(Attendance).filter(
            Attendance.training_id == training.id,
            Attendance.athlete_id == test_athlete.id,
        ).all()
        assert len(attendances) == 1
        assert attendances[0].present is False

    def test_bulk_register_attendance_chamada(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve registrar chamada em lote (mobile first - RNF-01)."""
        from app.models.training import Training
        from app.models.athlete import Athlete

        # Cria mais atletas
        athlete2 = Athlete(team_id=test_team.id, name="Atleta 2", birth_date=date(2000, 1, 1))
        athlete3 = Athlete(team_id=test_team.id, name="Atleta 3", birth_date=date(2001, 1, 1))
        db_session.add_all([athlete2, athlete3])
        db_session.commit()
        db_session.refresh(athlete2)
        db_session.refresh(athlete3)

        training = Training(team_id=test_team.id, date=date.today(), theme="Treino chamada")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        response = client.post(
            "/api/v1/attendances/bulk",
            json={
                "training_id": training.id,
                "attendances": [
                    {"training_id": training.id, "athlete_id": test_athlete.id, "present": True},
                    {"training_id": training.id, "athlete_id": athlete2.id, "present": True},
                    {"training_id": training.id, "athlete_id": athlete3.id, "present": False},
                ],
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["training_id"] == training.id
        assert data["saved"] == 3
        assert data["updated"] == 0

    def test_bulk_register_updates_existing(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve atualizar presenças existentes no bulk (RN-02)."""
        from app.models.training import Training
        from app.models.attendance import Attendance

        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        # Presença prévia
        existing = Attendance(training_id=training.id, athlete_id=test_athlete.id, present=False)
        db_session.add(existing)
        db_session.commit()

        response = client.post(
            "/api/v1/attendances/bulk",
            json={
                "training_id": training.id,
                "attendances": [
                    {"training_id": training.id, "athlete_id": test_athlete.id, "present": True},
                ],
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["saved"] == 0
        assert data["updated"] == 1

    def test_list_training_attendances(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve listar presenças de um treino."""
        from app.models.training import Training
        from app.models.attendance import Attendance

        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        att = Attendance(training_id=training.id, athlete_id=test_athlete.id, present=True)
        db_session.add(att)
        db_session.commit()

        response = client.get(f"/api/v1/attendances/training/{training.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["athlete_id"] == test_athlete.id
        assert data[0]["present"] is True

    def test_update_attendance_correction(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve corrigir presença já registrada (RF-17)."""
        from app.models.training import Training
        from app.models.attendance import Attendance

        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        att = Attendance(training_id=training.id, athlete_id=test_athlete.id, present=True)
        db_session.add(att)
        db_session.commit()
        db_session.refresh(att)

        response = client.put(
            f"/api/v1/attendances/{training.id}/athletes/{test_athlete.id}",
            json={"present": False},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["present"] is False

    def test_athlete_attendance_stats(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve retornar estatísticas de presença do atleta (RF-18)."""
        from app.models.training import Training
        from app.models.attendance import Attendance

        # 3 treinos
        trainings = [
            Training(team_id=test_team.id, date=date(2026, 1, 1), theme="T1"),
            Training(team_id=test_team.id, date=date(2026, 1, 8), theme="T2"),
            Training(team_id=test_team.id, date=date(2026, 1, 15), theme="T3"),
        ]
        db_session.add_all(trainings)
        db_session.commit()
        for t in trainings:
            db_session.refresh(t)

        # Presente em 2 de 3
        db_session.add_all([
            Attendance(training_id=trainings[0].id, athlete_id=test_athlete.id, present=True),
            Attendance(training_id=trainings[1].id, athlete_id=test_athlete.id, present=True),
            Attendance(training_id=trainings[2].id, athlete_id=test_athlete.id, present=False),
        ])
        db_session.commit()

        response = client.get(f"/api/v1/attendances/athlete/{test_athlete.id}/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total_trainings"] == 3
        assert data["present_count"] == 2
        assert data["attendance_percentage"] == 66.7