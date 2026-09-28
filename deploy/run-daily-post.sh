#!/usr/bin/env bash
# Executa o fluxo de agentes de LinkedIn (Estrategista→Redator→Revisor→Publicador)
# em modo headless, para ser chamado pelo cron na VM Oracle Cloud.
#
# Antes de usar: ajuste PROJECT_DIR abaixo para o caminho real do projeto na VM.

set -euo pipefail

PROJECT_DIR="$HOME/lm-linkedin-content-agents"
LOG_DIR="$PROJECT_DIR/deploy/logs"
mkdir -p "$LOG_DIR"

cd "$PROJECT_DIR"

PROMPT=$(cat <<'PROMPT_EOF'
Você vai gerar o conteúdo de LinkedIn do dia para a LM for Business, executando o sistema de agentes definido neste projeto. Todos os caminhos de arquivo abaixo são relativos à raiz do projeto (diretório atual).

⚠️ Já houve incidentes reais deste fluxo: o mesmo tema foi gerado e enviado por e-mail 3 vezes em dias diferentes, e o conteúdo saiu como carrossel de slides em vez de post de texto. As instruções abaixo têm passos extras especificamente para não repetir isso — não pule nenhum deles.

0. **Checagem anti-duplicidade (obrigatória, antes de tudo):** busque no Gmail por `subject:"Post pronto"` com `newer_than:60d` (use a ferramenta de busca do conector Gmail — nome no formato `mcp__<id>__search_threads`; se estiver deferida, use ToolSearch com "gmail search threads"). Anote os temas já enviados nos últimos 60 dias.

1. Leia `workflows/create-linkedin-post.md` para relembrar o fluxo obrigatório completo (ele detalha os mesmos passos abaixo com mais contexto).

2. Leia `content-queue.md` e pegue o **primeiro item da seção "Pendentes"** cujo tema NÃO apareça na lista de temas já enviados que você levantou no passo 0. Se todos os itens de "Pendentes" já tiverem sido enviados recentemente (sinal de que o arquivo está desatualizado), ou se "Pendentes" estiver vazia, reaproveite um tema de "Publicadas" que não apareça nos últimos 60 dias tanto na tabela quanto na busca do Gmail, com ângulo diferente do já usado. Só pare e relate "nenhum tema disponível" se genuinely não sobrar nenhuma opção.

3. Execute o fluxo completo para esse tema:
   a. **Estrategista**: tente primeiro invocar o subagente `estrategista` via Task/Agent tool (sessões novas devem ter o registro de agentes carregado corretamente). Se retornar "Agent type not found" ou similar, assuma o papel manualmente: leia `prompts/strategist.md` e os arquivos de `knowledge/` que ele lista (`brand.md`, `personas.md`, `products.md`, `linkedin-best-practices.md`), e produza o briefing completo no formato de `templates/briefing.md`. O campo "Solicitante" é sempre "Leandro Miranda". Persona padrão: `Fundador-Enxuto` (ver `knowledge/personas.md`) — só use as personas secundárias de produto/tech se o tema for claramente específico disso. Se o tema veio de reaproveitamento, registre isso explicitamente no briefing (data da publicação original + o que muda no ângulo desta vez).
   b. **Redator**: mesma lógica de fallback — tente o subagente `redator`; se indisponível, leia `prompts/writer.md` e escreva o post seguindo exatamente o briefing, no formato `templates/linkedin-post.md`. Regras inegociáveis: (i) o post é escrito em primeira pessoa (é o próprio Leandro Miranda quem publica) — nunca referencie "Leandro" em terceira pessoa dentro do texto do post; (ii) o post é **sempre um único texto corrido para o feed**, nunca carrossel/slides — ignore qualquer campo `Formato: Carrossel/Selfie/Reels` em `content-queue.md`, é só contexto histórico da ideia, não instrução de formato de saída; (iii) **linguagem clara e objetiva, sem jargão de produto/tecnologia não explicado** — a persona validada inclui setores fora de tech (advocacia, frotas), então termos como discovery, delivery, squad, sprint, churn, NPS, PMF, roadmap, MVP só podem aparecer se vierem acompanhados de uma explicação curta do que significam, ou evitados em favor de uma versão simples em português.
   c. **Revisor**: tente o subagente `revisor`; se indisponível, leia `prompts/reviewer.md` e rode o checklist completo de `knowledge/editorial-guidelines.md` contra o post (gancho, confronto, bullets com traço, dado numérico, seção IMPORTANTE, fechamento reflexivo, hashtags com #LMforBusiness — 2 a 5 hashtags são aceitáveis se o tema seguir o pilar "negócio tradicional criando produto digital" —, sem emojis, sem linguagem passiva/evasiva, primeira pessoa, formato de texto único (sem slides), linguagem clara sem jargão técnico não explicado, CTA do briefing presente, nada inventado).
   d. Se **REPROVADO**, volte ao Redator com o feedback específico do Revisor e repita o ciclo até aprovar, no máximo 3 tentativas. Se não aprovar após a 3ª tentativa, pare, não crie nenhum rascunho, e relate o histórico de reprovações e o motivo.
   e. Quando **APROVADO**, assuma o papel do **Publicador**: tente o subagente `publicador`; se indisponível, leia `prompts/publisher.md`, formate o post final e valide a contagem de caracteres contra os limites de `knowledge/linkedin-best-practices.md` (recomendado 900–1500 caracteres).

4. Crie um **rascunho** de e-mail no Gmail (nunca envie de fato) com esse conteúdo:
   - Ferramenta: procure a ferramenta de criar rascunho do conector Gmail conectado (nome no formato `mcp__<id>__create_draft`). Se ela aparecer como ferramenta deferida, use ToolSearch com a query "gmail create draft" antes de chamá-la.
   - Destinatário: leandro.miranda@lmforbusiness.com.br
   - Assunto: "[LM for Business] Post pronto — " seguido de um resumo curto do tema.
   - Corpo: post formatado (texto único, sem slides, linguagem clara) + contagem de caracteres + hashtags, seguindo a estrutura de `templates/email.html`.

5. **Imediatamente depois** de criar o rascunho — isso não é opcional e é a causa da duplicação que já aconteceu: atualize `content-queue.md`. Se o tema veio de "Pendentes", remova-o de lá e adicione uma nova linha na tabela "Publicadas" com a data de hoje, o tema e o serviço/ângulo relacionado. Se veio de reaproveitamento de "Publicadas", adicione uma nova linha com a data de hoje e a nota "(reaproveitado, ângulo: <o que mudou>)" — não apague a linha original. **Depois de salvar, releia o arquivo `content-queue.md` para confirmar que a alteração realmente persistiu** (o item não deve mais aparecer em "Pendentes", e a nova linha deve aparecer em "Publicadas"). Se a releitura mostrar que a alteração não pegou, tente de novo até confirmar. Não considere a execução concluída sem essa confirmação.

6. Ao final, escreva um resumo curto: o tema do dia (novo ou reaproveitado, e de qual data original, se for o caso), se foi aprovado de primeira ou precisou de correção (e quantas rodadas), confirmação de que o rascunho foi criado no Gmail, e confirmação explícita de que a releitura de `content-queue.md` mostrou a atualização persistida — ou, se algo bloqueou o fluxo, o motivo exato.

Restrições importantes, sempre válidas:
- Nunca envie o e-mail de fato — apenas crie o rascunho.
- Nunca invente produtos, dados de mercado, clientes ou estatísticas que não constem em `knowledge/products.md` ou não estejam claramente marcados como estimativa pessoal em primeira pessoa.
- Nunca escreva o post em terceira pessoa sobre Leandro Miranda.
- Nunca produza carrossel, slides ou qualquer formato multi-parte — sempre um único post de texto.
- Nunca use jargão técnico de produto/tecnologia sem explicar o que significa — a persona validada não é majoritariamente de tech.
- Nunca pule a checagem anti-duplicidade no Gmail (passo 0) nem a releitura de confirmação (passo 5).
- Nunca marque um tema como "Publicado" em `content-queue.md` sem o rascunho de e-mail ter sido criado com sucesso, e nunca finalize a execução sem confirmar por releitura que `content-queue.md` foi realmente atualizado.
- Nunca reaproveite um tema publicado há menos de 60 dias, nem repita o mesmo ângulo/gancho de uma publicação anterior do mesmo tema.
PROMPT_EOF
)

claude -p "$PROMPT" >> "$LOG_DIR/$(date +%F).log" 2>&1
