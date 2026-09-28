---
título: Diretrizes editoriais
fonte: "[LM] Análise de tom de voz e estilo de comunicação do Leandro Miranda.pdf"
  — com uma correção: ver nota sobre pessoa gramatical abaixo.
uso: Consultado principalmente pelo Redator (ao escrever) e pelo Revisor (checklist
  de aprovação). Ver também [[brand]] para o tom de voz geral.
---

> **Nota sobre pessoa gramatical:** o documento-fonte original recomendava
> referenciar Leandro em terceira pessoa. Isso foi corrigido — quem publica os
> posts é o próprio Leandro, na conta dele. Todo conteúdo deve ser escrito em
> **primeira pessoa** ("eu conversei com...", não "Leandro conversou com...").

> **Nota sobre formato de saída:** todo conteúdo gerado por este sistema é um
> **único post de texto** para o feed do LinkedIn — nunca carrossel, slides,
> Reels ou Selfie. O banco de ideias em `content-queue.md` guarda um campo
> `Formato` herdado da pesquisa original (Carrossel, Selfie, Reels); isso é só
> contexto histórico de onde a ideia veio e deve ser ignorado como instrução de
> formato de saída. Corrigido em 2026-09-03 após rascunhos reais saírem como
> carrossel de 8 slides.

> **Nota sobre duplicação:** já houve casos reais de o mesmo tema ser gerado e
> enviado mais de uma vez em dias diferentes (um chegou a ser enviado 3 vezes),
> porque a atualização de `content-queue.md` no fim do fluxo às vezes falha
> silenciosamente. Por isso, **antes de gerar qualquer conteúdo novo**, é
> obrigatório checar o Gmail (não só o arquivo) para confirmar que o tema não
> foi enviado recentemente — ver `workflows/create-linkedin-post.md`.

> **Nota sobre jargão técnico (2026-09-03):** a persona validada
> (`Fundador-Enxuto`, ver [[personas]]) inclui setores fora de tech — advocacia,
> locação/frotas — e não pode ser tratada como público de produto/tecnologia por
> padrão. A regra antiga de "usar inglês técnico sem tradução" foi substituída
> pela regra 6 abaixo: linguagem clara por padrão, jargão só quando indispensável
> e sempre explicado.

> **Nota sobre tom de vendas (2026-09-17):** o Leandro sinalizou por e-mail, mais
> de uma vez, que posts recentes soaram "muito voltados a vendas" e "com um tom
> longe da nossa atuação". Comparando com o PDF-fonte original
> (`[LM] Análise de tom de voz...pdf`), a estrutura real analisada **nunca
> incluiu uma etapa de CTA ou menção a serviço pago** — isso foi adicionado
> depois em `templates/briefing.md` e é a causa raiz do problema. Duas mudanças
> corrigem isso: (1) a regra "Nunca fazer #5" abaixo, que forçava urgência/
> consequência em todo post, virou opcional (regra 5 revisada); (2) a regra 13
> abaixo proíbe transformar o fechamento em propaganda de serviço. CTA comercial
> explícito só existe quando o briefing define isso deliberadamente (funil
> Fundo + objetivo Converter), nunca por padrão.

# Diretrizes editoriais

Regras objetivas para escrita, derivadas do guia de replicação de estilo. Aplicam-se
a todo conteúdo de LinkedIn da LM for Business.

## Sempre fazer

1. Começar com gancho forte: dado, pergunta ou afirmação provocadora.
2. Usar bullet lists com traço (–) ou hífen — nunca marcadores gráficos elaborados.
3. Incluir uma seção **"IMPORTANTE:"** antes do fechamento, com regra/alerta/princípio
   central do tema.
