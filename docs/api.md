# Contrato da API Vôlei+

**Versão do rascunho:** 0.2 · **Base:** `http://localhost:8000/api/v1`  
**Estado:** alinhado às rotas e schemas da branch `backend`; aguarda aprovação de Flavio e Gustavo antes de ser considerado contrato fechado.

Todas as rotas funcionais exigem `Authorization: Bearer <access_token>`, exceto cadastro e login. Os corpos e respostas usam JSON. Datas são strings ISO 8601 (`YYYY-MM-DD`); timestamps incluem fuso horário.

## Autenticação

| Método e rota         | Entrada                           | Resposta                                               | Observações                                               |
| --------------------- | --------------------------------- | ------------------------------------------------------ | --------------------------------------------------------- |
| `POST /auth/register` | `{ "name", "email", "password" }` | `201` com usuário                                      | Senha com 8–100 caracteres. Cadastro não cria token.      |
| `POST /auth/login`    | `{ "email", "password" }`         | `200` com `{ "access_token", "token_type": "bearer" }` | Token JWT. Credenciais inválidas: `401`.                  |
| `GET /auth/me`        | —                                 | `200` com usuário autenticado                          | Requer bearer token.                                      |
| `POST /auth/logout`   | —                                 | `200` com `{ "message" }`                              | O cliente descarta o token; o servidor não mantém sessão. |

Usuário: `id`, `name`, `email`, `role`, `is_active`, `created_at`, `updated_at`.

## Equipes

| Método e rota             | Entrada                                          | Resposta                                               |
| ------------------------- | ------------------------------------------------ | ------------------------------------------------------ |
| `POST /teams`             | `{ "name", "category" }`                         | `201` equipe criada                                    |
| `GET /teams`              | —                                                | Lista das equipes do treinador, com `athletes_count`   |
| `GET /teams/{team_id}`    | —                                                | Equipe                                                 |
| `PUT /teams/{team_id}`    | Campos opcionais `name`, `category`, `is_active` | Equipe atualizada                                      |
| `DELETE /teams/{team_id}` | —                                                | `204`; exclui ou inativa conforme as regras do serviço |

Equipe: `id`, `name`, `category`, `coach_id`, `is_active`, `created_at`, `updated_at`.

## Atletas

| Método e rota                                     | Entrada                                                                   | Resposta                                                                                           |
| ------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `POST /athletes`                                  | `{ "team_id", "name", "birth_date", "position?" }`                        | `201` atleta criado                                                                                |
| `GET /athletes?team_id=&active_only=true&search=` | Filtros opcionais                                                         | Lista de atletas                                                                                   |
| `GET /athletes/{athlete_id}`                      | —                                                                         | Atleta com contagens e percentual de presença                                                      |
| `GET /athletes/{athlete_id}/profile`              | —                                                                         | Perfil com equipe, presenças e avaliações; a implementação atual ainda retorna essas listas vazias |
| `PUT /athletes/{athlete_id}`                      | Campos opcionais `name`, `birth_date`, `position`, `is_active`, `team_id` | Atleta atualizado                                                                                  |
| `DELETE /athletes/{athlete_id}`                   | —                                                                         | `204`; inativa o atleta e preserva o histórico                                                     |

## Treinos

| Método e rota                     | Entrada                                    | Resposta                      |
| --------------------------------- | ------------------------------------------ | ----------------------------- |
| `POST /trainings`                 | `{ "team_id", "date", "theme", "notes?" }` | `201` treino criado           |
| `GET /trainings?team_id=`         | `team_id` opcional                         | Lista cronológica             |
| `GET /trainings/{training_id}`    | —                                          | Treino com resumo de presença |
| `PUT /trainings/{training_id}`    | Campos opcionais `date`, `theme`, `notes`  | Treino atualizado             |
| `DELETE /trainings/{training_id}` | —                                          | `204`                         |

## Presenças

| Método e rota                                          | Entrada                                                                          | Resposta                                |
| ------------------------------------------------------ | -------------------------------------------------------------------------------- | --------------------------------------- |
| `POST /attendances`                                    | `{ "training_id", "athlete_id", "present" }`                                     | `201` presença criada/atualizada        |
| `POST /attendances/bulk`                               | `{ "training_id", "attendances": [{ "training_id", "athlete_id", "present" }] }` | `{ "training_id", "saved", "updated" }` |
| `GET /attendances/training/{training_id}`              | —                                                                                | Lista de presenças do treino            |
| `PUT /attendances/{training_id}/athletes/{athlete_id}` | `{ "present" }`                                                                  | Presença corrigida                      |
| `GET /attendances/athlete/{athlete_id}/stats`          | —                                                                                | Estatísticas de presença                |

O serviço faz upsert para evitar duplicidade por atleta e treino.

## Avaliações e evolução

| Método e rota                                     | Entrada                                                                                                        | Resposta                                     |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `POST /evaluations`                               | `{ "athlete_id", "pass_rating", "serve_rating", "attack_rating", "block_rating", "defense_rating", "notes?" }` | `201` avaliação criada                       |
| `GET /evaluations/athlete/{athlete_id}`           | —                                                                                                              | Histórico do atleta                          |
| `GET /evaluations/athlete/{athlete_id}/evolution` | —                                                                                                              | Série de avaliações e percentual de presença |
| `PUT /evaluations/{evaluation_id}`                | Campos opcionais de nota e `notes`                                                                             | Avaliação atualizada                         |
| `DELETE /evaluations/{evaluation_id}`             | —                                                                                                              | `204`                                        |

Cada nota deve ser um inteiro de 1 a 5. Avaliação: `id`, `athlete_id`, `evaluator_id`, cinco notas, `notes`, `date`, `created_at`, `updated_at`.

## Erros e validação

| Código | Uso                                                                          |
| ------ | ---------------------------------------------------------------------------- |
| `400`  | Regra de negócio recusou a operação                                          |
| `401`  | Token ausente/inválido ou credenciais inválidas                              |
| `403`  | Perfil sem permissão                                                         |
| `404`  | Registro inexistente ou fora do escopo do treinador                          |
| `422`  | Corpo ou parâmetros inválidos; `detail` contém a lista de campos e mensagens |

Formato comum: `{ "detail": "mensagem" }`. Para validação do FastAPI, `detail` é uma lista com `loc`, `msg` e `type` por campo.

## Pontos a confirmar entre os dois lados

- Aprovar o contrato antes da integração das telas.
- Completar o conteúdo de `/athletes/{athlete_id}/profile` para retornar o histórico real.
- Confirmar se `GET /attendances/athlete/{athlete_id}/stats` terá filtros de período; hoje não recebe parâmetros.
- Confirmar se o logout continuará sendo apenas no cliente.
