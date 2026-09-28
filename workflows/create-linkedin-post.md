# Workflow: Criar post de LinkedIn

Fluxo obrigatório para transformar uma ideia em um post publicado.

```text
Usuário / rotina diária
    ↓
🔍 Checagem anti-duplicidade (no Gmail, não só no arquivo)
    ↓
🎯 Estrategista   → produz briefing (templates/briefing.md)
    ↓
✍️ Redator        → produz post de texto único (templates/linkedin-post.md)
    ↓
✅ Revisor        → APROVADO ou REPROVADO
    │
    ├── REPROVADO → volta ao Redator com o feedback do Revisor
    │               (Redator reescreve; Revisor reavalia — repete até aprovar)
    │
    └── APROVADO ↓
📧 Publicador     → formata post + prepara e-mail de entrega
    ↓
📌 Registro confirmado em content-queue.md (com verificação de leitura)
    ↓
Usuário recebe o post pronto
```

> **Importante sobre responsabilidade das etapas 0 e 9:** os subagentes
> `estrategista`, `redator`, `revisor` e `publicador` só têm ferramentas de
> leitura (Read/Glob/Grep) — nenhum deles tem acesso ao Gmail nem grava
> arquivos. A checagem anti-duplicidade (passo 0) e a criação do rascunho +
> atualização de `content-queue.md` (passo 9) são responsabilidade de quem
> orquestra o fluxo (a sessão principal, seja você ou a rotina agendada), não de
> nenhum dos quatro agentes. Isso importa porque foi exatamente a falha em
> executar o passo 9 de forma confiável que causou conteúdo duplicado no
> passado (ver nota em `knowledge/editorial-guidelines.md`).

## Passo a passo

0. **Checagem anti-duplicidade (obrigatória, antes de acionar o Estrategista):**
   busque no Gmail por `subject:"Post pronto"` dos últimos 60 dias (ex.:
   `search_threads` com `newer_than:60d`) e compare os temas/assuntos já
   enviados com o tema que está prestes a ser gerado. Se um tema equivalente já
   foi enviado dentro da janela de reaproveitamento, **não gere de novo** — pule
   para o próximo item de `content-queue.md`, ou, se o tema veio do usuário
   diretamente, avise que já foi coberto recentemente e pergunte se ele quer
   mesmo assim.
1. **Usuário → Estrategista**: envia a ideia/tema do post (ou o item já
   selecionado de `content-queue.md` após o passo 0).
2. **Estrategista**: lê `knowledge/brand.md`, `knowledge/personas.md`,
   `knowledge/products.md`, `knowledge/linkedin-best-practices.md`; produz o
   briefing completo (`templates/briefing.md`).
3. **Estrategista → Redator**: entrega o briefing.
4. **Redator**: lê `knowledge/brand.md`, `knowledge/editorial-guidelines.md`,
   `knowledge/linkedin-best-practices.md`; escreve o post seguindo o briefing
   (`templates/linkedin-post.md`) — **sempre um único post de texto, nunca
   carrossel/slides**, independente do campo `Formato` no banco de ideias.
5. **Redator → Revisor**: entrega o post.
6. **Revisor**: roda o checklist de `knowledge/editorial-guidelines.md`
   (inclui checar que não é carrossel e que a voz está em primeira pessoa).
   - Se **REPROVADO**: retorna ao Redator com problemas encontrados e sugestões de
     melhoria. Volta ao passo 4.
   - Se **APROVADO**: segue ao passo 7.
7. **Revisor → Publicador**: entrega o post aprovado.
8. **Publicador**: lê `knowledge/linkedin-best-practices.md` e
   `templates/email.html`; formata o post final.
9. **Registro e entrega (orquestrador, não o Publicador)**: cria o rascunho no
   Gmail e **imediatamente depois** atualiza `content-queue.md` (remove de
   "Pendentes" e/ou adiciona em "Publicadas"). Em seguida, **relê o arquivo**
   para confirmar que a alteração realmente foi salva antes de considerar a
   execução concluída — se não persistiu, tenta de novo. Nunca encerre a
   execução sem essa confirmação.

## Regras do fluxo

- Nenhuma etapa pode ser pulada — incluindo o passo 0 (checagem anti-duplicidade)
  e a verificação de leitura no passo 9.
- Nenhum agente executa a responsabilidade de outro (ver limitações em cada arquivo
  de `agents/`).
- O loop de reprovação (passos 4→6) não tem limite fixo de tentativas, mas se o
  Revisor reprovar o mesmo post 3 vezes seguidas pelo mesmo motivo, o Redator deve
  sinalizar ao usuário que o briefing pode precisar ser revisto pelo Estrategista.
- Só o Publicador formata para publicação; só o Revisor aprova conteúdo.
- Todo conteúdo é um post de texto único — nunca carrossel, Reels ou Selfie,
  mesmo que a ideia de origem em `content-queue.md` sugira outro formato.