4. Fechar com frase reflexiva curta (ex.: "Pense. Reflita." ou "Um abraço!").
5. Incluir `#LMforBusiness` em todas as hashtags.
6. Usar linguagem **clara, objetiva e sem jargão de produto/tecnologia** por
   padrão — a persona validada (`Fundador-Enxuto`) inclui setores fora de tech
   (advocacia, locação/frotas), então não presuma que o leitor conhece termos
   como discovery, delivery, squad, sprint, churn, NPS, PMF, roadmap, MVP.
   Prefira a versão em português simples sempre que existir uma equivalente
   clara (ex.: "validar com o cliente antes de construir" em vez de
   "discovery"). Se o termo técnico for indispensável — porque não há
   equivalente simples ou porque o post é especificamente para uma persona de
   produto/tech (`Lider-Scaleup`) — é **obrigatório explicar o que ele
   significa** na mesma frase ou logo em seguida (ex.: "discovery — a etapa de
   validar o problema com o cliente antes de construir qualquer coisa").
   Nunca deixe um termo técnico sem explicação "no ar".
7. Antecipar a objeção do leitor e refutá-la com veemência controlada.
8. Usar CAPS LOCK em 1–3 palavras-chave por post para ênfase.
9. Incluir um dado numérico (%, R$, X vezes) **quando fizer sentido e houver algo
    real ou uma estimativa pessoal honesta para citar** — não é obrigatório em
    todo post; forçar um número inventado ou vago só para "parecer dado" é o
    tipo de coisa que faz o post soar como material de vendas.
10. Usar a estrutura "Sem X → Y" para listar consequências, quando fizer sentido.
11. Manter parágrafos curtos (2–4 linhas), intercalados com listas.
12. Escrever em **primeira pessoa** ao citar experimentos/conversas reais — é o
    próprio Leandro quem publica (ex.: "Eu conversei com...", "Toda semana eu vejo
    founders...").
13. Por padrão, fechar com uma pergunta ou provocação puramente reflexiva —
    **sem citar nenhum serviço pago da LM for Business** no corpo ou no
    fechamento (ex.: nunca escrever algo como "esse é o processo que eu aplico
    na frente de Product Delivery"). Isso só muda se o briefing definir
    explicitamente um CTA comercial (ver regra do Estrategista em
    `prompts/strategist.md`) — e mesmo assim, como uma menção leve de uma frase,
    nunca um parágrafo dedicado a "vender" o serviço.

## Nunca fazer

1. Nunca usar linguagem passiva ou evasiva ("talvez", "pode ser que").
2. Nunca usar emojis — ausência total é característica da marca.
3. Nunca escrever parágrafos longos sem quebra de lista ou pergunta retórica.
4. Nunca omitir o confronto — toda publicação precisa refutar uma crença errada ou
   uma mentalidade comum.
5. Evitar forçar urgência artificial — uma consequência prática pode reforçar o
   argumento quando existir de verdade, mas não é obrigatório inventar uma
   "consequência de não agir" em todo post só para criar tensão. Revisado em
   2026-09-17: essa regra era absoluta e empurrava o tom para gatilho de
   vendas/medo; o padrão real de Leandro nem sempre tem urgência.
6. Nunca finalizar sem chamada reflexiva ou hashtags.
7. Nunca inventar dados, cases ou nomes de produtos que não constem em
   [[products]].
8. Nunca referenciar "Leandro" em terceira pessoa dentro do texto do post — quem
   fala é o próprio Leandro, em primeira pessoa.
9. Nunca produzir carrossel, slides ou qualquer formato multi-parte — sempre um
   único post de texto corrido, mesmo que `content-queue.md` sugira outro
   formato para aquela ideia.
10. Nunca gerar conteúdo sobre um tema sem antes confirmar (via busca no Gmail)
    que ele não foi enviado nos últimos 60 dias.
11. Nunca usar um termo técnico de produto/tecnologia (discovery, delivery,
    squad, sprint, churn, NPS, PMF, roadmap, MVP, entre outros) sem explicar o
    que ele significa — mesmo que pareça óbvio para quem trabalha com produto.
12. Nunca citar um serviço pago específico da LM for Business no corpo ou no
    fechamento do post como se fosse propaganda (ex.: "esse é o processo que eu
    aplico na frente de X", "é exatamente isso que a gente resolve com o
    serviço Y") — o post é conteúdo editorial, não anúncio. Só é permitido
    quando o briefing define explicitamente um CTA comercial (funil Fundo +
    objetivo Converter), e mesmo assim como menção leve, nunca como parágrafo
    de venda.

## Checklist de aderência (uso do Revisor)

- [ ] Gancho forte na primeira linha
- [ ] Confronto/quebra de crença presente
- [ ] Bullets com traço, não marcadores elaborados
- [ ] Dado numérico ou consequência prática presente **quando fizer sentido**
      (não reprovar só por ausência, se o tema não pedir)
- [ ] Seção "IMPORTANTE:" presente
- [ ] Fechamento reflexivo, sem pedido de engajamento direto
- [ ] Fechamento **não cita nenhum serviço pago como propaganda**, a menos que
      o briefing defina explicitamente CTA comercial (funil Fundo) — e mesmo
      assim, só uma menção leve, nunca um parágrafo de venda
- [ ] Hashtags incluindo `#LMforBusiness`
- [ ] Sem emojis
- [ ] Sem linguagem passiva/evasiva
- [ ] Primeira pessoa — nenhuma referência a "Leandro" em terceira pessoa no texto
- [ ] Post de texto único — sem slides, sem numeração de carrossel
- [ ] Linguagem clara, sem jargão técnico não explicado (todo termo de
      produto/tecnologia usado tem explicação junto)
- [ ] Nenhuma informação inventada sobre produtos/dados
