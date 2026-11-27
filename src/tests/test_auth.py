"""Testes de autenticação (Issue #10)."""
import pytest
from fastapi.testclient import TestClient


class TestAuthRegister:
    """Testes de cadastro de usuário."""

    def test_register_success(self, client: TestClient):
        """Deve cadastrar novo treinador com sucesso."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "name": "Novo Treinador",
                "email": "novo@test.com",
                "password": "senha123456",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "novo@test.com"
        assert data["name"] == "Novo Treinador"
        assert data["role"] == "coach"
        assert "id" in data
        assert "hashed_password" not in data  # não deve retornar senha

    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Deve rejeitar email duplicado."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "name": "Outro Treinador",
                "email": "coach@test.com",  # mesmo email do test_user
                "password": "senha123456",
            },
        )
        assert response.status_code == 400
        assert "já cadastrado" in response.json()["detail"].lower()

    def test_register_invalid_email(self, client: TestClient):
        """Deve rejeitar email inválido."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "name": "Treinador",
                "email": "email-invalido",
                "password": "senha123456",
            },
        )
        assert response.status_code == 422

    def test_register_short_password(self, client: TestClient):
        """Deve rejeitar senha muito curta."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "name": "Treinador",
                "email": "test@test.com",
                "password": "123",
            },
        )
        assert response.status_code == 422


class TestAuthLogin:
    """Testes de login."""

    def test_login_success(self, client: TestClient, test_user):
        """Deve fazer login e retornar token."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "coach@test.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user):
        """Deve rejeitar senha incorreta."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "coach@test.com", "password": "senhaerrada"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """Deve rejeitar usuário inexistente."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "naoexiste@test.com", "password": "senha123"},
        )
        assert response.status_code == 401

    def test_login_inactive_user(self, client: TestClient, db_session, test_user):
        """Deve rejeitar usuário inativo."""
        test_user.is_active = False
        db_session.commit()

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "coach@test.com", "password": "testpass123"},
        )
        assert response.status_code == 401


class TestAuthMe:
    """Testes do endpoint /me."""

    def test_me_success(self, client: TestClient, auth_headers):
        """Deve retornar dados do usuário autenticado."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "coach@test.com"
        assert data["role"] == "coach"

    def test_me_no_token(self, client: TestClient):
        """Deve rejeitar sem token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_me_invalid_token(self, client: TestClient):
        """Deve rejeitar token inválido."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer token-invalido"},
        )
        assert response.status_code == 401