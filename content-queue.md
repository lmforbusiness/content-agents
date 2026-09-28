# Fila de temas — rotina diária de LinkedIn

> **Correção de 2026-09-03:** esta fila teve pelo menos 3 temas enviados por
> e-mail sem nunca serem registrados aqui em "Publicadas" ("Experiência do
> cliente", "Mapear processo", "Marca forte não é logo bonito"), e um tema foi
> enviado 3 vezes em dias diferentes ("Achismo tem nome: falta de Product
> Analytics") porque essa atualização falhou silenciosamente. As linhas
> ausentes foram reconstruídas a partir do histórico real do Gmail. A partir de
> agora, a rotina também faz uma checagem direta no Gmail antes de gerar
> qualquer tema (não depende só deste arquivo) — ver
> `workflows/create-linkedin-post.md`, passo 0.

Fonte de ideias consumida pela rotina agendada `daily-linkedin-post`. A cada
execução, a rotina pega o **primeiro item numerado da seção "Pendentes"**, entrega
toda a metadata (categoria, formato, persona, serviço, gancho sugerido, estrutura)
como contexto para o Estrategista, roda o fluxo completo
(`workflows/create-linkedin-post.md`) e move o item para "Publicadas" com a data e
o link/nome do rascunho gerado.

> **Quando "Pendentes" esvaziar:** o Estrategista não para o fluxo. Ele pode
> **reaproveitar um tema da tabela "Publicadas"**, desde que não tenha sido
> publicado nos últimos **60 dias**, sempre com um ângulo, gancho ou estrutura
> diferente do já usado (nunca repete o post anterior). Ao reaproveitar, ele
> registra isso no briefing e, na tabela "Publicadas", a nova execução vira uma
> nova linha com a data atual e uma nota "(reaproveitado)".

> A seção **"Ideias reativas / oportunistas"**, no fim do arquivo, **não** é
> consumida automaticamente pela rotina sequencial — são ideias que dependem de
> notícia/contexto do momento (ex.: reagir a um case de mercado). Use-as
> manualmente quando fizer sentido.

Você pode editar esta fila a qualquer momento: reordenar, adicionar novas ideias no
fim de "Pendentes", ou remover itens.

**Fonte:** banco de ideias construído a partir do guia de tom de voz, do catálogo
de produtos, das personas e de 6 posts recentes reais do perfil do Leandro
(`ideias-linkedin-leandro-miranda.md`, colado em 2026-07-14). A ordem abaixo foi
intercalada por pilar/persona/formato em relação ao banco original — o banco
agrupava por bloco temático, o que geraria dias seguidos do mesmo assunto (ex.: 3
posts de IA em sequência); aqui os temas de IA e os institucionais foram
espaçados ao longo da fila.

Legenda de categorias: **PROCESSO** (bastidores), **DESEJO** (mostrar
autoridade/resultado), **UTILIDADE** (dica prática), **OPORTUNIDADE**
(novidade/gatilho de conversão), **OPINIÃO** (provocação/posicionamento).

Legenda de persona: `Founder-PMF`, `Lider-Scaleup`, `Investidor`.

Padrões de estilo confirmados nos 6 posts recentes reais (além do guia de tom de
voz oficial) — o Redator deve considerá-los quando o gancho sugerido pedir:
- Vocativo de abertura ocasional: "Galera!" ou "Founders:" (não em todo post).
- Recurso "[Achismo] diz X → Realidade é Y".
- Diálogo com a objeção do leitor em 1ª pessoa dirigida a Leandro: "Mas Leandro,
  preciso contratar pessoas boas para fazer... não, não, não." (o leitor
  imaginário se dirige a Leandro por nome — isso não viola a regra de primeira
  pessoa, porque quem fala nesse trecho é o leitor, não Leandro).
- Pilar recorrente forte: "negócio tradicional criando produto digital sem
  método" — variar o formato entre publicações desse pilar para não cansar a
  audiência.
- Hashtags variam entre 2 e 4 nos posts reais recentes (o padrão documentado em
  `knowledge/linkedin-best-practices.md` pede 3–5) — ao aprovar posts desse
  pilar, o Revisor pode aceitar 2 hashtags + `#LMforBusiness` sem reprovar só por
  isso.

## Pendentes

*(vazia — próximas execuções reaproveitam temas de "Publicadas" com mais de 60 dias, com ângulo novo)*

## Ideias reativas / oportunistas (uso manual — não entram na fila sequencial)

- **"Reação a case de startup que quebrou por escala mal feita"** — OPINIÃO,
  usar notícia real do mercado de tech brasileiro como gancho, sempre
  conectando à tese de governança + product discovery.
- **"Reação a lançamento de novo modelo de IA relevante"** — OPINIÃO/UTILIDADE,
  sempre trazendo de volta para "ferramenta não substitui processo".
- **"Pergunta recorrente de founder em mentoria"** — UTILIDADE, formato Reels,
  respondendo uma dúvida real recebida em DM ou mentoria (anonimizada).

## Publicadas

| Data | Tema | Serviço/ângulo relacionado |
|---|---|---|
| 2026-07-14 | Dev sênior caro não resolve falta de clareza de produto | Product Discovery |
| 2026-07-14 | Empresas usando IA sem avaliar custo, risco e governança | AI Assessment |
| 2026-07-15 | Achismo custa mais caro que discovery | Product Discovery |
| 2026-07-16 | Squad skills vêm antes do roadmap | Product Delivery |
| 2026-07-21 | Plano de Negócios não é formalidade de banco | Consultoria Empresarial — Plano de Negócios |
| 2026-07-22 | Com IA eu não preciso mais de processo estruturado | AI Product / AI Assessment |
| 2026-07-24 | Experiência do cliente e churn silencioso *(faltava aqui — reconstruído do Gmail)* | Consultoria Empresarial — Experiência do Cliente |
| 2026-07-28 | Sem Discovery → MVP errado → Dinheiro fora | Product Discovery |
| 2026-07-29 | Growth não é marketing. É produto fazendo o trabalho de vendas | Product Led Growth |
| 2026-08-03 | O que aprendi mentorando founders no Nexus Circle | Institucional / Nexus Circle-PIT-ABStartups |
| 2026-08-11 | Mapear processo não é burocracia, é economia *(faltava aqui — reconstruído do Gmail)* | Mapeamento de Processos |
| 2026-08-11 | Produto digital não é departamento, é decisão de negócio | Product Strategy |
| 2026-08-12 | Gestão de projetos não atrasa por falta de esforço | Consultoria Empresarial — Gestão de Projetos |
| 2026-08-13 | 3/4 perguntas antes de colocar IA no seu produto (checklist pré-decisão) | AI Assessment |
| 2026-08-14 | Achismo tem nome: falta de Product Analytics *(enviado de novo em 08-19 e 08-20 pelo mesmo bug — ver correção acima)* | Product Analytics |
| 2026-08-21 | Investidor também precisa de vocabulário de produto | Product Advisor |
| 2026-08-24 | Velocidade sem governança é só caos rápido | Consultoria Empresarial — Gestão de Projetos |
| 2026-08-25 | Marca forte não é logo bonito *(faltava aqui — gerado 2x em 08-25/08-26, nunca registrado; rascunhos duplicados devem ser conferidos manualmente no Gmail)* | Brand & Design |
| 2026-08-27 | O que eu pergunto antes de aprovar qualquer feature | Product Strategy |
| 2026-09-03 | Marketing e vendas remando em direções diferentes | Consultoria Empresarial — Marketing Digital e Vendas |
| 2026-09-04 | Negócio tradicional + produto digital: os 3 erros que eu mais vejo | Product Strategy / Consultoria Empresarial |
| 2026-09-08 | 3 métricas que todo founder ignora até ser tarde demais | Product Analytics |
| 2026-09-09 | O erro mais caro que vejo em projetos de IA | AI Product |
| 2026-09-11 | Gestão de pessoas não escala no achismo *(faltava aqui — item ficou esquecido em "Pendentes" mesmo após envio; reconstruído do Gmail em 2026-09-14)* | Consultoria Empresarial — Assessoria de Gestão de Pessoas |
| 2026-09-14 | Founder decide sozinho e erra caro | Product Advisor |
| 2026-09-15 | Como eu estruturo um time em 30 dias | Product Delivery |
| 2026-09-17 | O produto vende sozinho? Faça este teste | Product Led Growth |
| 2026-09-21 | MVP com IA: o que muda e o que continua igual | AI Product / Product Discovery |
| 2026-09-21 | Sua documentação de produto é um passivo, não um ativo *(faltava aqui — enviado por e-mail em 09-21, nunca registrado; reconstruído do Gmail em 2026-09-23)* | Product Delivery / Product Strategy |
| 2026-09-22 | Cultura de produto dá pra medir? | Product Delivery / Product Strategy |
| 2026-09-23 | Bastidor de um Diagnóstico: a pergunta que vem antes de qualquer entrega | Institucional / Diagnóstico — fechamento reflexivo, sem CTA comercial (CTA de venda sugerido na fila foi descartado de propósito) |
| 2026-09-24 | IA não é atalho para pular a conversa com o cliente *(item #30 da fila, "IA não é atalho para pular etapa de Produto")* | AI Product — ângulo: perguntar à IA em vez de ouvir o cliente real; contraste "IA respondeu vs. cliente disse" (sem o diálogo "Mas Leandro" usado em 07-22), fechamento reflexivo sem CTA comercial |
| 2026-09-25 | 5 anos de LM for Business: o que eu faria diferente *(item #31 da fila)* | Institucional — ângulo: erros do próprio fundador ("experiência não poupa do erro"), 5 aprendizados em primeira pessoa, fechamento reflexivo sem CTA comercial; Leandro deve confirmar os aprendizados antes de publicar |
| 2026-09-28 | Pagar caro no fornecedor não compra clareza sobre o que construir *(reaproveitado de 2026-07-14, "Dev sênior caro não resolve falta de clareza de produto")* | Product Discovery / Consultoria Empresarial — (reaproveitado, ângulo: dono de negócio tradicional — locadora, escritório, clínica — que fecha com o fornecedor de software mais caro achando que preço garante acerto; perguntas que eu faço antes de assinar; objeção "Mas Leandro..."; sem jargão, sem dado numérico, fechamento reflexivo sem CTA comercial) |

## Observação sobre a pesquisa que originou o banco de ideias

Não foi possível abrir `linkedin.com/in/leandrodmiranda` diretamente (o LinkedIn
bloqueia acesso automatizado) e a busca na web só retornou snippets antigos
(2022, fase "LM Consulting for Business"). Os padrões de estilo listados acima
vieram de 6 posts recentes reais que o usuário colou diretamente na conversa —
fonte mais confiável que a pesquisa automatizada. Se quiser um mapeamento mais
completo (últimos 3 meses, por exemplo), colar mais posts permite refinar ainda
mais este banco.
