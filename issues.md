# Backlog de Issues — Vôlei+

Backlog derivado de [requisitos.md](docs/requisitos.md), [descoberta.md](docs/descoberta.md) e [CONTRIBUTING.md](CONTRIBUTING.md). Está escrito **sem depender da stack**, então vale para qualquer tecnologia escolhida.

## Divisão da dupla

| Dev | Integrante | GitHub | Foco |
|---|---|---|---|
| **Dev A** | Flavio Henrique Alves da Silva | [@flaviohen16](https://github.com/flaviohen16) | Banco de dados, autenticação e API (back-end) |
| **Dev B** | Gustavo Leite Bringel | [@GustavoBringel](https://github.com/GustavoBringel) | Telas, usabilidade e gráficos (front-end) |
| **Ambos** | Flavio e Gustavo | | Descoberta, decisões, testes com usuários e relatório |

Nas issues, o campo **Resp.** usa o nome de quem é responsável. Regra de ouro: quem desenvolve não aprova o próprio PR; o outro revisa (ver CONTRIBUTING). Ao criar cada issue no GitHub, atribua ao usuário correspondente (`flaviohen16` ou `GustavoBringel`); nas issues "Ambos", atribua aos dois.

## Como as issues se conectam

1. **#5 (contrato da API)** é o ponto de encontro: depois dele, Gustavo pode construir telas com dados simulados enquanto Flavio implementa os endpoints.
2. Cada tela (Gustavo) depende do endpoint correspondente (Flavio) só na hora da integração.
3. Priorização: tudo marcado **M** nos requisitos entra nas milestones 1 a 3; **S** e **C** ficam no backlog final.

## Milestones

| # | Milestone | Objetivo |
|---|---|---|
| M0 | Fundação e descoberta | Repositório, decisões, parceiro, protótipos e modelo de dados |
| M1 | Acesso, equipes e atletas | Login e cadastro de equipes e atletas funcionando |
| M2 | Treinos e presença | Registro de treinos e chamada |
| M3 | Avaliações e evolução | Avaliações, histórico e gráficos |
| M4 | Validação e entrega | Testes com usuários, manual, avaliação e relatório |

## Etiquetas

`feature` · `bug` · `docs` · `chore` · `melhoria` · `decisão` · `bloqueado` · `prioridade-alta` · `feedback-parceiro` · `back-end` · `front-end` · `banco` · `ux` · `teste` · `descoberta`

## Visão geral

| # | Título | Resp. | Milestone | Requisitos |
|---|---|---|---|---|
| 1 | Definir a stack e registrar a decisão | Ambos | M0 | RNF-03, RNF-10 |
| 2 | Configurar o repositório e a organização do projeto | Flavio | M0 | RNF-09 |
| 3 | Criar a base do projeto, linter e testes automáticos | Flavio | M0 | RNF-09 |
| 36 | Criar a base do front-end, linter e testes automáticos | Gustavo | M0 | RNF-03, RNF-09 |
| 4 | Prototipar as telas do MVP | Gustavo | M0 | RNF-01, RNF-11 |
| 5 | Definir o contrato da API | Ambos | M0 | todos os RF |
| 6 | Modelar o banco de dados e criar as migrações | Flavio | M0 | RNF-10, RN-01 a RN-06 |
| 7 | Identificar o parceiro e obter autorização | Ambos | M0 | RN-07 |
| 8 | Realizar o diagnóstico com o parceiro | Ambos | M0 | descoberta |
| 9 | Consolidar achados e validar os requisitos | Ambos | M0 | requisitos |
| 10 | Autenticação: cadastro, login e logout | Flavio | M1 | RF-01, RF-02, RNF-04 |
| 11 | Controle de acesso por perfil | Flavio | M1 | RF-03, RN-04, RNF-06 |
| 12 | API de equipes | Flavio | M1 | RF-05, RF-06 |
| 13 | API de atletas | Flavio | M1 | RF-07, RF-08, RF-09, RN-01, RN-05 |
| 14 | Layout base, navegação e responsividade | Gustavo | M1 | RNF-01, RNF-03, RNF-11 |
| 15 | Telas de login e cadastro | Gustavo | M1 | RF-01, RF-02 |
| 16 | Telas de equipes | Gustavo | M1 | RF-05, RF-06 |
| 17 | Telas de atletas | Gustavo | M1 | RF-07, RF-08, RF-09 |
| 18 | API de treinos | Flavio | M2 | RF-12, RF-13, RF-14 |
| 19 | API de presença | Flavio | M2 | RF-15, RF-16, RF-17, RN-02 |
| 20 | Telas de treinos | Gustavo | M2 | RF-12, RF-13, RF-14 |
| 21 | Tela de chamada (mobile primeiro) | Gustavo | M2 | RF-15, RF-16, RF-17, RNF-01 |
| 22 | API de avaliações | Flavio | M3 | RF-19, RF-21, RN-03 |
| 23 | API de perfil, histórico e evolução do atleta | Flavio | M3 | RF-18, RF-21, RF-23 |
| 24 | Tela de avaliação de fundamentos | Gustavo | M3 | RF-19 |
| 25 | Perfil do atleta com histórico | Gustavo | M3 | RF-21, RF-23 |
| 26 | Gráficos de evolução e percentual de presença | Gustavo | M3 | RF-18, RF-24 |
| 27 | Dados fictícios para testes e demonstração | Flavio | M3 | RN-07 |
| 28 | Testes das regras de negócio e fluxos críticos | Ambos | M3 | RN-01 a RN-06 |
| 29 | Publicar o ambiente de teste (HTTPS e backup) | Flavio | M4 | RNF-05, RNF-08 |
| 30 | Escrever o manual de uso | Gustavo | M4 | RNF-02 |
| 31 | Ajustes de usabilidade e desempenho | Gustavo | M4 | RNF-02, RNF-07 |
| 32 | Testar com o parceiro e coletar feedback | Ambos | M4 | RNF-02 |
| 33 | Questionário de satisfação e indicadores | Ambos | M4 | objetivo 4 |
| 34 | Relatório final e organização das evidências | Ambos | M4 | objetivo 4 |
| 35 | Backlog opcional (S e C) | A definir | Backlog | ver lista |

---

## M0 — Fundação e descoberta

### #1 — Definir a stack e registrar a decisão
**Resp.:** Ambos · **Etiquetas:** `decisão` · **Milestone:** M0
**Descrição:** comparar opções (linguagem, framework, abordagem web ou mobile, hospedagem) considerando o que a dupla já domina, o prazo e o uso em celular na quadra. Registrar a escolha e o motivo.
**Aceite:**
- [ ] Decisão registrada em issue e refletida no README (seções Tecnologias e Como executar).
- [ ] Banco PostgreSQL confirmado.
- [ ] Definido se haverá PWA, site responsivo ou app nativo.

### #2 — Configurar o repositório e a organização do projeto
**Resp.:** Flavio · **Etiquetas:** `chore` · **Milestone:** M0 · **Req.:** RNF-09
**Descrição:** proteger a `main`, criar etiquetas e milestones deste backlog, modelos de issue e de PR conforme o CONTRIBUTING, quadro de tarefas e `.gitignore`/`.env.example`.
**Aceite:**
- [ ] `main` protegida (merge só por PR com 1 aprovação).
- [ ] Etiquetas e milestones criadas.
- [ ] Modelos de issue e PR no repositório.
- [ ] Documentos movidos para `docs/` e links conferidos.

### #3 — Criar a base do projeto, linter e testes automáticos
**Resp.:** Flavio · **Etiquetas:** `chore`, `back-end` · **Milestone:** M0 · **Req.:** RNF-09
**Depende de:** #1
**Descrição:** estrutura inicial do código, formatador, linter, execução de testes e integração contínua simples. Escopo: back-end (a base do front-end está na #36).
**Aceite:**
- [ ] Projeto roda localmente seguindo o README.
- [ ] Linter e testes executam no pull request.
- [ ] README e CONTRIBUTING atualizados com os comandos.

### #36 — Criar a base do front-end, linter e testes automáticos
**Resp.:** Gustavo · **Etiquetas:** `chore`, `front-end` · **Milestone:** M0 · **Req.:** RNF-03, RNF-09
**Depende de:** #1
**Descrição:** criar o projeto React com Vite (JavaScript) em `frontend/`, com ESLint, Prettier e Vitest, variáveis de ambiente e um ponto único para chamadas à API. A #3 cobre a base do back-end; esta cobre o front-end, e a #14 passa a depender desta.
**Aceite:**
- [x] Projeto criado em `frontend/` com Vite e React (JavaScript), rodando com `npm run dev`.
- [x] ESLint e Prettier configurados, com scripts `lint` e `format` e sem erros no código inicial.
- [x] Vitest configurado, com script `test` e ao menos um teste de exemplo passando.
- [x] `.env.example` com o endereço da API (variável com prefixo `VITE_`) e `.env` no `.gitignore`.
- [x] Módulo único para chamadas à API (ex.: `src/services/api.js`), com a URL base vinda do ambiente.
- [x] Estrutura de pastas definida (páginas, componentes, serviços) e descrita no README.
- [ ] Lint e testes do front-end rodando no CI do pull request, junto com o job do back-end da #3.
- [x] README e CONTRIBUTING atualizados com os comandos do front-end.
- [ ] Opcional: repositório conectado à Vercel com preview por pull request (ou registrado na #29).

### #4 — Prototipar as telas do MVP
**Resp.:** Gustavo · **Etiquetas:** `ux`, `front-end` · **Milestone:** M0 · **Req.:** RNF-01, RNF-11
**Descrição:** protótipos de login, painel, equipes, atletas, treinos, chamada, avaliação e perfil do atleta, com foco em celular.
**Aceite:**
- [x] Protótipo navegável no Figma (ou equivalente) com link no repositório. (Documentado em `docs/prototypes.md` como referência até criação no Figma)
- [x] Fluxo da chamada em poucos toques.
- [ ] Protótipo mostrado ao treinador e ajustado com o retorno.

### #5 — Definir o contrato da API
**Resp.:** Ambos · **Etiquetas:** `decisão`, `back-end`, `front-end` · **Milestone:** M0
**Depende de:** #1, #6
**Descrição:** listar endpoints, métodos, formatos de requisição e resposta, códigos de erro e regras de autenticação. É o acordo que permite trabalhar em paralelo.
**Aceite:**
- [ ] Documento do contrato (ex.: arquivo `docs/api.md` ou especificação OpenAPI).
- [ ] Cobre auth, equipes, atletas, treinos, presença, avaliações e perfil.
- [ ] Padrão de erros e validações definido.
- [ ] Aprovado pelos dois.

### #6 — Modelar o banco de dados e criar as migrações
**Resp.:** Flavio · **Etiquetas:** `banco`, `back-end` · **Milestone:** M0 · **Req.:** RNF-10, RN-01 a RN-06
**Descrição:** diagrama entidade-relacionamento e migrações para usuários, equipes, atletas, treinos, presenças e avaliações, incluindo restrições (presença única por atleta e treino, notas na escala).
**Aceite:**
- [ ] Diagrama no repositório.
- [ ] Migrações executam do zero em um banco vazio.
- [ ] Restrições de unicidade e de escala das notas aplicadas no banco.
- [ ] Atleta inativo mantém histórico (RN-05).

### #7 — Identificar o parceiro e obter autorização
**Resp.:** Ambos · **Etiquetas:** `descoberta` · **Milestone:** M0 · **Req.:** RN-07
**Descrição:** escolher a equipe, escola ou projeto em Palmas, apresentar a proposta e conseguir o aceite. Se houver menores, definir como obter a autorização dos responsáveis.
**Aceite:**
- [ ] Parceiro definido e preenchido na seção 4 de `descoberta.md`.
- [ ] Aceite do parceiro registrado (anexo fora do repositório público).
- [ ] Combinados dia, horário e contato.

### #8 — Realizar o diagnóstico com o parceiro
**Resp.:** Ambos · **Etiquetas:** `descoberta` · **Milestone:** M0
**Depende de:** #7
**Descrição:** executar o plano de coleta de `descoberta.md`: reunião inicial, entrevista com o treinador, observação de treino e questionário com atletas.
**Aceite:**
- [ ] Entrevista e observação realizadas e registradas na seção 6.
- [ ] Questionário aplicado e respostas guardadas.
- [ ] Hipóteses H1 a H5 marcadas como confirmadas ou descartadas.

### #9 — Consolidar achados e validar os requisitos
**Resp.:** Ambos · **Etiquetas:** `descoberta`, `docs` · **Milestone:** M0
**Depende de:** #8
**Descrição:** preencher a síntese de necessidades, ligar cada requisito à sua origem e resolver os pontos em aberto (escala de notas, acesso do atleta, modo offline, dados autorizados).
**Aceite:**
- [ ] Seção 7 de `descoberta.md` preenchida.
- [ ] Coluna "Origem" de `requisitos.md` preenchida.
- [ ] Pontos em aberto respondidos e versão 0.2 de `requisitos.md` registrada.
- [ ] Parceiro validou a lista de funcionalidades do MVP.

---

## M1 — Acesso, equipes e atletas

### #10 — Autenticação: cadastro, login e logout
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M1 · **Req.:** RF-01, RF-02, RNF-04
**Depende de:** #5, #6
**Aceite:**
- [ ] Cadastro com nome, e-mail e senha, com validação.
- [ ] Senha guardada com hash seguro.
- [ ] Login e logout funcionando, com sessão ou token.
- [ ] E-mail duplicado recusado com mensagem clara.
- [ ] Testes automáticos dos fluxos principais.

### #11 — Controle de acesso por perfil
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M1 · **Req.:** RF-03, RN-04, RNF-06
**Depende de:** #10
**Aceite:**
- [ ] Rotas protegidas exigem login.
- [ ] Treinador só acessa suas equipes, atletas e avaliações.
- [ ] Tentativa de acesso indevido retorna erro adequado.
- [ ] Testes cobrindo acesso permitido e negado.

### #12 — API de equipes
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M1 · **Req.:** RF-05, RF-06
**Depende de:** #11
**Aceite:**
- [ ] Criar, editar, listar e excluir (ou inativar) equipes.
- [ ] Exclusão com treinos exige confirmação ou vira inativação (RN-06).
- [ ] Validação de campos e testes.

### #13 — API de atletas
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M1 · **Req.:** RF-07, RF-08, RF-09, RN-01, RN-05
**Depende de:** #12
**Aceite:**
- [ ] Cadastrar, editar, listar e inativar atletas.
- [ ] Atleta vinculado a uma única equipe por vez.
- [ ] Atleta inativo some da lista ativa e preserva o histórico.
- [ ] Testes das regras RN-01 e RN-05.

### #14 — Layout base, navegação e responsividade
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end`, `ux` · **Milestone:** M1 · **Req.:** RNF-01, RNF-03, RNF-11
**Depende de:** #4, #36
**Aceite:**
- [ ] Estrutura de páginas, menu e rotas protegidas.
- [ ] Funciona em celular e computador.
- [ ] Contraste e tamanho de texto adequados.
- [ ] Estados de carregamento e de erro padronizados.

### #15 — Telas de login e cadastro
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end` · **Milestone:** M1 · **Req.:** RF-01, RF-02
**Depende de:** #14 (integração com #10)
**Aceite:**
- [ ] Formulários com validação e mensagens claras.
- [ ] Redireciona ao painel após o login.
- [ ] Logout acessível em qualquer tela.

### #16 — Telas de equipes
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end` · **Milestone:** M1 · **Req.:** RF-05, RF-06
**Depende de:** #14 (integração com #12)
**Aceite:**
- [ ] Lista, criação, edição e exclusão/inativação de equipes.
- [ ] Confirmação antes de ações destrutivas.
- [ ] Estado vazio explicativo.

### #17 — Telas de atletas
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end` · **Milestone:** M1 · **Req.:** RF-07, RF-08, RF-09
**Depende de:** #16 (integração com #13)
**Aceite:**
- [ ] Lista de atletas por equipe, cadastro, edição e inativação.
- [ ] Busca por nome, se o item opcional RF-10 já estiver incluído.
- [ ] Formulário simples e utilizável no celular.

---

## M2 — Treinos e presença

### #18 — API de treinos
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M2 · **Req.:** RF-12, RF-13, RF-14
**Depende de:** #12
**Aceite:**
- [ ] Criar, editar, excluir e listar treinos por equipe, em ordem cronológica.
- [ ] Validação de data e equipe.
- [ ] Testes automáticos.

### #19 — API de presença
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M2 · **Req.:** RF-15, RF-16, RF-17, RN-02
**Depende de:** #13, #18
**Aceite:**
- [ ] Registrar presença de vários atletas de uma vez.
- [ ] Sem duplicidade por atleta e treino (atualiza o registro existente).
- [ ] Corrigir presença já registrada.
- [ ] Só atletas ativos da equipe aparecem na chamada.
- [ ] Testes da RN-02.

### #20 — Telas de treinos
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end` · **Milestone:** M2 · **Req.:** RF-12, RF-13, RF-14
**Depende de:** #14 (integração com #18)
**Aceite:**
- [ ] Lista cronológica de treinos por equipe.
- [ ] Criação, edição e exclusão com confirmação.
- [ ] Acesso direto à chamada a partir do treino.

### #21 — Tela de chamada (mobile primeiro)
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end`, `ux` · **Milestone:** M2 · **Req.:** RF-15, RF-16, RF-17, RNF-01
**Depende de:** #20 (integração com #19)
**Aceite:**
- [ ] Lista de atletas com marcação de presente/ausente em um toque.
- [ ] Botão "marcar todos presentes" e salvar.
- [ ] Possível corrigir a chamada depois.
- [ ] Testada em tela pequena e em conexão lenta.

---

## M3 — Avaliações e evolução

### #22 — API de avaliações
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M3 · **Req.:** RF-19, RF-21, RN-03
**Depende de:** #13
**Aceite:**
- [ ] Registrar avaliação com notas de passe, saque, ataque, bloqueio e defesa.
- [ ] Notas fora da escala são recusadas com mensagem clara.
- [ ] Listar histórico por atleta, com data e avaliador.
- [ ] Observações opcionais e edição/exclusão (RF-20, RF-22), se priorizados.
- [ ] Testes de validação.

### #23 — API de perfil, histórico e evolução do atleta
**Resp.:** Flavio · **Etiquetas:** `feature`, `back-end` · **Milestone:** M3 · **Req.:** RF-18, RF-21, RF-23
**Depende de:** #19, #22
**Aceite:**
- [ ] Endpoint retorna dados do atleta, presença e avaliações.
- [ ] Série de notas por fundamento ao longo do tempo.
- [ ] Percentual de presença por período.
- [ ] Teste com atleta sem avaliações.

### #24 — Tela de avaliação de fundamentos
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end` · **Milestone:** M3 · **Req.:** RF-19
**Depende de:** #14 (integração com #22)
**Aceite:**
- [ ] Formulário com os cinco fundamentos e campo de observações.
- [ ] Validação da escala antes do envio.
- [ ] Confirmação clara de que a avaliação foi salva.

### #25 — Perfil do atleta com histórico
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end` · **Milestone:** M3 · **Req.:** RF-21, RF-23
**Depende de:** #24 (integração com #23)
**Aceite:**
- [ ] Mostra dados, presença e histórico de avaliações.
- [ ] Atalhos para nova avaliação e edição do atleta.
- [ ] Estados vazios bem explicados.

### #26 — Gráficos de evolução e percentual de presença
**Resp.:** Gustavo · **Etiquetas:** `feature`, `front-end`, `ux` · **Milestone:** M3 · **Req.:** RF-18, RF-24
**Depende de:** #25 (integração com #23)
**Aceite:**
- [ ] Gráfico de linhas por fundamento ao longo do tempo.
- [ ] Mensagem quando há menos de duas avaliações.
- [ ] Percentual de presença exibido por período.
- [ ] Legível em celular.

### #27 — Dados fictícios para testes e demonstração
**Resp.:** Flavio · **Etiquetas:** `chore`, `back-end` · **Milestone:** M3 · **Req.:** RN-07
**Aceite:**
- [ ] Script cria equipes, atletas, treinos, presenças e avaliações fictícios.
- [ ] Nenhum dado real no repositório.
- [ ] Documentado no README.

### #28 — Testes das regras de negócio e fluxos críticos
**Resp.:** Ambos · **Etiquetas:** `teste` · **Milestone:** M3
**Aceite:**
- [ ] Testes cobrindo RN-01 a RN-06.
- [ ] Fluxo completo testado: login, criar equipe, cadastrar atleta, treino, chamada, avaliação e gráfico.
- [ ] Testes rodando no CI.

---

## M4 — Validação e entrega

### #29 — Publicar o ambiente de teste (HTTPS e backup)
**Resp.:** Flavio · **Etiquetas:** `chore`, `back-end` · **Milestone:** M4 · **Req.:** RNF-05, RNF-08
**Aceite:**
- [ ] Sistema acessível por HTTPS para o parceiro.
- [ ] Variáveis de ambiente fora do código.
- [ ] Rotina de backup do banco documentada.
- [ ] Link e instruções no README.

### #30 — Escrever o manual de uso
**Resp.:** Gustavo · **Etiquetas:** `docs` · **Milestone:** M4 · **Req.:** RNF-02
**Aceite:**
- [ ] Guia curto, com capturas de tela, para o treinador.
- [ ] Cobre cadastro, treino, chamada, avaliação e evolução.
- [ ] Linguagem simples, testada com alguém que não participou do projeto.

### #31 — Ajustes de usabilidade e desempenho
**Resp.:** Gustavo · **Etiquetas:** `melhoria`, `ux` · **Milestone:** M4 · **Req.:** RNF-02, RNF-07
**Descrição:** corrigir problemas apontados nos testes e no feedback do parceiro.
**Aceite:**
- [ ] Problemas críticos de usabilidade resolvidos.
- [ ] Telas principais abrem em menos de 3 segundos em conexão móvel comum.

### #32 — Testar com o parceiro e coletar feedback
**Resp.:** Ambos · **Etiquetas:** `descoberta`, `feedback-parceiro` · **Milestone:** M4 · **Req.:** RNF-02
**Descrição:** apresentar o Vôlei+, orientar o uso, acompanhar treinos reais e registrar dificuldades e sugestões.
**Aceite:**
- [ ] Apresentação e orientação realizadas.
- [ ] Dificuldades e sugestões registradas em issues com `feedback-parceiro`.
- [ ] Treinador consegue registrar treino e chamada sozinho.

### #33 — Questionário de satisfação e indicadores
**Resp.:** Ambos · **Etiquetas:** `docs`, `descoberta` · **Milestone:** M4
**Aceite:**
- [ ] Questionário aplicado e respostas consolidadas.
- [ ] Indicadores levantados: usuários cadastrados, treinos, presenças e avaliações registradas.
- [ ] Conversa final com o treinador registrada.

### #34 — Relatório final e organização das evidências
**Resp.:** Ambos · **Etiquetas:** `docs` · **Milestone:** M4
**Aceite:**
- [ ] Relatório com contexto, problema, ação, resultados, avaliação e aprendizados.
- [ ] Evidências organizadas (atas, prints, questionários, links).
- [ ] Carga horária conferida com o limite da disciplina.
- [ ] Autoavaliação da equipe incluída.

---

## Backlog opcional

### #35 — Itens S e C dos requisitos
**Etiquetas:** `feature` · **Criar uma issue para cada item que for priorizado:**

| Requisito | Item | Resp. sugerida |
|---|---|---|
| RF-04 | Recuperação de senha | Flavio + Gustavo |
| RF-10 | Busca de atletas por nome | Flavio + Gustavo |
| RF-11 | Vincular conta de usuário ao atleta (perfil Atleta) | Flavio + Gustavo |
| RF-20 | Observações na avaliação (se não entrou na #22) | Flavio + Gustavo |
| RF-22 | Editar e excluir avaliação | Flavio + Gustavo |
| RF-25 | Comparar duas avaliações | Gustavo |
| RF-26 | Exportar histórico (PDF ou CSV) | Flavio |
| RNF-08 | Modo offline para a chamada (se o parceiro pedir) | Ambos |

---

## Ordem sugerida de execução

1. **Semana inicial:** #1, #2, #7 em paralelo; depois #3, #4, #6 e #36.
2. **Em seguida:** #5 (contrato) e #8 (diagnóstico); fechar com #9.
3. **Núcleo:** #10 e #14 em paralelo, depois #11–#13 (Flavio) e #15–#17 (Gustavo).
4. **Treinos e presença:** #18–#19 (Flavio) e #20–#21 (Gustavo).
5. **Avaliações e evolução:** #22–#23 (Flavio) e #24–#26 (Gustavo), com #27 e #28 ao final.
6. **Entrega:** #29–#34.
