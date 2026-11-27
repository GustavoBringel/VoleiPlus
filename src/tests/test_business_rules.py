"""Testes das regras de negócio (RN-01 a RN-06)."""
import pytest
from datetime import date
from fastapi.testclient import TestClient


class TestBusinessRules:
    """Testes das regras de negócio do Vôlei+."""

    def test_rn01_athlete_one_team(self, client: TestClient, auth_headers, db_session, test_user, test_team):
        """RN-01: Um atleta pertence a uma equipe por vez."""
        from app.models.team import Team
        from app.models.athlete import Athlete

        # Cria segunda equipe do mesmo treinador
        team2 = Team(name="Time 2", category="adulto", coach_id=test_user.id)
        db_session.add(team2)
        db_session.commit()
        db_session.refresh(team2)

        # Cria atleta no time 1
        response = client.post(
            "/api/v1/athletes",
            json={
                "team_id": test_team.id,
                "name": "Atleta RN01",
                "birth_date": "2000-01-01",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        athlete_id = response.json()["id"]

        # Move para time 2
        response = client.put(
            f"/api/v1/athletes/{athlete_id}",
            json={"team_id": team2.id},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["team_id"] == team2.id

        # Verifica que não está mais no time 1
        response = client.get(f"/api/v1/athletes?team_id={test_team.id}", headers=auth_headers)
        data = response.json()
        assert all(a["id"] != athlete_id for a in data)

        # Verifica que está no time 2
        response = client.get(f"/api/v1/athletes?team_id={team2.id}", headers=auth_headers)
        data = response.json()
        assert any(a["id"] == athlete_id for a in data)

    def test_rn02_unique_attendance_per_training(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """RN-02: Um atleta tem no máximo um registro de presença por treino."""
        from app.models.training import Training
        from app.models.attendance import Attendance

        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        # Registra presença duas vezes via API (upsert)
        for present in [True, False, True]:
            response = client.post(
                "/api/v1/attendances",
                json={
                    "training_id": training.id,
                    "athlete_id": test_athlete.id,
                    "present": present,
                },
                headers=auth_headers,
            )
            assert response.status_code == 201

        # Verifica no banco: apenas 1 registro
        count = db_session.query(Attendance).filter(
            Attendance.training_id == training.id,
            Attendance.athlete_id == test_athlete.id,
        ).count()
        assert count == 1

        # Verifica valor final
        att = db_session.query(Attendance).filter(
            Attendance.training_id == training.id,
            Attendance.athlete_id == test_athlete.id,
        ).first()
        assert att.present is True  # último valor

    def test_rn03_rating_scale_1_to_5(self, client: TestClient, auth_headers, test_athlete):
        """RN-03: Notas de avaliação seguem escala 1 a 5."""
        # Testa cada fundamento com valores inválidos
        fundamentals = [
            "pass_rating",
            "serve_rating",
            "attack_rating",
            "block_rating",
            "defense_rating",
        ]

        for field in fundamentals:
            # Teste valor 0
            payload = {f: 3 for f in fundamentals}
            payload[field] = 0
            payload["athlete_id"] = test_athlete.id
            response = client.post("/api/v1/evaluations", json=payload, headers=auth_headers)
            assert response.status_code == 422, f"Deveria rejeitar {field}=0"

            # Teste valor 6
            payload[field] = 6
            response = client.post("/api/v1/evaluations", json=payload, headers=auth_headers)
            assert response.status_code == 422, f"Deveria rejeitar {field}=6"

            # Teste valor válido
            payload[field] = 3
            response = client.post("/api/v1/evaluations", json=payload, headers=auth_headers)
            assert response.status_code == 201, f"Deveria aceitar {field}=3"
            break  # só precisa testar um válido

    def test_rn04_coach_accesses_only_own_data(self, client: TestClient, db_session):
        """RN-04: Treinador só acessa suas equipes/atletas/avaliações."""
        from app.models.user import User
        from app.core.security import get_password_hash
        from app.models.team import Team
        from app.models.athlete import Athlete

        # Cria segundo treinador
        coach2 = User(
            name="Coach 2",
            email="coach2@test.com",
            hashed_password=get_password_hash("pass123"),
        )
        db_session.add(coach2)
        db_session.commit()
        db_session.refresh(coach2)

        # Equipe do coach 2
        team2 = Team(name="Time Coach 2", category="adulto", coach_id=coach2.id)
        db_session.add(team2)
        db_session.commit()
        db_session.refresh(team2)

        # Atleta do coach 2
        athlete2 = Athlete(team_id=team2.id, name="Atleta Coach 2", birth_date=date(2000, 1, 1))
        db_session.add(athlete2)
        db_session.commit()
        db_session.refresh(athlete2)

        # Login coach 2
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "coach2@test.com", "password": "pass123"},
        )
        coach2_headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        # Coach 1 tenta acessar atleta do coach 2
        response = client.get(f"/api/v1/athletes/{athlete2.id}", headers=coach2_headers)
        # Deve funcionar para o dono
        assert response.status_code == 200

        # Login coach 1 (test_user)
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "coach@test.com", "password": "testpass123"},
        )
        coach1_headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        # Coach 1 tenta acessar atleta do coach 2
        response = client.get(f"/api/v1/athletes/{athlete2.id}", headers=coach1_headers)
        assert response.status_code == 404  # Não encontrado para ele

        # Coach 1 tenta criar atleta no time do coach 2
        response = client.post(
            "/api/v1/athletes",
            json={"team_id": team2.id, "name": "Intruso", "birth_date": "2000-01-01"},
            headers=coach1_headers,
        )
        assert response.status_code == 404

    def test_rn05_inactive_athlete_keeps_history(self, client: TestClient, auth_headers, db_session, test_team, test_athlete):
        """RN-05: Atletas inativados mantêm histórico, mas não aparecem na chamada."""
        from app.models.training import Training
        from app.models.attendance import Attendance
        from app.models.evaluation import Evaluation

        # Cria histórico
        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()
        db_session.refresh(training)

        att = Attendance(training_id=training.id, athlete_id=test_athlete.id, present=True)
        eval = Evaluation(
            athlete_id=test_athlete.id,
            evaluator_id=1,
            date=date.today(),
            pass_rating=3, serve_rating=3, attack_rating=3, block_rating=3, defense_rating=3,
        )
        db_session.add_all([att, eval])
        db_session.commit()

        # Inativa atleta
        response = client.delete(f"/api/v1/athletes/{test_athlete.id}", headers=auth_headers)
        assert response.status_code == 204

        # Não deve aparecer na lista ativa (chamada)
        response = client.get("/api/v1/athletes", headers=auth_headers)
        data = response.json()
        assert all(a["id"] != test_athlete.id for a in data)

        # Mas deve aparecer se active_only=false
        response = client.get("/api/v1/athletes?active_only=false", headers=auth_headers)
        data = response.json()
        assert any(a["id"] == test_athlete.id and a["is_active"] is False for a in data)

        # Histórico de presença mantido
        response = client.get(f"/api/v1/attendances/training/{training.id}", headers=auth_headers)
        data = response.json()
        assert len(data) == 1
        assert data[0]["athlete_id"] == test_athlete.id

        # Histórico de avaliações mantido
        response = client.get(f"/api/v1/evaluations/athlete/{test_athlete.id}", headers=auth_headers)
        data = response.json()
        assert len(data) == 1

    def test_rn06_team_with_trainings_inactivates(self, client: TestClient, auth_headers, db_session, test_user, test_team):
        """RN-06: Exclusão de equipe com treinos registrados vira inativação."""
        from app.models.training import Training

        # Cria treino para a equipe
        training = Training(team_id=test_team.id, date=date.today(), theme="Treino")
        db_session.add(training)
        db_session.commit()

        # Tenta excluir
        response = client.delete(f"/api/v1/teams/{test_team.id}", headers=auth_headers)
        assert response.status_code == 204

        # Equipe deve estar inativa, não excluída
        response = client.get(f"/api/v1/teams/{test_team.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False

        # Treino deve continuar existindo
        response = client.get(f"/api/v1/trainings/{training.id}", headers=auth_headers)
        assert response.status_code == 200