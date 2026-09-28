# Sistema de agentes — Conteúdo para LinkedIn (LM for Business)

Sistema multiagente especializado exclusivamente na criação de posts de LinkedIn,
composto por 4 agentes com responsabilidades exclusivas e uma base de conhecimento
única e compartilhada.

```text
Usuário → 🎯 Estrategista → ✍️ Redator → ✅ Revisor → 📧 Publicador
                                              │
                                    REPROVADO → volta ao Redator
```

## Estrutura

```text
agents/       Documentação completa de cada agente (objetivo, responsabilidades,
              limitações, E/S, critérios, exemplos)
prompts/      System prompt canônico de cada agente (fonte única — agents/ aponta
              para cá em vez de duplicar)
knowledge/    Base de conhecimento única, compartilhada por todos os agentes
templates/    Formatos de saída (briefing, post, e-mail)
workflows/    Fluxo obrigatório entre os agentes
config/       settings.yaml — configuração central
.claude/agents/  Subagentes reais do Claude Code, prontos para uso
```

## Como usar no Claude Code

Os 4 agentes já estão registrados em `.claude/agents/` como subagentes nativos:
`estrategista`, `redator`, `revisor`, `publicador`. Cada um lê seu prompt em
`prompts/` e a base de conhecimento em `knowledge/` antes de responder — nada fica
duplicado entre os arquivos.

Para gerar um post, basta pedir no Claude Code, por exemplo:

> "Use o fluxo de criação de post de LinkedIn para o tema: como founders confundem
> velocidade com produtividade."

O Claude Code vai acionar `estrategista` → `redator` → `revisor` → `publicador` na
ordem descrita em [`workflows/create-linkedin-post.md`](workflows/create-linkedin-post.md),
retornando ao Redator automaticamente sempre que o Revisor reprovar.

Você também pode acionar um agente isoladamente (ex.: só gerar o briefing) chamando-o
pelo nome.

> **Importante:** o Claude Code carrega o registro de subagentes no início da
> sessão. Se você criou ou editou arquivos em `.claude/agents/` durante a sessão
> atual, inicie uma nova sessão para que `estrategista`, `redator`, `revisor` e
> `publicador` fiquem disponíveis como agentes nativos.

## Teste do fluxo

[`tests/test-fluxo-completo.md`](tests/test-fluxo-completo.md) documenta uma
execução real de ponta a ponta — da ideia inicial ao e-mail de entrega —
incluindo um ciclo genuíno de reprovação e correção pelo Revisor/Redator. Use
como referência do comportamento esperado de cada agente.

## Antes de usar em produção

- **`knowledge/personas.md` é um rascunho inicial**, derivado do vocabulário da
  análise de tom de voz e do catálogo de serviços. Vale validar com dados reais de
  audiência (analytics do LinkedIn, CRM, entrevistas com clientes).
- **`knowledge/products.md` traz o catálogo real de serviços**, extraído de
  `_[LM] Apresentação comercial v.8.pdf`. A seção "Objeções comuns" ainda é
  inferida — vale refinar com objeções reais coletadas em vendas/CS.
- O tom de voz e as diretrizes editoriais (`knowledge/brand.md`,
  `knowledge/editorial-guidelines.md`, `knowledge/linkedin-best-practices.md`) vêm
  diretamente de `knowledge/[LM] Análise de tom de voz e estilo de comunicação do
  Leandro Miranda.pdf` — a fonte oficial já existente no projeto.
- Nomes de clientes/parceiros em `knowledge/products.md` só devem aparecer em
  conteúdo público com autorização de divulgação do cliente citado.

## Expansão futura

- Novo canal (ex. Instagram): duplicar apenas `linkedin-best-practices.md` como
  `instagram-best-practices.md` e ajustar os prompts — `brand.md`, `personas.md` e
  `products.md` continuam compartilhados sem alteração.
- Novo agente (ex. Analista de Performance pós-publicação): seguir o mesmo padrão
  `agents/*.md` + `prompts/*.md` + entrada no `workflows/` e em `config/settings.yaml`.
