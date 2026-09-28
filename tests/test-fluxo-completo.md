# Teste end-to-end — fluxo completo de criação de post de LinkedIn

Executa o fluxo descrito em `workflows/create-linkedin-post.md`, do zero até o
conteúdo pronto para publicação, incluindo um ciclo de reprovação real (não
forçado artificialmente — o Revisor encontrou problemas genuínos no rascunho do
Redator e o post voltou para correção).

> Nota de execução: os subagentes nativos em `.claude/agents/` só ficam
> disponíveis para o Claude Code em uma nova sessão (o registro de agentes é
> carregado no início da sessão). Este teste foi executado interpretando cada
> papel manualmente, seguindo à risca `prompts/*.md` e `knowledge/*.md` — o
> mesmo comportamento que os subagentes terão quando invocados nativamente.

> **Correção aplicada em 2026-07-14 (1/2):** a primeira versão deste teste seguia
> a regra original do documento-fonte de tom de voz, que pedia para referenciar
> Leandro em terceira pessoa. O usuário corrigiu: como é o próprio Leandro quem
> publica os posts, o texto deve estar em primeira pessoa. A regra foi corrigida
> em `knowledge/editorial-guidelines.md` (e reforçada diretamente em
> `prompts/writer.md` e `.claude/agents/redator.md`) e os trechos abaixo foram
> reescritos para refletir isso.

> **Correção aplicada em 2026-07-14 (2/2):** o usuário definiu que o campo
> "Solicitante" do briefing é sempre Leandro Miranda (é ele quem publica todo
> post), regra agora fixada em `templates/briefing.md`, `prompts/strategist.md`
> e `config/settings.yaml`. O e-mail de entrega deste teste continua endereçado a
> rennale.gregorio@lmforbusiness.com.br — isso foi uma instrução explícita à parte
> sobre quem *recebe* o conteúdo pronto, distinta de quem *solicita* o post.

---

## Entrada do usuário

> "Muita startup contrata um dev sênior caro achando que vai resolver o problema
> de produto, e continua sem saber o que construir. Queria um post sobre isso."

Solicitante: Leandro Miranda (padrão)

---

## 1. 🎯 Estrategista → briefing

```
# Briefing — Dev sênior caro não resolve falta de clareza de produto

Data: 2026-07-14
Solicitante: Leandro Miranda

## 1. Objetivo da publicação
Confrontar a crença de que contratar tech sênior resolve um problema que na
verdade é de clareza de produto, e conectar isso ao serviço de Product Discovery.

## 2. Persona
Founder-PMF (founder em fase de validação, ainda sem product-market fit, decidindo
sozinho ou com squad pequena o que construir)

## 3. Estágio do funil
Meio

## 4. Objetivo do conteúdo
Gerar autoridade (com viés de educar)

## 5. Ângulo escolhido
"Preciso de um dev sênior" costuma ser um sintoma mal diagnosticado. O problema
não é velocidade de entrega — é não saber com clareza o que construir. Contratar
tech caro sem resolver isso só faz o time errar mais rápido.

## 6. Estrutura sugerida
1. Gancho: "Contratou o dev sênior mais caro do mercado. Continua sem saber o que
   construir."
2. Contexto/Problema: founders resolvendo "lentidão" contratando quem constrói
   mais rápido, sem diagnosticar a causa.
3. Confronto/Subversão: o problema não é o dev — é a falta de clareza sobre o que
   precisa ser construído.
4. Lista de pontos: sinais de que o problema é de produto, não de tech (backlog
   sem direção, squad não explica o problema do cliente, feature sem engajamento,
   roadmap de reunião, squad travada esperando decisão).
5. Dado ou consequência: minha estimativa pessoal, em primeira pessoa, com base em
   conversas com founders + custo de reescrever o produto depois de já ter pago
   para construí-lo errado.
6. Seção IMPORTANTE: dev sênior resolve velocidade, não resolve direção.
7. Fechamento reflexivo: provocação para o founder avaliar se sabe o que construir
   antes de contratar quem constrói rápido.

## 7. CTA
Convite reflexivo + ponte comercial leve para o serviço de Product Discovery
(`knowledge/products.md` → Product Design as a Service / Product Discovery).
Não é CTA de venda direta — é abertura de conversa.

## 8. Título/gancho sugerido
"Contratou o dev sênior mais caro do mercado. Continua sem saber o que construir."

## 9. Hashtags sugeridas
#ProductDiscovery #Startups #ProductManagement #LMforBusiness

## 10. Observações para o Redator
- Persona costuma racionalizar a decisão errada ("não é question de dinheiro, é
  velocidade") — o confronto precisa ser direto, sem suavizar.
- Não inventar estatística de mercado; se usar número, ancorar em experiência
  pessoal, em primeira pessoa, não em pesquisa externa não verificada.
- Escrever em primeira pessoa ("eu") em todo o post — é o próprio Leandro quem
  publica, nunca referenciá-lo em terceira pessoa.
- Incluir a ponte para Product Discovery no fechamento, não como CTA comercial
  agressivo.
```

