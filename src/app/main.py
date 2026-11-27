"""Aplicação principal FastAPI - Vôlei+."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import auth, teams, athletes, trainings, attendances, evaluations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de startup/shutdown."""
    # Startup
    init_db()
    yield
    # Shutdown (se necessário)


app = FastAPI(
    title=settings.APP_NAME,
    description="API para gestão de equipes de voleibol - treinos, presença e avaliações",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(teams.router, prefix=settings.API_V1_PREFIX)
app.include_router(athletes.router, prefix=settings.API_V1_PREFIX)
app.include_router(trainings.router, prefix=settings.API_V1_PREFIX)
app.include_router(attendances.router, prefix=settings.API_V1_PREFIX)
app.include_router(evaluations.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """Health check / info básica."""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check para monitoramento."""
    return {"status": "healthy"}