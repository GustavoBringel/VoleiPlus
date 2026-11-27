"""Serviço de autenticação e autorização."""
from datetime import timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserLogin, Token, TokenData


class AuthService:
    """Serviço para operações de autenticação."""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Cria novo usuário (treinador)."""
        # Verifica se email já existe
        existing = self.db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise ValueError("Email já cadastrado")

        hashed_password = get_password_hash(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=UserRole.COACH,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, login_data: UserLogin) -> Optional[User]:
        """Autentica usuário com email e senha."""
        user = self.db.query(User).filter(User.email == login_data.email).first()
        if not user:
            return None
        if not user.is_active:
            return None
        if not verify_password(login_data.password, user.hashed_password):
            return None
        return user

    def create_token(self, user: User) -> Token:
        """Cria token de acesso para usuário autenticado."""
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value,
            }
        )
        return Token(access_token=access_token)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email."""
        return self.db.query(User).filter(User.email == email).first()

    def verify_token(self, token: str) -> TokenData:
        """Verifica e decodifica token JWT."""
        payload = decode_token(token)
        return TokenData(
            user_id=int(payload.get("sub")),
            email=payload.get("email"),
            role=payload.get("role"),
        )