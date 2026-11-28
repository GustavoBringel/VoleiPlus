# Guia de Contribuição — Vôlei+

Obrigado por contribuir com o Vôlei+. Este guia define como a equipe trabalha no repositório, para manter o histórico organizado e evitar retrabalho.

## Sumário

- [Princípios](#princípios)
- [Antes de começar](#antes-de-começar)
- [Fluxo de trabalho](#fluxo-de-trabalho)
- [Branches](#branches)
- [Commits](#commits)
- [Pull requests](#pull-requests)
- [Revisão de código](#revisão-de-código)
- [Issues](#issues)
- [Padrões de código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)
- [Privacidade e dados](#privacidade-e-dados)
- [Dúvidas e decisões](#dúvidas-e-decisões)

## Princípios

1. **O usuário vem primeiro.** Funcionalidades nascem de necessidades validadas com o parceiro (ver [descoberta.md](docs/descoberta.md)), não de suposições.
2. **Pequeno e frequente.** Mudanças pequenas e integradas com frequência são mais fáceis de revisar e menos arriscadas.
3. **A `develop` sempre funciona.** Nada quebrado vai para a branch principal.
4. **Tudo rastreável.** Cada mudança de código deve poder ser ligada a uma issue e a um requisito (ex.: `RF-15`).
5. **Respeito e colaboração.** Revisões criticam o código, não a pessoa.

## Antes de começar

1. Leia o [README.md](README.md), [requisitos.md](docs/requisitos.md) e [descoberta.md](docs/descoberta.md).
2. Clone o repositório e siga as instruções de execução do README.
3. Configure o Git com seu nome e e-mail:

   ```bash
   git config user.name "Seu Nome"
   git config user.email "seu@email.com"
   ```

4. Nunca versione segredos. Copie `.env.example` para `.env` e mantenha o `.env` fora do Git.

## Fluxo de trabalho

1. Escolha uma issue (ou crie uma) e atribua a você.
2. Atualize a `develop` local:

   ```bash
   git checkout develop
   git pull origin develop
   ```

3. Crie uma branch a partir de `develop`:

   ```bash
   git checkout -b feat/chamada-presenca
   ```

4. Desenvolva em commits pequenos, com testes quando aplicável.
5. Antes de abrir o PR, atualize sua branch com `develop` e resolva conflitos:

   ```bash
   git fetch origin
   git rebase origin/develop
   ```

6. Envie a branch e abra o pull request:

   ```bash
   git push -u origin feat/chamada-presenca
   ```

7. Aguarde a revisão, ajuste o que for pedido e faça o merge quando aprovado.
8. Apague a branch depois do merge.

## Branches

A `develop` é protegida: mudanças entram por pull request com ao menos uma aprovação; não se faz push direto nela.

| Prefixo | Uso | Exemplo |
|---|---|---|
| `feat/` | Nova funcionalidade | `feat/cadastro-atletas` |
| `fix/` | Correção de erro | `fix/duplicidade-presenca` |
| `docs/` | Documentação | `docs/atualiza-requisitos` |
| `refactor/` | Refatoração sem mudar comportamento | `refactor/servico-treinos` |
| `test/` | Testes | `test/avaliacoes` |
| `chore/` | Configuração, dependências, build | `chore/atualiza-dependencias` |

Use nomes curtos, em minúsculas e com hífens.

## Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/):

```
<tipo>(escopo opcional): descrição curta no imperativo

Corpo opcional explicando o porquê da mudança.

Refs: #12
```

**Tipos:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

**Exemplos:**

```
feat(presenca): registrar chamada de um treino
fix(avaliacao): validar notas fora da escala de 1 a 5
docs(requisitos): detalhar critérios de aceite de RF-19
```

**Boas práticas:**

- Um commit, uma ideia.
- Descrição com até cerca de 72 caracteres.
- Não misture formatação, refatoração e funcionalidade no mesmo commit.
- Não faça commit de arquivos gerados, dependências instaladas ou segredos.

## Pull requests

- Um PR por issue ou assunto, o menor possível.
- Título no mesmo padrão dos commits.
- Descreva o que mudou, por quê e como testar.
- Ligue à issue com `Closes #número`.
- Inclua capturas de tela em mudanças de interface.
- Abra como **Draft** se ainda estiver em andamento.

**Modelo de descrição:**

```markdown
## O que mudou
-

## Por quê
Closes #

## Como testar
1.
2.

## Checklist
- [ ] Segue os padrões do projeto
- [ ] Testes adicionados ou atualizados
- [ ] Documentação atualizada, se necessário
- [ ] Sem segredos ou dados reais de atletas
- [ ] Testado em tela de celular (se houver mudança de interface)
```

## Revisão de código

**Quem revisa:** o outro integrante da dupla aprova antes do merge. Ninguém aprova o próprio PR.

| Área | Responsável | Revisor |
|---|---|---|
| Banco de dados, autenticação e API | Flavio ([@flaviohen16](https://github.com/flaviohen16)) | Gustavo |
| Telas, usabilidade e gráficos | Gustavo ([@GustavoBringel](https://github.com/GustavoBringel)) | Flavio |

Mudanças no contrato da API (endpoints, formatos de resposta) e no modelo de dados precisam da aprovação dos dois, porque afetam as duas áreas.

**O que olhar:**

- Atende ao requisito e aos critérios de aceite?
- O código é legível e está coerente com o restante do projeto?
- Há tratamento de erros e validação de entradas?
- Há risco de segurança ou de expor dados pessoais?
- Os testes cobrem o comportamento principal?
- A interface funciona em celular?

**Combinados:**

- Responder a revisões em até 24 horas, sempre que possível.
- Comentários objetivos, com sugestão de solução.
- Distinguir o que é obrigatório do que é sugestão (por exemplo, prefixar com `sugestão:`).

## Issues

Use issues para tarefas, erros e ideias.

**Para tarefas:** título claro, requisito relacionado (`RF-xx`), critérios de aceite e responsável.

**Para erros:**

```markdown
**O que aconteceu**

**O que era esperado**

**Passos para reproduzir**
1.
2.

**Ambiente** (navegador, aparelho, versão)

**Capturas de tela ou logs**
```

**Etiquetas sugeridas:** `feature`, `bug`, `docs`, `melhoria`, `bloqueado`, `prioridade-alta`, `feedback-parceiro`.

Sugestões vindas do parceiro ou dos usuários devem receber a etiqueta `feedback-parceiro` e ser registradas também em [descoberta.md](docs/descoberta.md).

## Padrões de código

Regras gerais, válidas para o back-end e o front-end:

- Nomes de variáveis, funções e arquivos descritivos e consistentes.
- Funções curtas e com uma responsabilidade.
- Sem código comentado nem `console.log`/`print` de depuração no PR.
- Sem valores fixos de configuração no código: use variáveis de ambiente.
- Validar toda entrada do usuário no servidor, não só na interface.
- Nunca guardar senha em texto puro.
- Usar migrações para qualquer alteração do banco; não alterar o banco "na mão".
- Rodar o formatador e o linter antes do commit.

**Back-end (Python, FastAPI)**

- Usar _type hints_ nas funções e seguir o PEP 8, com Ruff para lint e formatação.
- Separar os modelos do banco (SQLAlchemy) dos esquemas de entrada e saída (Pydantic).
- Regras de negócio em funções/serviços próprios, não dentro das rotas.
- Toda alteração no banco por migração do Alembic, revisada no PR; não editar migrações já aplicadas.
- Variáveis de ambiente para configuração e segredos (`.env` fora do Git, `.env.example` no repositório).

**Front-end (React, Vite)**

- Componentes funcionais pequenos e reutilizáveis, com nomes descritivos.
- Chamadas à API concentradas em um módulo próprio, não espalhadas pelos componentes.
- JavaScript (sem TypeScript); ESLint para lint e Prettier para formatação.
- Tratar estados de carregamento, erro e lista vazia em toda tela que consome a API.
- Pensar primeiro no celular (mobile first).

**Contrato da API**

- O contrato fica na documentação OpenAPI gerada pelo FastAPI e no `docs/api.md`, se existir.
- Mudou rota ou formato de resposta? Atualize o contrato no mesmo PR, avise o outro integrante e peça a aprovação dos dois.

## Testes

- Funcionalidades novas devem vir com testes sempre que viável, ao menos para as regras de negócio (ex.: `RN-02`, presença duplicada).
- Correções de erro devem incluir um teste que falhava antes da correção.
- Rode os testes localmente antes de abrir o PR.
- Back-end: `pytest`. Front-end: Vitest e testes de componentes.
- Teste a interface em tamanho de celular, que é o uso principal na quadra.

## Documentação

Atualize a documentação na mesma mudança que altera o comportamento:

- Requisito novo ou alterado: [requisitos.md](docs/requisitos.md) (e registre a versão no histórico).
- Novo achado com o parceiro: [descoberta.md](docs/descoberta.md).
- Novo passo de instalação ou configuração: [README.md](README.md).
- Variável de ambiente nova: `.env.example`.

## Privacidade e dados

O sistema trata dados de atletas, incluindo possivelmente menores de idade.

- **Nunca** versionar dados reais de atletas, treinadores ou responsáveis.
- Usar dados fictícios em seeds, testes, capturas de tela e demonstrações.
- Não publicar fotos ou nomes de participantes sem autorização.
- Não incluir contatos, documentos ou outros dados pessoais em issues e PRs.
- Se algum dado sensível for enviado por engano, avise a equipe imediatamente e remova-o do histórico.

## Dúvidas e decisões

- Dúvidas rápidas: converse direto com a dupla.
- Decisões técnicas relevantes (stack, modelo de dados, mudança de escopo): registre em uma issue com a etiqueta `decisão` ou na seção "Decisões e pendências" de [descoberta.md](docs/descoberta.md).
- Mudanças de escopo precisam ser acordadas com o orientador e o parceiro antes de implementadas.
