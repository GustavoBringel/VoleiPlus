# Migrações do Banco de Dados

Este diretório contém as migrações do Alembic para o Vôlei+.

## Como usar

```bash
# Ver status
alembic current

# Aplicar migrações
alembic upgrade head

# Criar nova migração (após alterar models)
alembic revision --autogenerate -m "descrição da mudança"

# Reverter última migração
alembic downgrade -1
```

## Histórico

- **001_initial_schema.py** — Criação de todas as tabelas: users, teams, athletes, trainings, attendances, evaluations