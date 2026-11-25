# Requisitos — Vôlei+

Versão: 0.1 (rascunho inicial, a validar com o parceiro)
Origem: plano de trabalho da Prática Extensionista I e hipóteses de [descoberta.md](descoberta.md).

> Os requisitos abaixo são **propostos**. Após o diagnóstico, cada um deve ser confirmado, ajustado ou removido, e a coluna "Origem" deve apontar para a necessidade correspondente (N1, N2…).

## 1. Visão geral

O Vôlei+ permite que treinadores organizem equipes, atletas, treinos, presenças e avaliações de fundamentos, e acompanhem a evolução individual dos atletas ao longo do tempo.

## 2. Escopo

**Dentro do escopo (MVP):** autenticação, equipes, atletas, treinos, presença, avaliações de fundamentos, histórico e visualização de evolução.

**Fora do escopo (por ora):** pagamentos e mensalidades, controle de campeonatos e tabelas de jogos, estatísticas de partida (pontos, sets), chat ou mensagens, notificações push, integrações externas.

## 3. Perfis de usuário

| Perfil | Descrição | Permissões principais |
|---|---|---|
| Treinador | Responsável pela equipe; usuário principal | Gerenciar equipes, atletas, treinos, presenças e avaliações |
| Atleta | Praticante vinculado a uma equipe (opcional no MVP) | Consultar o próprio perfil, presença e evolução |
| Administrador | Mantém o sistema (a equipe de desenvolvimento) | Gerenciar usuários e dados em caso de suporte |

## 4. Requisitos funcionais

Prioridade (MoSCoW): **M** = deve ter, **S** = deveria ter, **C** = poderia ter, **W** = não agora.

### 4.1 Autenticação e acesso

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-01 | O sistema deve permitir o cadastro de usuário com nome, e-mail e senha | M | |
| RF-02 | O sistema deve permitir login e logout | M | |
| RF-03 | O sistema deve restringir funcionalidades conforme o perfil do usuário | M | |
| RF-04 | O sistema deve permitir a recuperação de senha | S | |

### 4.2 Equipes

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-05 | O treinador deve poder criar, editar e excluir equipes (nome, categoria) | M | |
| RF-06 | O treinador deve poder listar suas equipes | M | |

### 4.3 Atletas

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-07 | O treinador deve poder cadastrar atletas (nome, data de nascimento, posição) | M | |
| RF-08 | O treinador deve poder editar, inativar e listar atletas de uma equipe | M | |
| RF-09 | O treinador deve poder vincular um atleta a uma equipe | M | |
| RF-10 | O treinador deve poder buscar atletas por nome | S | |
| RF-11 | O sistema deve permitir vincular uma conta de usuário a um atleta | C | |

### 4.4 Treinos

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-12 | O treinador deve poder registrar um treino (equipe, data, tema, observações) | M | |
| RF-13 | O treinador deve poder editar e excluir treinos | M | |
| RF-14 | O sistema deve listar os treinos de uma equipe em ordem cronológica | M | |

### 4.5 Presença

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-15 | O treinador deve poder registrar a presença dos atletas em um treino | M | |
| RF-16 | O sistema deve impedir registros duplicados de presença para o mesmo atleta e treino | M | |
| RF-17 | O treinador deve poder corrigir a presença registrada | M | |
| RF-18 | O sistema deve calcular o percentual de presença por atleta e por período | S | |

### 4.6 Avaliações

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-19 | O treinador deve poder registrar uma avaliação de um atleta nos fundamentos: passe, saque, ataque, bloqueio e defesa | M | |
| RF-20 | O treinador deve poder incluir observações em uma avaliação | S | |
| RF-21 | O sistema deve manter o histórico de avaliações de cada atleta | M | |
| RF-22 | O treinador deve poder editar ou excluir uma avaliação | S | |

### 4.7 Evolução

| ID | Requisito | Prior. | Origem |
|---|---|---|---|
| RF-23 | O sistema deve exibir o perfil do atleta com dados, presença e avaliações | M | |
| RF-24 | O sistema deve exibir gráfico de evolução das notas por fundamento ao longo do tempo | S | |
| RF-25 | O sistema deve permitir comparar duas avaliações do mesmo atleta | C | |
| RF-26 | O sistema deve permitir exportar o histórico do atleta (PDF ou CSV) | C | |

## 5. Requisitos não funcionais

