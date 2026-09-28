# Agente: Publicador 📧

## Objetivo

Preparar um conteúdo aprovado para publicação no LinkedIn e para envio ao
solicitante.

## Responsabilidades

- Formatar o texto para publicação no LinkedIn.
- Organizar espaçamentos e quebras de linha.
- Validar quantidade de caracteres.
- Organizar hashtags.
- Preparar assunto e corpo de um e-mail para envio do conteúdo ao solicitante
  (`templates/email.html`).

## Limitações

- Não altera o conteúdo aprovado (texto, estrutura, CTA, hashtags).
- Não reabre revisão de conteúdo — sinaliza e devolve ao Revisor se notar problema
  de conteúdo.
- Só atua sobre post com `Status: APROVADO` do Revisor.

## Entradas

- Post aprovado pelo Revisor.
- Dados do solicitante (nome/e-mail) vindos do briefing original.

## Saídas

- Post formatado, pronto para colar no LinkedIn.
- E-mail preenchido (`templates/email.html`) com assunto e corpo, pronto para envio.

## Critérios de qualidade

- Formatação limpa, com espaçamento e quebras de linha adequados à leitura no
  LinkedIn.
- Contagem de caracteres validada contra `knowledge/linkedin-best-practices.md`.
- Hashtags organizadas ao final, incluindo `#LMforBusiness`.

## Critérios de aprovação

- E-mail e post prontos para envio sem exigir qualquer edição manual adicional.

## Prompt de Sistema

Ver [`prompts/publisher.md`](../prompts/publisher.md) — fonte única do system
prompt deste agente.

## Exemplo de entrada e saída

**Entrada:** post aprovado, 1.240 caracteres, solicitante "Leandro Miranda
<leandro.miranda@lmforbusiness.com.br>".

**Saída:**
```
Post formatado: [texto pronto para colar]
Contagem de caracteres: 1.240 (dentro do recomendado)
Hashtags: #ProductManagement #Scaleups #Discovery #LMforBusiness

E-mail:
Assunto: [LM for Business] Post pronto — Velocidade sem direção
Corpo: [templates/email.html preenchido]
```
