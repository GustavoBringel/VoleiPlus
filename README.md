# Vôlei+ — Gestão e Desenvolvimento Esportivo

Solução web/mobile para ajudar equipes e projetos de voleibol de Palmas-TO a organizar atletas, treinos, presenças e avaliações, e a acompanhar a evolução de cada atleta ao longo do tempo.

> Projeto de extensão da disciplina **Prática Extensionista I** (UFT, 2026/2).

---

## 📋 Sumário

- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Banco de Dados](#banco-de-dados)
- [Executando](#executando)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação](#documentação)
- [Equipe](#equipe)
- [Licença](#licença)

---

## 🛠 Tecnologias

| Camada | Tecnologia |
|--------|------------|
| **Linguagem** | Python 3.12+ |
| **Framework API** | FastAPI 0.115+ |
| **Banco de Dados** | PostgreSQL 16 |
| **ORM** | SQLAlchemy 2.0 |
| **Migrações** | Alembic |
| **Autenticação** | JWT (python-jose) + bcrypt (passlib) |
| **Validação** | Pydantic 2 |
| **Testes** | pytest + httpx |
| **Lint/Format** | Ruff + Black |
| **Type Checking** | mypy |
| **Containerização** | Docker + Docker Compose |

---

## 📦 Pré-requisitos

- **Python 3.12+** (recomendado 3.12 ou 3.13)
- **PostgreSQL 16+** (local ou via Docker)
- **Git**
- **Make** (opcional, para usar `Makefile`)

---

## ⚙️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/voleiPlus.git
cd voleiPlus
```

### 2. Crie ambiente virtual e instale dependências
```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### 3. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

---

## 🔧 Configuração

Edite o arquivo `.env` com suas configurações:

```env
# Banco de Dados (PostgreSQL)
DATABASE_URL=postgresql://volei_user:volei_pass@localhost:5432/volei_plus

# Segurança
SECRET_KEY=gere-uma-chave-secreta-forte-com-openssl-rand-base64-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Aplicação
APP_NAME=Vôlei+
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api/v1

# CORS (origens permitidas para o frontend)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

> **Dica:** Gere `SECRET_KEY` com: `openssl rand -base64 32` ou `python -c "import secrets; print(secrets.token_urlsafe(32))"`

---

## 🗄 Banco de Dados

### Opção A: PostgreSQL Local
1. Instale PostgreSQL 16+
2. Crie usuário e banco:
```sql
CREATE USER volei_user WITH PASSWORD 'volei_pass';
CREATE DATABASE volei_plus OWNER volei_user;
GRANT ALL PRIVILEGES ON DATABASE volei_plus TO volei_user;
```

### Opção B: Docker (recomendado para desenvolvimento)
```bash
# Sobe apenas o banco
docker compose up -d db

# Ou sobe tudo (API + banco)
docker compose up -d
```

### Migrações (Alembic)
```bash
# Aplica todas as migrações
alembic upgrade head

# Cria nova migração após alterar models
alembic revision --autogenerate -m "descrição da mudança"

# Reverte última migração
alembic downgrade -1

# Ver histórico
alembic history
```

---

## 🚀 Executando

### Desenvolvimento (com reload automático)
```bash
# Via Makefile
make dev

# Ou direto
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
# Via Makefile
make run

# Ou direto
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker
```bash
# Build e sobe tudo
docker compose up --build -d

# Logs
docker compose logs -f api

# Para
docker compose down
```

### Acessos
- **API**: http://localhost:8000
- **Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🧪 Testes

```bash
# Todos os testes
make test
# ou
pytest

# Com coverage
make test-cov
# ou
pytest --cov=src --cov-report=term-missing --cov-report=html

# Testes específicos
pytest tests/test_auth.py -v
pytest tests/test_business_rules.py -v

# Modo watch (re-executa ao salvar)
pytest --watch
```

### Cobertura mínima alvo: **70%**

---

## 📁 Estrutura do Projeto

```
voleiPlus/
├── .github/
│   ├── ISSUE_TEMPLATE/      # Templates de issues
│   ├── workflows/           # CI/CD (GitHub Actions)
│   └── pull_request_template.md
├── docs/
│   ├── descoberta.md        # Diagnóstico com parceiro
│   └── requisitos.md        # Requisitos funcionais e não-funcionais
├── migrations/              # Migrações Alembic
│   ├── versions/
│   │   └── 001_initial_schema.py
│   ├── env.py
│   └── script.py.mako
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py          # Dependências (DB, auth, etc)
│   │   │   └── v1/              # Rotas da API v1
│   │   │       ├── auth.py      # Login, register, token
│   │   │       ├── teams.py     # CRUD equipes
│   │   │       ├── athletes.py  # CRUD atletas
│   │   │       ├── trainings.py # CRUD treinos
│   │   │       ├── attendances.py # Presença (chamada)
│   │   │       └── evaluations.py # Avaliações + evolução
│   │   ├── core/
│   │   │   ├── config.py        # Settings (Pydantic Settings)
│   │   │   ├── security.py      # Hash senha, JWT
│   │   │   └── database.py      # SQLAlchemy engine/session
│   │   ├── models/              # Models SQLAlchemy
│   │   │   ├── user.py
│   │   │   ├── team.py
│   │   │   ├── athlete.py
│   │   │   ├── training.py
│   │   │   ├── attendance.py
│   │   │   └── evaluation.py
│   │   ├── schemas/             # Schemas Pydantic (request/response)
│   │   │   ├── user.py
│   │   │   ├── team.py
│   │   │   ├── athlete.py
│   │   │   ├── training.py
│   │   │   ├── attendance.py
│   │   │   └── evaluation.py
│   │   ├── services/            # Camada de negócio
│   │   │   ├── auth_service.py
│   │   │   ├── team_service.py
│   │   │   ├── athlete_service.py
│   │   │   ├── training_service.py
│   │   │   ├── attendance_service.py
│   │   │   └── evaluation_service.py
│   │   ├── main.py              # App FastAPI
│   │   └── __init__.py
│   └── tests/                   # Testes automatizados
│       ├── conftest.py          # Fixtures pytest
│       ├── test_auth.py
│       ├── test_teams.py
│       ├── test_athletes.py
│       ├── test_trainings.py
│       ├── test_attendances.py
│       ├── test_evaluations.py
│       └── test_business_rules.py
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore
├── alembic.ini                  # Config Alembic
├── docker-compose.yml
├── Dockerfile
├── Makefile                     # Comandos úteis
├── pyproject.toml               # Dependências e config tools
├── CONTRIBUTING.md              # Guia de contribuição
├── issues.md                    # Backlog de issues
└── README.md                    # Este arquivo
```

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [README.md](README.md) | Visão geral, instalação, execução |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guia de contribuição (branches, commits, PRs, revisão) |
| [issues.md](issues.md) | Backlog completo com milestones e responsáveis |
| [docs/descoberta.md](docs/descoberta.md) | Diagnóstico com comunidade parceira |
| [docs/requisitos.md](docs/requisitos.md) | Requisitos funcionais, não-funcionais, regras de negócio |
| [API Docs (Swagger)](http://localhost:8000/docs) | Documentação interativa da API |

---

## 👥 Equipe

| Nome | Papel | GitHub | Responsabilidades |
|------|-------|--------|-------------------|
| **Flavio Henrique Alves da Silva** | Dev A (Back-end) | [@flaviohen16](https://github.com/flaviohen16) | Banco de dados, autenticação, API, migrações, testes back-end |
| **Gustavo Leite Bringel** | Dev B (Front-end) | [@GustavoBringel](https://github.com/GustavoBringel) | Telas, usabilidade, gráficos, integração front-end |

> **Regra de ouro:** Quem desenvolve não aprova o próprio PR. O outro integrante revisa.

---

## 📄 Licença

A definir.

---

## 🤝 Contribuindo

Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para entender o fluxo de trabalho, padrões de commit, revisão de código e como abrir issues/PRs.

### Resumo rápido:
1. Escolha uma issue (ou crie uma) e atribua a você
2. Atualize `main` local: `git checkout main && git pull origin main`
3. Crie branch: `git checkout -b feat/nome-da-feature`
4. Desenvolva com commits pequenos (Conventional Commits)
5. Rode testes e lint: `make check`
6. Push e abra PR: `git push -u origin feat/nome-da-feature`
7. Aguarde revisão do colega
8. Merge após aprovação