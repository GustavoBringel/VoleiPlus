"""Testes de equipes (Issue #12)."""
import pytest
from fastapi.testclient import TestClient


class TestTeams:
    """Testes CRUD de equipes."""

    def test_create_team_success(self, client: TestClient, auth_headers):
        """Deve criar equipe para o treinador logado."""
        response = client.post(
            "/api/v1/teams",
            json={"name": "Vôlei Masters", "category": "adulto"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Vôlei Masters"
        assert data["category"] == "adulto"
        assert data["coach_id"] == 1  # test_user.id
        assert data["is_active"] is True

    def test_create_team_unauthorized(self, client: TestClient):
        """Deve rejeitar sem autenticação."""
        response = client.post(
            "/api/v1/teams",
            json={"name": "Time", "category": "sub-15"},
        )
        assert response.status_code == 401

    def test_list_teams(self, client: TestClient, auth_headers, test_team):
        """Deve listar equipes do treinador."""
        response = client.get("/api/v1/teams", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["name"] == "Time Teste"

    def test_get_team(self, client: TestClient, auth_headers, test_team):
        """Deve buscar equipe por ID."""
        response = client.get(f"/api/v1/teams/{test_team.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_team.id
        assert data["name"] == "Time Teste"

    def test_get_team_not_found(self, client: TestClient, auth_headers):
        """Deve retornar 404 para equipe inexistente."""
        response = client.get("/api/v1/teams/999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_team(self, client: TestClient, auth_headers, test_team):
        """Deve atualizar equipe."""
        response = client.put(
            f"/api/v1/teams/{test_team.id}",
            json={"name": "Novo Nome", "category": "sub-17"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Novo Nome"
        assert data["category"] == "sub-17"

    def test_update_team_not_found(self, client: TestClient, auth_headers):
        """Deve retornar 404 ao atualizar inexistente."""
        response = client.put(
            "/api/v1/teams/999",
            json={"name": "X"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_delete_team_no_trainings(self, client: TestClient, auth_headers, db_session, test_user):
        """Deve excluir equipe sem treinos."""
        from app.models.team import Team
        team = Team(name="Para Excluir", category="adulto", coach_id=test_user.id)
        db_session.add(team)
        db_session.commit()
        db_session.refresh(team)

        response = client.delete(f"/api/v1/teams/{team.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verifica se foi excluído
        response = client.get(f"/api/v1/teams/{team.id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_team_with_trainings_inactivates(self, client: TestClient, auth_headers, db_session, test_team):
        """Deve apenas inativar equipe que tem treinos (RN-06)."""
        from app.models.training import Training
        from datetime import date

        # Cria treino para a equipe
        training = Training(team_id=test_team.id, date=date.today(), theme="Treino teste")
        db_session.add(training)
        db_session.commit()

        response = client.delete(f"/api/v1/teams/{test_team.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verifica se foi apenas inativada
        response = client.get(f"/api/v1/teams/{test_team.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False