"""Testes de atletas (Issue #13)."""
import pytest
from datetime import date
from fastapi.testclient import TestClient


class TestAthletes:
    """Testes CRUD de atletas."""

    def test_create_athlete_success(self, client: TestClient, auth_headers, test_team):
        """Deve cadastrar atleta na equipe do treinador (RF-07, RF-09)."""
        response = client.post(
            "/api/v1/athletes",
            json={
                "team_id": test_team.id,
                "name": "Maria Silva",
                "birth_date": "2005-03-15",
                "position": "levantador",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Maria Silva"
        assert data["team_id"] == test_team.id
        assert data["position"] == "levantador"
        assert data["is_active"] is True

    def test_create_athlete_wrong_team(self, client: TestClient, auth_headers, db_session, test_user):
        """Deve rejeitar cadastro em equipe de outro treinador."""
        from app.models.team import Team
        other_team = Team(name="Outro Time", category="adulto", coach_id=999)
        db_session.add(other_team)
        db_session.commit()
        db_session.refresh(other_team)

        response = client.post(
            "/api/v1/athletes",
            json={
                "team_id": other_team.id,
                "name": "Atleta",
                "birth_date": "2000-01-01",
            },
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_list_athletes(self, client: TestClient, auth_headers, test_athlete):
        """Deve listar atletas do treinador (RF-08)."""
        response = client.get("/api/v1/athletes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["name"] == "Atleta Teste"

    def test_list_athletes_filter_by_team(self, client: TestClient, auth_headers, test_team, test_athlete):
        """Deve filtrar atletas por equipe."""
        response = client.get(f"/api/v1/athletes?team_id={test_team.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(a["team_id"] == test_team.id for a in data)

    def test_list_athletes_search(self, client: TestClient, auth_headers, test_athlete):
        """Deve buscar atletas por nome (RF-10 opcional)."""
        response = client.get("/api/v1/athletes?search=Teste", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "Teste" in data[0]["name"]

    def test_get_athlete(self, client: TestClient, auth_headers, test_athlete):
        """Deve buscar atleta com detalhes."""
        response = client.get(f"/api/v1/athletes/{test_athlete.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_athlete.id
        assert "attendances_count" in data
        assert "evaluations_count" in data
        assert "attendance_percentage" in data

    def test_get_athlete_profile(self, client: TestClient, auth_headers, test_athlete):
        """Deve retornar perfil completo para evolução (RF-23)."""
        response = client.get(f"/api/v1/athletes/{test_athlete.id}/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_athlete.id
        assert "attendances" in data
        assert "evaluations" in data

    def test_update_athlete(self, client: TestClient, auth_headers, test_athlete):
        """Deve atualizar atleta (RF-08)."""
        response = client.put(
            f"/api/v1/athletes/{test_athlete.id}",
            json={"name": "Novo Nome", "position": "líbero"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Novo Nome"
        assert data["position"] == "líbero"

    def test_deactivate_athlete(self, client: TestClient, auth_headers, test_athlete):
        """Deve inativar atleta (RN-05: mantém histórico)."""
        response = client.delete(f"/api/v1/athletes/{test_athlete.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verifica se está inativo
        response = client.get("/api/v1/athletes", headers=auth_headers)
        data = response.json()
        # Atletas inativos não devem aparecer na lista padrão (active_only=True)
        assert all(a["id"] != test_athlete.id for a in data)

        # Mas deve aparecer se active_only=False
        response = client.get("/api/v1/athletes?active_only=false", headers=auth_headers)
        data = response.json()
        assert any(a["id"] == test_athlete.id and a["is_active"] is False for a in data)

    def test_rn01_one_team_per_athlete(self, client: TestClient, auth_headers, db_session, test_user, test_team, test_athlete):
        """RN-01: Um atleta pertence a uma equipe por vez."""
        # Cria segunda equipe
        from app.models.team import Team
        team2 = Team(name="Time 2", category="adulto", coach_id=test_user.id)
        db_session.add(team2)
        db_session.commit()
        db_session.refresh(team2)

        # Tenta mover atleta para outra equipe (update team_id)
        response = client.put(
            f"/api/v1/athletes/{test_athlete.id}",
            json={"team_id": team2.id},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["team_id"] == team2.id

        # Atleta não existe mais na equipe antiga
        response = client.get(f"/api/v1/athletes?team_id={test_team.id}", headers=auth_headers)
        data = response.json()
        assert all(a["id"] != test_athlete.id for a in data)