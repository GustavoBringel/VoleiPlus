"""Dependencies para injeção de dependências FastAPI."""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import SessionLocal
from app.core.security import decode_token
from app.models.user import User
from app.services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    """Dependency para sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency para AuthService."""
    return AuthService(db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Dependency para obter usuário atual autenticado."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = auth_service.verify_token(token)
        if token_data.user_id is None:
            raise credentials_exception
    except (ValueError, JWTError):
        raise credentials_exception

    user = auth_service.get_user_by_id(token_data.user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def get_current_coach(current_user: User = Depends(get_current_user)) -> User:
    """Dependency que garante que o usuário é um treinador (coach)."""
    if current_user.role.value != "coach" and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a treinadores",
        )
    return current_user