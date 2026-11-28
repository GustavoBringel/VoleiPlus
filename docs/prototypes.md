# Protótipos das Telas do MVP — Vôlei+

> Documento complementar ao [issues.md](../issues.md#4--prototipar-as-telas-do-mvp) e [requisitos.md](requisitos.md).
> Este repositório contém um [protótipo navegável local](prototipo/index.html), feito com HTML, CSS e JavaScript e sem dependências. Os dados são fictícios; não há conexão com a API. As descrições abaixo registram os fluxos e critérios de interface.

## Princípios de UX

- **Mobile First**: uso principal na quadra, em celular, com uma mão.
- **Poucos toques**: ações críticas (chamada, salvar avaliação) em ≤ 3 toques.
- **Estados claros**: carregando, erro, vazio, sucesso sempre visíveis.
- **Contraste e tamanho**: mínimo WCAG AA, fontes ≥ 16px, áreas de toque ≥ 44×44px.
- **Navegação consistente**: header com título + ação principal, bottom nav nas telas principais.

---

## 1. Login e Cadastro

### Login

```
┌─────────────────────┐
│       Vôlei+        │
├─────────────────────┤
│                     │
│  E-mail             │
│  ┌───────────────┐  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  Senha              │
│  ┌───────────────┐  │
│  │ ●●●●●●●●      │  │
│  └───────────────┘  │
│                     │
│  [ Entrar        ]  │ ← Botão principal (full width)
│                     │
│  Esqueci a senha?   │ ← Link (RF-04, backlog)
│                     │
│  Não tem conta?     │
│  [ Cadastrar-se  ]  │ ← Botão secundário
└─────────────────────┘
```

### Cadastro

```
┌─────────────────────┐
│  ←  Cadastrar-se    │
├─────────────────────┤
│                     │
│  Nome completo      │
│  ┌───────────────┐  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  E-mail             │
│  ┌───────────────┐  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  Senha              │
│  ┌───────────────┐  │
│  │ ●●●●●●●●      │  │
│  └───────────────┘  │
│                     │
│  Confirmar senha    │
│  ┌───────────────┐  │
│  │ ●●●●●●●●      │  │
│  └───────────────┘  │
│                     │
│  [ Criar conta    ] │
│                     │
│  Já tem conta?      │
│  [ Entrar        ]  │
└─────────────────────┘
```

**Estados:**

- Validação inline (e-mail inválido, senhas não coincidem, e-mail já cadastrado)
- Loading no botão durante requisição
- Toast de erro/sucesso

---

## 2. Painel (Dashboard) — Página Inicial pós-login

```
┌─────────────────────┐
│  Vôlei+      ⚙️    │
├─────────────────────┤
│                     │
│  Minhas Equipes     │
│  ┌───────────────┐  │
│  │ 🏐 Equipe A   │  │ ← Card por equipe
│  │ 12 atletas    │  │
│  │ Próximo: 15/03│  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 🏐 Equipe B   │  │
│  │ 8 atletas     │  │
│  │ Próximo: 18/03│  │
│  └───────────────┘  │
│                     │
│  [ + Nova Equipe ]  │ ← FAB ou botão fixo no rodapé
│                     │
├─────────────────────┤
│  🏠  👥  📊  ⚙️    │ ← Bottom nav
└─────────────────────┘
```

**Estados:**

- Vazio: "Você ainda não tem equipes. Toque em + para criar a primeira."
- Loading: skeleton cards
- Erro: toast + botão "Tentar novamente"

---

## 3. Equipes

### Lista de Equipes (aba dentro do painel ou tela dedicada)

```
┌─────────────────────┐
│  ←  Equipes    ➕   │
├─────────────────────┤
│  🔍 Buscar equipe   │
├─────────────────────┤
│  ┌───────────────┐  │
│  │ 🏐 Falcões    │  │
│  │ Treinador: João│ │
│  │ 15 atletas    │  │
│  │ [Entrar] [⋮]  │  │ ← Ações: Entrar, Editar, Inativar
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 🏐 Águias     │  │
│  │ Treinador: Maria│ │
│  │ 10 atletas    │  │
│  │ [Entrar] [⋮]  │  │
│  └───────────────┘  │
└─────────────────────┘
```

### Criar/Editar Equipe

```
┌─────────────────────┐
│  ←  Nova Equipe     │
├─────────────────────┤
│                     │
│  Nome da equipe *   │
│  ┌───────────────┐  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  Categoria *        │
│  ┌───────────────┐  │
│  │ Sub-17 ▼      │  │ ← Select: Sub-13, Sub-15, Sub-17, Adulto, Misto
│  └───────────────┘  │
│                     │
│  Descrição          │
│  ┌───────────────┐  │
│  │               │  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  [ Cancelar ] [Salvar] │
└─────────────────────┘
```

### Confirmar Inativação/Exclusão

```
┌─────────────────────┐
│  Inativar equipe?   │
├─────────────────────┤
│                     │
│  A equipe "Falcões" │
│  será inativada.    │
│  Os treinos e       │
│  atletas ficam      │
│  preservados.       │
│                     │
│  [ Cancelar ] [Confirmar] │
└─────────────────────┘
```

---

## 4. Atletas

### Lista de Atletas (por equipe)

```
┌─────────────────────┐
│  ←  Falcões    ➕   │
├─────────────────────┤
│  🔍 Buscar atleta   │
├─────────────────────┤
│  ┌───────────────┐  │
│  │ 👤 Ana Silva  │  │
│  │ Ponteira • 16 │  │
│  │ Ativo         │  │ ← Badge: Ativo/Inativo
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 👤 Bruno Costa│  │
│  │ Levantador • 17│ │
│  │ Ativo         │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 👤 Carla Dias │  │
│  │ Líbero • 15   │  │
│  │ Inativo       │  │
│  └───────────────┘  │
└─────────────────────┘
```

### Criar/Editar Atleta

```
┌─────────────────────┐
│  ←  Novo Atleta     │
├─────────────────────┤
│                     │
│  Nome completo *    │
│  ┌───────────────┐  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  Data de nascimento *│
│  ┌───────────────┐  │
│  │ 15/03/2009 ▼  │  │ ← Date picker
│  └───────────────┘  │
│                     │
│  Posição *          │
│  ┌───────────────┐  │
│  │ Ponteira ▼    │  │ ← Select: Ponteira, Levantadora, Oposta,
│  └───────────────┘  │     Central, Líbero
│                     │
│  Número da camisa   │
│  ┌───────────────┐  │
│  │ 10            │  │
│  └───────────────┘  │
│                     │
│  [ Cancelar ] [Salvar] │
└─────────────────────┘
```

---

## 5. Treinos

### Lista de Treinos (por equipe, ordem cronológica)

```
┌─────────────────────┐
│  ←  Treinos     ➕  │
├─────────────────────┤
│  ┌───────────────┐  │
│  │ 📅 15/03/2026 │  │
│  │ 19:00 - 21:00 │  │
│  │ Quadra 2      │  │
│  │ [Chamada] [⋮] │  │ ← Acesso direto à chamada
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 📅 12/03/2026 │  │
│  │ 19:00 - 20:30 │  │
│  │ Quadra 1      │  │
│  │ [Chamada] [⋮] │  │
│  └───────────────┘  │
└─────────────────────┘
```

### Criar/Editar Treino

```
┌─────────────────────┐
│  ←  Novo Treino     │
├─────────────────────┤
│                     │
│  Data *             │
│  ┌───────────────┐  │
│  │ 15/03/2026 ▼  │  │
│  └───────────────┘  │
│                     │
│  Horário início *   │
│  ┌───────────────┐  │
│  │ 19:00 ▼       │  │
│  └───────────────┘  │
│                     │
│  Horário fim *      │
│  ┌───────────────┐  │
│  │ 21:00 ▼       │  │
│  └───────────────┘  │
│                     │
│  Local *            │
│  ┌───────────────┐  │
│  │ Quadra 2      │  │
│  └───────────────┘  │
│                     │
│  Observações        │
│  ┌───────────────┐  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  [ Cancelar ] [Salvar] │
└─────────────────────┘
```

---

## 6. Chamada (Mobile First) — **Tela Crítica**

### Lista de Atletas para Marcar Presença

```
┌─────────────────────┐
│  ←  Chamada 15/03  ✓│
├─────────────────────┤
│  Treino: 19:00-21:00│
│  Quadra 2           │
├─────────────────────┤
│  [☑ Marcar todos]   │ ← Botão secundário
├─────────────────────┤
│  ┌───────────────┐  │
│  │ 👤 Ana Silva  │  │
│  │ ☑ Presente    │  │ ← Toggle grande, toque único
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 👤 Bruno Costa│  │
│  │ ☐ Ausente     │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 👤 Carla Dias │  │
│  │ ☐ Ausente     │  │ ← Inativo não aparece (RN-02)
│  └───────────────┘  │
├─────────────────────┤
│  [ Salvar chamada  ]│ ← Botão principal (full width, destaque)
└─────────────────────┘
```

### Confirmação de Salvamento

```
┌─────────────────────┐
│  ✓  Chamada salva!  │
├─────────────────────┤
│                     │
│  12 presentes       │
│  3 ausentes         │
│                     │
│  [ Fechar ]         │
└─────────────────────┘
```

### Corrigir Chamada (após salva)

- Mesma tela, mas com dados pré-preenchidos
- Botão "Atualizar chamada" em vez de "Salvar"

**Requisitos críticos:**

- ✓ Marcar todos presentes em 1 toque
- ✓ Toggle presença/ausência em 1 toque por atleta
- ✓ Atletas inativos não aparecem
- ✓ Sem duplicidade (RN-02): atualiza registro existente
- ✓ Funciona offline (RNF-08, backlog) — sincroniza quando voltar

---

## 7. Avaliação de Fundamentos

### Formulário de Avaliação

```
┌─────────────────────┐
│  ←  Avaliar Ana   ✓ │
├─────────────────────┤
│  Data: 15/03/2026   │
├─────────────────────┤
│  Passe      ★★★★☆   │ ← Rating 1-5 (chips ou estrelas)
│  [1] [2] [3] [4] [5]│
│                     │
│  Saque      ★★★☆☆   │
│  [1] [2] [3] [4] [5]│
│                     │
│  Ataque     ★★★★☆   │
│  [1] [2] [3] [4] [5]│
│                     │
│  Bloqueio   ★★☆☆☆   │
│  [1] [2] [3] [4] [5]│
│                     │
│  Defesa     ★★★★☆   │
│  [1] [2] [3] [4] [5]│
│                     │
│  Observações        │
│  ┌───────────────┐  │
│  │ Melhorou no   │  │
│  │ passe...      │  │
│  └───────────────┘  │
│                     │
│  [ Cancelar ] [Salvar] │
└─────────────────────┘
```

**Validação:** todos os 5 fundamentos obrigatórios, escala 1-5 (RN-03)

---

## 8. Perfil do Atleta com Histórico

```
┌─────────────────────┐
│  ←  Ana Silva       │
├─────────────────────┤
│  👤 Ana Silva       │
│  Ponteira • 16 anos │
│  Camisa: 10         │
│  Status: Ativo      │
├─────────────────────┤
│  [Nova Avaliação]   │ ← Botão principal
│  [Editar Atleta]    │ ← Botão secundário
├─────────────────────┤
│  📊 Evolução        │
│  ┌───────────────┐  │
│  │   Gráfico     │  │ ← Mini gráfico ou link para tela
│  │   de linhas   │  │     dedicada (#26)
│  └───────────────┘  │
│                     │
│  📅 Presença: 85%   │ ← Percentual do período
│  (últimos 30 dias)  │
├─────────────────────┤
│  📝 Histórico       │
│  ┌───────────────┐  │
│  │ 15/03 ★★★★☆   │  │
│  │ Passe: 4      │  │
│  │ Saque: 3      │  │
│  │ ...           │  │
│  │ [Ver] [⋮]     │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ 08/03 ★★★☆☆   │  │
│  │ ...           │  │
│  └───────────────┘  │
│                     │
│  [Ver todas]        │
└─────────────────────┘
```

**Estados vazios:**

- Sem avaliações: "Nenhuma avaliação registrada. Toque em 'Nova Avaliação' para começar."
- Sem presença: "Nenhum treino com chamada registrada."

---

## 9. Gráficos de Evolução (Tela Dedicada)

```
┌─────────────────────┐
│  ←  Evolução: Ana  │
├─────────────────────┤
│  Período: [30d ▼]   │ ← Select: 30d, 90d, 1a, Personalizado
├─────────────────────┤
│  📈 Passe           │
│  ┌───────────────┐  │
│  │   ╭─╮         │  │ ← Gráfico de linhas
│  │  ╱   ╲        │  │    Eixo X: datas das avaliações
│  │ ╱     ╲       │  │    Eixo Y: nota 1-5
│  └───────────────┘  │
│                     │
│  📈 Saque           │
│  ┌───────────────┐  │
│  │     ╭─╮       │  │
│  │   ╱    ╲      │  │
│  └───────────────┘  │
│                     │
│  ... (Ataque, Bloqueio, Defesa) │
│                     │
│  📊 Presença: 85%   │ ← Card de resumo
│                     │
│  ℹ️ Mínimo 2 avaliações para mostrar tendência │
└─────────────────────┘
```

**Mensagem para poucos dados:**

```
┌─────────────────────┐
│  📈 Passe           │
├─────────────────────┤
│                     │
│  ℹ️ São necessárias │
│  pelo menos 2      │
│  avaliações para   │
│  exibir o gráfico. │
│                     │
│  [Nova Avaliação]   │
│                     │
└─────────────────────┘
```

---

## Navegação Global (Bottom Nav)

```
┌─────────────────────┐
│                     │
│      Conteúdo       │
│                     │
├─────────────────────┤
│  🏠  👥  📊  ⚙️    │
│  Início Equipes    │
│  Evolução Config   │
└─────────────────────┘
```

- **Início (🏠)**: Dashboard com resumo das equipes
- **Equipes (👥)**: Lista/gerenciamento de equipes e atletas
- **Evolução (📊)**: Gráficos e relatórios (quando houver dados)
- **Configurações (⚙️)**: Perfil, logout, preferências

---

## Fluxos Principais (User Journeys)

### Fluxo 1: Primeira vez (Onboarding)

1. Abre app → Tela de Login
2. "Não tem conta?" → Cadastro
3. Preenche dados → Cria conta
4. Login automático → Dashboard vazio
5. "+ Nova Equipe" → Cria equipe
6. "+ Novo Atleta" → Cadastra atletas
7. "+ Novo Treino" → Agenda treino
8. "Chamada" → Registra presença

### Fluxo 2: Dia de Treino (Uso Recorrente)

1. Abre app → Dashboard
2. Toca na equipe → Lista de treinos
3. Toca em "Chamada" no treino de hoje
4. "Marcar todos presentes" (ou individual)
5. "Salvar chamada" → Confirmação
6. (Opcional) Toca em atleta → "Nova Avaliação"

### Fluxo 3: Acompanhamento de Evolução

1. Abre app → Dashboard
2. Toca na equipe → Lista de atletas
3. Toca no atleta → Perfil com histórico
4. Toca em "Ver evolução" → Gráficos
5. Altera período → Atualiza gráficos

---

## Próximos Passos

1. [x] Criar protótipo navegável equivalente no repositório
2. [x] Compartilhar o caminho do protótipo neste documento
3. [ ] Apresentar ao treinador parceiro
4. [ ] Coletar feedback e ajustar
5. [ ] Validar fluxos críticos (especialmente **Chamada**)

---

## Link do protótipo navegável

Abra [`docs/prototipo/index.html`](prototipo/index.html) diretamente no navegador. Para revisar o fluxo, use **Equipes → Atletas → Avaliar** ou **Treinos → Fazer chamada**. Os nomes e dados exibidos são fictícios.
