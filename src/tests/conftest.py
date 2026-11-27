"""Configuração de testes com pytest."""
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.core.database import Base, get_db
from app.main import app
from app.models import User, UserRole, Team, Athlete, Training, Attendance, Evaluation  # noqa: F401
from app.services.auth_service import AuthService


# Banco de dados SQLite em arquivo para testes
TEST_DB_PATH = Path(__file__).parent / "test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria tabelas uma vez por sessão de testes."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink(missing_ok=True)


@pytest.fixture(scope="function")
def db_session():
    """Sessão para fixtures configurarem dados (com commit para persistir)."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Cliente de teste FastAPI - cada request usa sua própria sessão."""

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Cria usuário de teste (com commit para persistir no banco)."""
    from app.core.security import get_password_hash
    user = User(
        name="Test Coach",
        email="coach@test.com",
        hashed_password=get_password_hash("testpass123"),
        role=UserRole.COACH,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(db_session, test_user):
    """Headers de autenticação para usuário de teste (gera token diretamente)."""
    auth_service = AuthService(db_session)
    token = auth_service.create_token(test_user)
    return {"Authorization": f"Bearer {token.access_token}"}


@pytest.fixture
def test_team(db_session, test_user):
    """Cria equipe de teste."""
    team = Team(
        name="Time Teste",
        category="adulto",
        coach_id=test_user.id,
    )
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team


@pytest.fixture
def test_athlete(db_session, test_team):
    """Cria atleta de teste."""
    from datetime import date
    athlete = Athlete(
        team_id=test_team.id,
        name="Atleta Teste",
        birth_date=date(2000, 1, 1),
        position="ponteiro",
    )
    db_session.add(athlete)
    db_session.commit()
    db_session.refresh(athlete)
    return athlete