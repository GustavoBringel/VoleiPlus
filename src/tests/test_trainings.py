"""Testes de treinos (Issue #18)."""
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient


class TestTrainings:
    """Testes CRUD de treinos."""

    def test_create_training_success(self, client: TestClient, auth_headers, test_team):
        """Deve registrar treino (RF-12)."""
        today = date.today().isoformat()
        response = client.post(
            "/api/v1/trainings",
            json={
                "team_id": test_team.id,
                "date": today,
                "theme": "Fundamentos de passe",
                "notes": "Foco no passe alto",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["team_id"] == test_team.id
        assert data["theme"] == "Fundamentos de passe"
        assert data["date"] == today

    def test_create_training_wrong_team(self, client: TestClient, auth_headers, db_session, test_user):
        """Deve rejeitar treino em equipe de outro treinador."""
        from app.models.team import Team
        other_team = Team(name="Outro", category="adulto", coach_id=999)
        db_session.add(other_team)
        db_session.commit()
        db_session.refresh(other_team)

        response = client.post(
            "/api/v1/trainings",
            json={
                "team_id": other_team.id,
                "date": date.today().isoformat(),
                "theme": "Treino",
            },
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_list_trainings_chronological(self, client: TestClient, auth_headers, db_session, test_team):
        """Deve listar treinos em ordem cronológica (RF-14)."""
        from app.models.training import Training
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Cria fora de ordem
        db_session.add_all([
            Training(team_id=test_team.id, date=today, theme="Hoje"),
            Training(team_id=test_team.id, date=yesterday, theme="Ontem"),
            Training(team_id=test_team.id, date=tomorrow, theme="Amanhã"),
        ])
        db_session.commit()

        response = client.get(f"/api/v1/trainings?team_id={test_team.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # Deve vir em ordem decrescente (mais recente primeiro)
        assert data[0]["theme"] == "Amanhã"
        assert data[1]["theme"] == "Hoje"
        assert data[2]["theme"] == "Ontem"

    def test_get_training_with_attendance(self, client: TestClient, auth_headers, db_session, test_team):
        """Deve buscar treino com resumo de presença."""
        from app.models.training import Training
        training = Training(team_id=test_team.id, date=date.today(), theme="Treino com presença")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        response = client.get(f"/api/v1/trainings/{training.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == training.id
        assert "attendances_count" in data
        assert "present_count" in data

    def test_update_training(self, client: TestClient, auth_headers, db_session, test_team):
        """Deve atualizar treino (RF-13)."""
        from app.models.training import Training
        training = Training(team_id=test_team.id, date=date.today(), theme="Original")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        response = client.put(
            f"/api/v1/trainings/{training.id}",
            json={"theme": "Atualizado", "notes": "Nova observação"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["theme"] == "Atualizado"
        assert data["notes"] == "Nova observação"

    def test_delete_training(self, client: TestClient, auth_headers, db_session, test_team):
        """Deve excluir treino (RF-13)."""
        from app.models.training import Training
        training = Training(team_id=test_team.id, date=date.today(), theme="Para Excluir")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        response = client.delete(f"/api/v1/trainings/{training.id}", headers=auth_headers)
        assert response.status_code == 204

        response = client.get(f"/api/v1/trainings/{training.id}", headers=auth_headers)
        assert response.status_code == 404