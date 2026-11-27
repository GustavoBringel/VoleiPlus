"""Testes de avaliações (Issues #22, #23)."""
import pytest
from datetime import date, datetime
from fastapi.testclient import TestClient


class TestEvaluations:
    """Testes de avaliações de fundamentos."""

    def test_create_evaluation_success(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """Deve registrar avaliação com notas 1-5 (RF-19, RN-03)."""
        response = client.post(
            "/api/v1/evaluations",
            json={
                "athlete_id": test_athlete.id,
                "pass_rating": 4,
                "serve_rating": 3,
                "attack_rating": 5,
                "block_rating": 2,
                "defense_rating": 4,
                "notes": "Bom passe, precisa melhorar bloqueio",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["athlete_id"] == test_athlete.id
        assert data["pass_rating"] == 4
        assert data["serve_rating"] == 3
        assert data["attack_rating"] == 5
        assert data["block_rating"] == 2
        assert data["defense_rating"] == 4
        assert data["evaluator_id"] == 1

    def test_create_evaluation_invalid_rating(self, client: TestClient, auth_headers, test_athlete):
        """Deve rejeitar nota fora da escala 1-5 (RN-03)."""
        response = client.post(
            "/api/v1/evaluations",
            json={
                "athlete_id": test_athlete.id,
                "pass_rating": 6,  # inválido
                "serve_rating": 3,
                "attack_rating": 5,
                "block_rating": 2,
                "defense_rating": 4,
            },
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_create_evaluation_zero_rating(self, client: TestClient, auth_headers, test_athlete):
        """Deve rejeitar nota zero (RN-03)."""
        response = client.post(
            "/api/v1/evaluations",
            json={
                "athlete_id": test_athlete.id,
                "pass_rating": 0,
                "serve_rating": 3,
                "attack_rating": 5,
                "block_rating": 2,
                "defense_rating": 4,
            },
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_list_athlete_evaluations_history(self, client: TestClient, auth_headers, db_session, test_athlete):
        """Deve listar histórico de avaliações (RF-21)."""
        from app.models.evaluation import Evaluation

        eval1 = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 1, 1),
            pass_rating=3, serve_rating=3, attack_rating=3, block_rating=3, defense_rating=3,
        )
        eval2 = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 2, 1),
            pass_rating=4, serve_rating=4, attack_rating=4, block_rating=4, defense_rating=4,
        )
        db_session.add_all([eval1, eval2])
        db_session.commit()

        response = client.get(f"/api/v1/evaluations/athlete/{test_athlete.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Ordem decrescente por data
        assert data[0]["pass_rating"] == 4
        assert data[1]["pass_rating"] == 3

    def test_get_athlete_evolution_for_chart(self, client: TestClient, auth_headers, db_session, test_athlete, test_team):
        """Deve retornar dados para gráfico de evolução (RF-24)."""
        from app.models.evaluation import Evaluation
        from app.models.training import Training
        from app.models.attendance import Attendance

        # Avaliações em datas diferentes
        eval1 = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 1, 1),
            pass_rating=2, serve_rating=2, attack_rating=2, block_rating=2, defense_rating=2,
        )
        eval2 = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 2, 1),
            pass_rating=3, serve_rating=3, attack_rating=3, block_rating=3, defense_rating=3,
        )
        eval3 = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 3, 1),
            pass_rating=4, serve_rating=4, attack_rating=4, block_rating=4, defense_rating=4,
        )
        db_session.add_all([eval1, eval2, eval3])
        db_session.commit()

        # Treinos para cálculo de presença
        trainings = [
            Training(team_id=test_team.id, date=date(2026, 1, 1), theme="T1"),
            Training(team_id=test_team.id, date=date(2026, 1, 15), theme="T2"),
        ]
        db_session.add_all(trainings)
        db_session.commit()
        for t in trainings:
            db_session.refresh(t)

        db_session.add_all([
            Attendance(training_id=trainings[0].id, athlete_id=test_athlete.id, present=True),
            Attendance(training_id=trainings[1].id, athlete_id=test_athlete.id, present=True),
        ])
        db_session.commit()

        response = client.get(f"/api/v1/evaluations/athlete/{test_athlete.id}/evolution", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["athlete_id"] == test_athlete.id
        assert data["athlete_name"] == "Atleta Teste"
        assert len(data["evaluations"]) == 3
        # Verifica média calculada
        assert data["evaluations"][0]["average"] == 2.0
        assert data["evaluations"][1]["average"] == 3.0
        assert data["evaluations"][2]["average"] == 4.0
        assert data["attendance_percentage"] == 100.0

    def test_update_evaluation(self, client: TestClient, auth_headers, db_session, test_athlete):
        """Deve atualizar avaliação (RF-22)."""
        from app.models.evaluation import Evaluation

        eval = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 1, 1),
            pass_rating=3, serve_rating=3, attack_rating=3, block_rating=3, defense_rating=3,
        )
        db_session.add(eval)
        db_session.commit()
        db_session.refresh(eval)

        response = client.put(
            f"/api/v1/evaluations/{eval.id}",
            json={"pass_rating": 5, "notes": "Atualizado"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["pass_rating"] == 5
        assert data["notes"] == "Atualizado"

    def test_delete_evaluation(self, client: TestClient, auth_headers, db_session, test_athlete):
        """Deve excluir avaliação (RF-22)."""
        from app.models.evaluation import Evaluation

        eval = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=datetime(2026, 1, 1),
            pass_rating=3, serve_rating=3, attack_rating=3, block_rating=3, defense_rating=3,
        )
        db_session.add(eval)
        db_session.commit()
        db_session.refresh(eval)

        response = client.delete(f"/api/v1/evaluations/{eval.id}", headers=auth_headers)
        assert response.status_code == 204

        response = client.get(f"/api/v1/evaluations/athlete/{test_athlete.id}", headers=auth_headers)
        data = response.json()
        assert len(data) == 0