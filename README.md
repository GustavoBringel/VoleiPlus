# Vôlei+ — Gestão e Desenvolvimento Esportivo

Solução web/mobile para ajudar equipes e projetos de voleibol de Palmas-TO a organizar atletas, treinos, presenças e avaliações, e a acompanhar a evolução de cada atleta ao longo do tempo.

> Projeto de extensão da disciplina **Prática Extensionista I** (UFT, 2026/2).

## Sumário

- [Contexto](#contexto)
- [Problema](#problema)
- [Objetivos](#objetivos)
- [Funcionalidades](#funcionalidades)
- [Documentação](#documentação)
- [Tecnologias](#tecnologias)
- [Como executar](#como-executar)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Fluxo de trabalho](#fluxo-de-trabalho)
- [Equipe](#equipe)
- [Status](#status)

## Contexto

O Vôlei+ será desenvolvido em parceria com uma equipe, escola ou projeto social de voleibol em Palmas-TO. O público é formado por atletas (adolescentes e adultos), treinadores e responsáveis. As funcionalidades são definidas a partir das necessidades levantadas com a comunidade parceira (ver [descoberta.md](docs/descoberta.md)).

## Problema

Em muitas equipes, os dados dos atletas, a presença, o planejamento dos treinos e as avaliações ficam em anotações, planilhas ou informações dispersas. Isso dificulta o acompanhamento individual e a visualização da evolução.

**Questão norteadora:** como uma solução web e/ou mobile pode auxiliar equipes e projetos de voleibol da comunidade na organização dos treinos, no registro das atividades e no acompanhamento da evolução dos atletas?

## Objetivos

**Geral:** desenvolver e validar uma solução web e/ou mobile que auxilie equipes e projetos de voleibol na gestão dos treinamentos e no acompanhamento da evolução dos atletas.

**Específicos:**

1. Levantar as necessidades da comunidade parceira e definir os requisitos prioritários.
2. Projetar e desenvolver um MVP com cadastro de atletas/equipes, treinos, presença e avaliações.
3. Testar com usuários reais, coletar feedback e ajustar usabilidade e funcionamento.
4. Avaliar os resultados e documentar as contribuições para a comunidade e para a formação dos estudantes.

## Funcionalidades

Escopo previsto (sujeito a ajuste após o diagnóstico; detalhes em [requisitos.md](docs/requisitos.md)):

- [ ] Cadastro e login
- [ ] Cadastro de equipes
- [ ] Cadastro de atletas
- [ ] Registro de treinos
- [ ] Controle de presença
- [ ] Avaliação de fundamentos (passe, saque, ataque, bloqueio e defesa)
- [ ] Histórico de avaliações
- [ ] Visualização da evolução do atleta (gráficos)

## Documentação

| Documento                                | Conteúdo                                                                             |
| ---------------------------------------- | ------------------------------------------------------------------------------------ |
| [docs/descoberta.md](docs/descoberta.md) | Diagnóstico com a comunidade: roteiros, registros e necessidades identificadas       |
| [docs/requisitos.md](docs/requisitos.md) | Perfis, requisitos funcionais e não funcionais, regras de negócio e priorização      |
| [docs/api.md](docs/api.md)               | Rascunho do contrato entre o front-end e o back-end                                  |
| [docs/manual.md](docs/manual.md)         | Guia de uso do front-end (versão de trabalho)                                        |
| [docs/prototypes.md](docs/prototypes.md) | Fluxos e acesso ao protótipo navegável local                                         |
| [CONTRIBUTING.md](CONTRIBUTING.md)       | Guia de contribuição: branches, commits, pull requests, revisão e cuidados com dados |
| [issues.md](issues.md)                   | Backlog de issues por milestone, com responsável e critérios de aceite               |

## Tecnologias

Stack definida na issue #1 (back-end e front-end em projetos separados):

| Camada                            | Tecnologia                                      | Situação                                 |
| --------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| Back-end                          | Python com FastAPI                              | Definido                                 |
| Acesso a dados                    | SQLAlchemy e migrações com Alembic              | Definido                                 |
| Banco de dados                    | PostgreSQL                                      | Definido (plano de trabalho)             |
| Front-end                         | React com Vite                                  | Definido                                 |
| Linguagem do front-end            | JavaScript                                      | Definido                                 |
| Validação                         | Pydantic (back-end)                             | Padrão do FastAPI                        |
| Autenticação                      | JWT, com hash seguro de senha                   | Definido (biblioteca de hash a escolher) |
| Testes                            | pytest (back-end)                               | Definido                                 |
| Testes do front-end               | Vitest                                          | Definido                                 |
| Lint e formatação                 | Ruff (back-end) e ESLint + Prettier (front-end) | Definido                                 |
| Gráficos                          | Recharts                                        | Definido                                 |
| Hospedagem do front-end           | Vercel                                          | Definido                                 |
| Hospedagem do back-end e do banco | Railway                                         | Definido (configuração na issue #29)     |
| Versionamento                     | Git e GitHub                                    | Definido                                 |

O FastAPI gera a documentação da API automaticamente (OpenAPI), que serve de base para o contrato da issue #5.

## Como executar

**Pré-requisitos:** Node.js 22 e npm

**Front-end** (`frontend/`)

1. Instalar as dependências:
   ```bash
   cd frontend
   npm install
   ```
2. Copiar `.env.example` para `.env` e informar o endereço da API:
   ```bash
   cp .env.example .env
   # Editar .env com a URL da API (ex: VITE_API_URL=http://localhost:8000/api/v1)
   ```
3. Iniciar o servidor de desenvolvimento do Vite:

   ```bash
   npm run dev
   ```

   A aplicação estará disponível em `http://localhost:5173`

4. Rodar os testes:

   ```bash
   npm run test
   ```

5. Rodar o linter:

   ```bash
   npm run lint
   ```

6. Formatar o código com Prettier:

   ```bash
   npm run format
   ```

7. Build de produção:
   ```bash
   npm run build
   ```
   Os arquivos otimizados serão gerados na pasta `dist/`.

**Back-end** (`backend/`)

_EM DESENVOLVIMENTO - aguardando issue #3_

1. Criar e ativar o ambiente virtual e instalar as dependências.
2. Copiar `.env.example` para `.env` e preencher a conexão com o banco.
3. Aplicar as migrações do Alembic.
4. Iniciar a API (a documentação interativa fica em `/docs`).
5. Rodar os testes com `pytest`.

## Estrutura do repositório

```
.
├── README.md
├── CONTRIBUTING.md
├── issues.md
├── docs/
│   ├── descoberta.md
│   ├── api.md
│   ├── manual.md
│   └── requisitos.md
├── backend/     # FastAPI, SQLAlchemy e Alembic
└── frontend/    # React com Vite
```

## Fluxo de trabalho

Resumo abaixo; o passo a passo completo está no [CONTRIBUTING.md](CONTRIBUTING.md).

- Branch principal protegida: `main`.
- Cada tarefa em uma branch própria (`feat/nome`, `fix/nome`, `docs/nome`).
- Alterações entram por _pull request_, revisado pelo outro integrante.
- Mensagens de commit objetivas, de preferência no padrão _Conventional Commits_ (`feat:`, `fix:`, `docs:`).
- Tarefas acompanhadas por _Issues_ ligadas aos requisitos (ex.: `RF-05`).

## Equipe

| Nome                           | Papel                                                | GitHub                                               |
| ------------------------------ | ---------------------------------------------------- | ---------------------------------------------------- |
| Flavio Henrique Alves da Silva | Dev A: banco de dados, autenticação e API (back-end) | [@flaviohen16](https://github.com/flaviohen16)       |
| Gustavo Leite Bringel          | Dev B: telas, usabilidade e gráficos (front-end)     | [@GustavoBringel](https://github.com/GustavoBringel) |

Atividades compartilhadas (descoberta, decisões, testes com usuários e relatório final) são feitas pelos dois. O backlog completo, com a divisão por responsável, está em [issues.md](issues.md).

Orientação: professor(a) da disciplina Prática Extensionista I.
Parceiro: a definir.

## Status

Em fase de **documentação e descoberta**.

- [x] Plano de trabalho
- [ ] Diagnóstico com a comunidade parceira
- [ ] Requisitos validados
- [ ] Protótipos das telas
- [ ] MVP
- [ ] Testes com usuários
- [ ] Avaliação e relatório final

## Licença

A definir.