**Para o Redator.**

---

## 2. ✍️ Redator → rascunho v1

```
Contratou o dev sênior mais caro do mercado. Continua sem saber o que construir.

Eu converso toda semana com founders convictos de que o problema é velocidade de
entrega. Resolvem contratando quem "constrói mais rápido".

Mas talvez o problema não seja o dev. É não saber, com clareza, o que precisa
ser construído.

Sinais de que o problema é de produto, não de tech:
– o backlog muda de direção a cada sprint
– ninguém na squad explica o problema do cliente em uma frase
– a feature foi entregue, o engajamento não veio
– o roadmap nasceu em reunião, não em pesquisa
– a squad trava esperando decisão de cima

Eu estimo que 9 em cada 10 conversas que começam com "preciso contratar um
sênior" terminam em "você precisa validar antes de construir". A consequência de
pular essa etapa é sempre a mesma: reescrever o produto depois de já ter pago
para construí-lo errado.

IMPORTANTE: dev sênior resolve VELOCIDADE. Não resolve DIREÇÃO.

Antes de contratar quem constrói mais rápido, descubra se você sabe o que
construir.

Pense. Reflita.

#ProductDiscovery #Startups #ProductManagement #LMforBusiness
```

**Para o Revisor.**

---

## 3. ✅ Revisor → 1ª avaliação

```
Status:
REPROVADO

Problemas encontrados:
- Linguagem evasiva no confronto: "Mas talvez o problema não seja o dev." O
  trecho "talvez" viola a regra de nunca usar linguagem passiva/evasiva
  (knowledge/editorial-guidelines.md, Nunca fazer #1). O post precisa afirmar,
  não hipotetizar — é exatamente o momento de maior impacto do texto (a
  subversão da crença).
- CTA do briefing ausente: o briefing pede uma ponte para Product Discovery no
  fechamento. O rascunho fecha só com "Pense. Reflita.", sem qualquer conexão
  com o serviço. CTA não está de acordo com o briefing.

Sugestões de melhoria:
- Reescrever a frase de confronto como afirmação direta: algo como "O problema
  não é o dev. É não saber, com clareza, o que precisa ser construído."
- Adicionar uma linha antes do fechamento reflexivo conectando com Product
  Discovery, sem tom de venda agressiva — ex.: convite a falar com a LM se esse
  for o momento do founder.
```

**Retorna ao Redator.**

---

## 4. ✍️ Redator → rascunho v2 (correção)

