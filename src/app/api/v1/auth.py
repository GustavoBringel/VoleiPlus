"""Rotas de autenticação (Issue #10)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_auth_service, get_current_user
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """
    Cadastra novo treinador (RF-01).
    """
    try:
        user = auth_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    """
    Login e geração de token JWT (RF-02).
    """
    user = auth_service.authenticate(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_service.create_token(user)
    return token


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user=Depends(get_current_user)):
    """
    Retorna dados do usuário logado.
    """
    return current_user


@router.post("/logout")
def logout():
    """
    Logout (client-side: apenas descarta o token).
    """
    return {"message": "Logout realizado com sucesso"}