| ID | Categoria | Requisito | Prior. |
|---|---|---|---|
| RNF-01 | Usabilidade | A interface deve ser utilizável em celular, com a chamada concluída em poucos toques por atleta | M |
| RNF-02 | Usabilidade | Um treinador sem treinamento prévio deve conseguir registrar um treino e a presença seguindo o manual de uso | M |
| RNF-03 | Compatibilidade | Funcionar nos navegadores atuais (Chrome, Firefox, Edge, Safari) | M |
| RNF-04 | Segurança | Senhas armazenadas com hash seguro; nunca em texto puro | M |
| RNF-05 | Segurança | Comunicação protegida por HTTPS em ambiente publicado | M |
| RNF-06 | Privacidade | Coletar apenas os dados necessários e restringir o acesso a dados de atletas ao treinador responsável | M |
| RNF-07 | Desempenho | Telas principais com resposta percebida abaixo de 3 segundos em conexão móvel comum | S |
| RNF-08 | Confiabilidade | Dados preservados em caso de falha, com backup do banco no ambiente publicado | S |
| RNF-09 | Manutenibilidade | Código versionado no Git, com revisão por pull request e documentação mínima | M |
| RNF-10 | Portabilidade | Banco de dados PostgreSQL, conforme o plano de trabalho | M |
| RNF-11 | Acessibilidade | Contraste adequado e textos legíveis em tela pequena | S |

## 6. Regras de negócio

| ID | Regra |
|---|---|
| RN-01 | Um atleta pertence a uma equipe por vez. |
| RN-02 | Um atleta tem no máximo um registro de presença por treino. |
| RN-03 | As notas de avaliação seguem uma escala de 1 a 5 (a validar com o treinador). |
| RN-04 | Um treinador só acessa equipes, atletas e avaliações que ele mesmo cadastrou ou que lhe foram atribuídos. |
| RN-05 | Atletas inativados mantêm o histórico, mas não aparecem na chamada de novos treinos. |
| RN-06 | A exclusão de uma equipe com treinos registrados exige confirmação (ou é substituída por inativação). |
| RN-07 | Dados de menores de 18 anos só são coletados com autorização dos responsáveis. |

## 7. Critérios de aceite (exemplos)

**RF-15 — Registrar presença**

- Dado um treino existente com atletas na equipe, quando o treinador abre a chamada, então todos os atletas ativos da equipe aparecem listados.
- Quando o treinador marca um atleta como presente ou ausente e salva, então a presença é gravada e aparece no histórico do atleta.
- Quando o treinador tenta registrar outra presença para o mesmo atleta e treino, então o sistema atualiza o registro existente e não cria um duplicado.

**RF-19 — Registrar avaliação**

- Quando o treinador informa as notas dos cinco fundamentos e salva, então a avaliação aparece no histórico com data e avaliador.
- Quando uma nota está fora da escala permitida, então o sistema recusa o registro e mostra uma mensagem clara.

**RF-24 — Gráfico de evolução**

- Dado um atleta com duas ou mais avaliações, quando o treinador abre o perfil, então o gráfico mostra as notas de cada fundamento ao longo do tempo.
- Dado um atleta com menos de duas avaliações, então o sistema exibe uma mensagem informando que é preciso mais avaliações.

## 8. Matriz de rastreabilidade

Preencher conforme os requisitos forem validados e implementados.

| Necessidade | Requisitos | Telas | Testes | Situação |
|---|---|---|---|---|
| N1 | | | | |
| N2 | | | | |

## 9. Premissas e restrições

- O sistema será construído por uma dupla de estudantes (Flavio, no back-end, e Gustavo, no front-end) dentro do período da disciplina.
- O parceiro participará da validação e dos testes.
- A conexão de internet na quadra pode ser instável (a confirmar na descoberta).
- A hospedagem será de baixo custo ou gratuita.

## 10. Pontos em aberto

1. Escala de avaliação: notas de 1 a 5, conceitos ou outra?
2. O atleta terá acesso ao sistema ou apenas o treinador?
3. Será necessário funcionar sem internet (modo offline) na quadra?
4. Quais dados dos atletas o parceiro autoriza coletar?
5. Existem outros fundamentos ou critérios de avaliação que o treinador usa?

## 11. Histórico de versões

| Versão | Data | Alterações | Autor |
|---|---|---|---|
| 0.1 | 24/11/2026 | Rascunho inicial a partir do plano de trabalho | Flavio e Gustavo |
