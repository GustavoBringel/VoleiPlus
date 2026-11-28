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

| Documento | Conteúdo |
|---|---|
| [docs/descoberta.md](docs/descoberta.md) | Diagnóstico com a comunidade: roteiros, registros e necessidades identificadas |
| [docs/requisitos.md](docs/requisitos.md) | Perfis, requisitos funcionais e não funcionais, regras de negócio e priorização |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guia de contribuição: branches, commits, pull requests, revisão e cuidados com dados |
| [issues.md](issues.md) | Backlog de issues por milestone, com responsável e critérios de aceite |

## Tecnologias

A stack ainda está **em definição**. Tecnologias já previstas no plano de trabalho:

- Banco de dados: PostgreSQL
- Versionamento: Git e GitHub
- Interface: framework web e/ou mobile (a definir)
- Prototipação: ferramenta de design (a definir)

> Atualizar esta seção quando a decisão for tomada.

## Como executar

_A preencher quando houver código._ Esta seção deve conter:

1. Pré-requisitos (versões de runtime e banco)
2. Instalação das dependências
3. Variáveis de ambiente (copiar `.env.example` para `.env`)
4. Criação e migração do banco
5. Comando para iniciar a aplicação
6. Comando para rodar os testes

## Estrutura do repositório

```
.
├── README.md
├── CONTRIBUTING.md
├── issues.md
├── docs/
│   ├── descoberta.md
│   └── requisitos.md
└── (código-fonte, a definir conforme a stack)
```

## Fluxo de trabalho

Resumo abaixo; o passo a passo completo está no [CONTRIBUTING.md](CONTRIBUTING.md).

- Branch principal protegida: `develop`.
- Cada tarefa em uma branch própria (`feat/nome`, `fix/nome`, `docs/nome`).
- Alterações entram por _pull request_, revisado pelo outro integrante.
- Mensagens de commit objetivas, de preferência no padrão _Conventional Commits_ (`feat:`, `fix:`, `docs:`).
- Tarefas acompanhadas por _Issues_ ligadas aos requisitos (ex.: `RF-05`).

## Equipe

| Nome | Papel | GitHub |
|---|---|---|
| Flavio Henrique Alves da Silva | Dev A: banco de dados, autenticação e API (back-end) | [@flaviohen16](https://github.com/flaviohen16) |
| Gustavo Leite Bringel | Dev B: telas, usabilidade e gráficos (front-end) | [@GustavoBringel](https://github.com/GustavoBringel) |

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