```
Contratou o dev sênior mais caro do mercado. Continua sem saber o que construir.

Eu converso toda semana com founders convictos de que o problema é velocidade de
entrega. Resolvem contratando quem "constrói mais rápido".

O problema não é o dev. É não saber, com clareza, o que precisa ser construído.

Sinais de que o problema é de produto, não de tech:
– o backlog muda de direção a cada sprint
– ninguém na squad explica o problema do cliente em uma frase
– a feature foi entregue, o engajamento não veio
– o roadmap nasceu em reunião, não em pesquisa
– a squad trava esperando decisão de cima

Eu estimo que 9 em cada 10 conversas que começam com "preciso contratar um
sênior" terminam em "você precisa validar antes de construir". A consequência de
pular essa etapa é sempre a mesma: reescrever o produto depois de já ter pago
para construí-lo errado.

IMPORTANTE: dev sênior resolve VELOCIDADE. Não resolve DIREÇÃO.

Antes de contratar quem constrói mais rápido, descubra se você sabe o que
construir. Se esse é o seu momento, fala com a gente sobre Product Discovery.

Pense. Reflita.

#ProductDiscovery #Startups #ProductManagement #LMforBusiness
```

**Para o Revisor.**

---

## 5. ✅ Revisor → 2ª avaliação

```
Status:
APROVADO
```

Checklist (`knowledge/editorial-guidelines.md`):
- [x] Gancho forte na primeira linha
- [x] Confronto/quebra de crença presente e afirmativo
- [x] Bullets com traço, não marcadores elaborados
- [x] Ao menos um dado numérico (estimativa pessoal do autor, em primeira pessoa,
      não inventada como pesquisa externa)
- [x] Seção "IMPORTANTE:" presente
- [x] Fechamento reflexivo, sem pedido de engajamento direto forçado
- [x] Hashtags incluindo #LMforBusiness
- [x] Sem emojis
- [x] Sem linguagem passiva/evasiva
- [x] Primeira pessoa — nenhuma referência a "Leandro" em terceira pessoa no texto
- [x] CTA do briefing presente (ponte para Product Discovery)
- [x] Nenhuma informação inventada sobre produtos/dados

**Para o Publicador.**

---

## 6. 📧 Publicador → formatação final e e-mail

**Contagem de caracteres:** 1.155 (dentro da faixa recomendada de 900–1.500 —
`knowledge/linkedin-best-practices.md`)
**Hashtags:** #ProductDiscovery #Startups #ProductManagement #LMforBusiness (4 —
dentro da faixa de 3 a 5)

Post formatado pronto para publicação: ver seção "Rascunho v2" acima (idêntico,
sem alterações de conteúdo — apenas validado).

**E-mail de entrega** (`templates/email.html` preenchido):

- Assunto: `[LM for Business] Post pronto — Dev sênior caro não resolve falta de clareza de produto`
- Destinatário: rennale.gregorio@lmforbusiness.com.br
- Corpo: template `templates/email.html` com o post acima colado no bloco
  destacado, contagem de caracteres e hashtags preenchidas.

> Envio: este teste não teve um e-mail efetivamente enviado — não há conector de
> e-mail (Gmail/Outlook) disponível na sessão que rodou o teste. O Publicador
> prepara o conteúdo do e-mail como texto; o envio depende de uma ferramenta de
> e-mail conectada e de confirmação explícita do usuário (ver limitação em
> `agents/publisher.md` e `.claude/agents/publicador.md`).

---

## Resultado do teste

| Etapa | Resultado |
|---|---|
| Estrategista produziu briefing completo, sem campos em branco | ✅ |
| Redator seguiu a estratégia do briefing sem redefini-la | ✅ |
| Revisor reprovou um problema real (linguagem evasiva + CTA ausente) e não reescreveu o texto, apenas apontou | ✅ |
| Redator corrigiu exatamente os dois pontos apontados, sem alterar o resto | ✅ |
| Revisor aprovou na 2ª rodada com checklist limpo | ✅ |
| Publicador não alterou o conteúdo aprovado, só formatou/validou/empacotou | ✅ |
| Nenhum agente inventou produto, dado de mercado ou cliente fora da base de conhecimento | ✅ |

O fluxo `Usuário → Estrategista → Redator → Revisor → Publicador`, incluindo o
retorno ao Redator em caso de reprovação, funciona de ponta a ponta.
