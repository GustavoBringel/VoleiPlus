# Makefile - Vôlei+ API
# Uso: make <comando>

.PHONY: help install dev test lint format migrate seed run docker-build docker-up docker-down

# Variáveis
PYTHON := python
PIP := pip
UVICORN := uvicorn
ALEMBIC := alembic
PYTEST := pytest
RUFF := ruff
BLACK := black
MYPY := mypy

# Configuração padrão
ENV_FILE := .env
ifeq ($(wildcard $(ENV_FILE)),)
	ENV_FILE := .env.example
endif

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências de produção
	$(PIP) install -e .

install-dev: ## Instala dependências de desenvolvimento
	$(PIP) install -e ".[dev]"
	pre-commit install

dev: ## Inicia servidor de desenvolvimento com reload
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

run: ## Inicia servidor de produção (sem reload)
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000

# Testes
test: ## Roda todos os testes
	$(PYTEST)

test-cov: ## Roda testes com coverage
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html

test-watch: ## Roda testes em modo watch
	$(PYTEST) --watch

# Qualidade de código
lint: ## Roda linter (ruff)
	$(RUFF) check src tests

lint-fix: ## Roda linter com auto-fix
	$(RUFF) check --fix src tests

format: ## Formata código (black + ruff)
	$(BLACK) src tests
	$(RUFF) format src tests

format-check: ## Verifica formatação sem alterar
	$(BLACK) --check src tests
	$(RUFF) format --check src tests

type-check: ## Verifica tipos (mypy)
	$(MYPY) src

# Banco de dados
migrate: ## Aplica migrações (alembic upgrade head)
	$(ALEMBIC) upgrade head

migrate-create: ## Cria nova migração (uso: make migrate-create MSG="descrição")
	$(ALEMBIC) revision --autogenerate -m "$(MSG)"

migrate-down: ## Reverte última migração
	$(ALEMBIC) downgrade -1

migrate-history: ## Mostra histórico de migrações
	$(ALEMBIC) history

db-reset: ## Recria banco do zero (CUIDADO: apaga dados!)
	$(ALEMBIC) downgrade base
	$(ALEMBIC) upgrade head

seed: ## Popula banco com dados fictícios (ISSUE #27)
	$(PYTHON) -m scripts.seed

# Qualidade completa (para CI local)
check: lint format-check type-check test ## Roda todos os checks de qualidade

# Docker
docker-build: ## Build da imagem Docker
	docker build -t volei-plus-api .

docker-up: ## Sobe containers (API + Postgres)
	docker compose up -d

docker-down: ## Para containers
	docker compose down

docker-logs: ## Mostra logs dos containers
	docker compose logs -f

# Utilitários
shell: ## Abre shell Python com app carregado
	$(PYTHON) -c "from app.main import app; print('App carregado')"

check-deps: ## Verifica dependências desatualizadas
	$(PIP) list --outdated

clean: ## Limpa arquivos gerados
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/ dist/ build/ *.egg-info/