#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orquestrador da rotina diária de posts de LinkedIn — LM for Business.

Fluxo: escolhe o tema em content-queue.md -> Estrategista -> Redator ->
Revisor (até 3 rodadas) -> Publicador -> envia o e-mail -> registra o tema em
"Publicadas" e confirma a gravação relendo o arquivo.

Uso:
    python scripts/orquestrador.py            # execução real
    python scripts/orquestrador.py --dry-run  # não envia e-mail nem altera a fila
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import logging
import os
import re
import smtplib
import sys
import unicodedata
from email.message import EmailMessage
from pathlib import Path

import anthropic
import yaml
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent.parent
load_dotenv(BASE / ".env")

FILA = BASE / "content-queue.md"
CONFIG = yaml.safe_load((BASE / "config" / "settings.yaml").read_text(encoding="utf-8"))
LIMITES = CONFIG["linkedin_limits"]

MODELO = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")
MAX_RODADAS_REVISAO = int(CONFIG["workflow"]["max_reproval_loops_before_escalation"])
JANELA_REAPROVEITAMENTO = 60  # dias
HOJE = dt.date.today()

LOG_DIR = BASE / "logs"
EXECUCAO_DIR = LOG_DIR / HOJE.isoformat()

logger = logging.getLogger("orquestrador")


# --------------------------------------------------------------------------
# Infraestrutura
# --------------------------------------------------------------------------

def configurar_log() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    EXECUCAO_DIR.mkdir(exist_ok=True)
    formato = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    arquivo = logging.FileHandler(LOG_DIR / "orquestrador.log", encoding="utf-8")
    arquivo.setFormatter(formato)
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formato)
    logger.setLevel(logging.INFO)
    logger.addHandler(arquivo)
    logger.addHandler(console)


def ler(*partes: str) -> str:
    return BASE.joinpath(*partes).read_text(encoding="utf-8")


def escrever(caminho: Path, conteudo: str) -> None:
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)


def salvar_artefato(nome: str, conteudo: str) -> None:
    escrever(EXECUCAO_DIR / nome, conteudo)


def normalizar(texto: str) -> str:
    """Minúsculas, sem acento e sem pontuação — para comparar temas."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto.lower())
    return re.sub(r"\s+", " ", texto).strip()


def temas_equivalentes(a: str, b: str) -> bool:
    na, nb = normalizar(a), normalizar(b)
    if not na or not nb:
        return False
    if na in nb or nb in na:
        return True
    return difflib.SequenceMatcher(None, na, nb).ratio() >= 0.80


# --------------------------------------------------------------------------
# Fila de temas (content-queue.md)
# --------------------------------------------------------------------------

class Tema:
    def __init__(self, titulo: str, metadata: str, servico: str,
                 reaproveitado: bool = False, data_original: str = "") -> None:
        self.titulo = titulo
        self.metadata = metadata
        self.servico = servico or "a definir"
        self.reaproveitado = reaproveitado
        self.data_original = data_original

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Tema {self.titulo!r} reaproveitado={self.reaproveitado}>"


def _secao(conteudo: str, titulo: str) -> tuple[int, int]:
    """Índices (início, fim) das linhas da seção '## <titulo>'."""
    linhas = conteudo.splitlines()
    inicio = next((i for i, l in enumerate(linhas) if l.strip() == f"## {titulo}"), None)
    if inicio is None:
        raise RuntimeError(f"Seção '## {titulo}' não encontrada em content-queue.md")
    fim = next((i for i in range(inicio + 1, len(linhas)) if linhas[i].startswith("## ")), len(linhas))
    return inicio, fim


def itens_pendentes(conteudo: str) -> list[tuple[int, int, str, str]]:
    """Lista de (linha_inicial, linha_final, titulo, bloco) da seção Pendentes."""
    linhas = conteudo.splitlines()
    inicio, fim = _secao(conteudo, "Pendentes")
    marcadores = [i for i in range(inicio + 1, fim) if re.match(r"^\d+\.\s+\*\*", linhas[i])]
    itens = []
    for pos, i in enumerate(marcadores):
        j = marcadores[pos + 1] if pos + 1 < len(marcadores) else fim
        bloco = "\n".join(linhas[i:j]).rstrip()
        titulo = re.match(r"^\d+\.\s+\*\*(.+?)\*\*", linhas[i]).group(1)
        itens.append((i, j, titulo.strip(" \"\u201c\u201d'"), bloco))
    return itens


def linhas_publicadas(conteudo: str) -> list[tuple[dt.date, str, str]]:
    publicadas = []
    for linha in conteudo.splitlines():
        m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*$", linha)
        if m:
            tema = re.sub(r"\*\(.*?\)\*", "", m.group(2)).strip()
            publicadas.append((dt.date.fromisoformat(m.group(1)), tema, m.group(3)))
    return publicadas


def publicado_recentemente(titulo: str, publicadas: list[tuple[dt.date, str, str]]) -> bool:
    limite = HOJE - dt.timedelta(days=JANELA_REAPROVEITAMENTO)
    return any(data >= limite and temas_equivalentes(titulo, tema) for data, tema, _ in publicadas)


def extrair_servico(bloco: str) -> str:
    m = re.search(r"Servi[c\u00e7]o:\s*(.+)", bloco)
    return m.group(1).strip(" ·") if m else ""


def selecionar_tema() -> Tema:
    conteudo = FILA.read_text(encoding="utf-8")
    publicadas = linhas_publicadas(conteudo)

    for _, _, titulo, bloco in itens_pendentes(conteudo):
        if publicado_recentemente(titulo, publicadas):
            logger.warning("Pulando '%s': tema equivalente publicado nos últimos %s dias.",
                           titulo, JANELA_REAPROVEITAMENTO)
            continue
        return Tema(titulo, bloco, extrair_servico(bloco))

    # Fila vazia (ou toda ela já publicada): reaproveita o tema mais antigo elegível.
    limite = HOJE - dt.timedelta(days=JANELA_REAPROVEITAMENTO)
    candidatos = [
        (data, tema, servico) for data, tema, servico in publicadas
        if data < limite and not publicado_recentemente(tema, publicadas)
    ]
    if not candidatos:
        raise RuntimeError(
            "Nenhum tema disponível: 'Pendentes' está vazia e nenhum tema publicado "
            f"tem mais de {JANELA_REAPROVEITAMENTO} dias."
        )
    data, tema, servico = min(candidatos, key=lambda c: c[0])
    logger.info("Fila de pendentes esgotada — reaproveitando '%s' (original de %s).", tema, data)
    return Tema(tema, f"Tema reaproveitado da publicação de {data.isoformat()}.",
                servico, reaproveitado=True, data_original=data.isoformat())


def registrar_publicacao(tema: Tema) -> None:
    """Remove o tema de 'Pendentes' e adiciona uma linha em 'Publicadas'."""
    conteudo = FILA.read_text(encoding="utf-8")
    linhas = conteudo.splitlines()

    if not tema.reaproveitado:
        for i, j, titulo, _ in itens_pendentes(conteudo):
            if titulo == tema.titulo:
                del linhas[i:j]
                break
        else:
            logger.warning("Tema '%s' não encontrado em 'Pendentes' para remoção.", tema.titulo)

    conteudo = "\n".join(linhas)
    inicio, fim = _secao(conteudo, "Publicadas")
    linhas = conteudo.splitlines()
    ultima_linha_tabela = max(
        (i for i in range(inicio, fim) if linhas[i].startswith("|")), default=None
    )
    if ultima_linha_tabela is None:
        raise RuntimeError("Tabela de 'Publicadas' não encontrada em content-queue.md")

    nota = f" *(reaproveitado de {tema.data_original})*" if tema.reaproveitado else ""
    linhas.insert(ultima_linha_tabela + 1,
                  f"| {HOJE.isoformat()} | {tema.titulo}{nota} | {tema.servico} |")
    escrever(FILA, "\n".join(linhas) + "\n")

    # Confirmação por releitura — passo 9 do workflow.
    novo = FILA.read_text(encoding="utf-8")
    ainda_pendente = any(titulo == tema.titulo for _, _, titulo, _ in itens_pendentes(novo))
    registrado = any(data == HOJE and temas_equivalentes(tema.titulo, t)
                     for data, t, _ in linhas_publicadas(novo))
    if (not tema.reaproveitado and ainda_pendente) or not registrado:
        raise RuntimeError("A atualização de content-queue.md não persistiu na releitura.")
    logger.info("content-queue.md atualizado e confirmado por releitura.")


# --------------------------------------------------------------------------
# Agentes
# --------------------------------------------------------------------------

cliente = anthropic.Anthropic(max_retries=3)


def conhecimento_de(agente: str) -> str:
    arquivos = CONFIG["agents"][agente].get("knowledge", [])
    partes = [f"# {caminho}\n\n{BASE.joinpath(caminho).read_text(encoding='utf-8')}"
              for caminho in arquivos]
    return "\n\n---\n\n".join(partes)


def rodar_agente(agente: str, entrada: str, max_tokens: int = 16000) -> str:
    logger.info("Agente %s: iniciando.", agente)
    resposta = cliente.messages.create(
        model=MODELO,
        max_tokens=max_tokens,
        system=[
            # Bloco estável primeiro, para o cache de prompt valer entre os agentes.
            {"type": "text", "text": conhecimento_de(agente),
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": ler(CONFIG["agents"][agente]["prompt"])},
        ],
        messages=[{"role": "user", "content": entrada}],
    )
    if resposta.stop_reason == "refusal":
        detalhe = getattr(resposta.stop_details, "explanation", "") if resposta.stop_details else ""
        raise RuntimeError(f"O agente {agente} foi recusado pela API: {detalhe}")
    if resposta.stop_reason == "max_tokens":
        raise RuntimeError(f"O agente {agente} estourou max_tokens ({max_tokens}) e saiu truncado.")

    texto = "\n".join(b.text for b in resposta.content if b.type == "text").strip()
    uso = resposta.usage
    logger.info("Agente %s: concluído (entrada=%s, cache lido=%s, saída=%s).",
                agente, uso.input_tokens, uso.cache_read_input_tokens, uso.output_tokens)
    return texto


REGRAS_COMUNS = """
Regras inegociáveis desta rotina:
- O post é escrito em PRIMEIRA PESSOA pelo próprio Leandro Miranda, que é quem publica.
  Nunca cite "Leandro" em terceira pessoa dentro do texto.
- O resultado é SEMPRE um único post de texto corrido para o feed. Nunca carrossel,
  slides, Reels ou qualquer formato multi-parte, mesmo que a ideia original diga isso.
- Linguagem clara e objetiva. A persona validada inclui setores fora de tecnologia
  (advocacia, frotas, saúde), então jargão de produto/tecnologia (discovery, delivery,
  squad, sprint, churn, NPS, PMF, roadmap, MVP) só entra com explicação curta em
  português — ou é substituído por uma forma simples.
- O fechamento NÃO pode ser oferta comercial de serviço pago. Só use CTA comercial
  direto quando o item da fila pedir isso explicitamente.
- Nunca invente produtos, clientes, cases ou estatísticas que não estejam na base de
  conhecimento.
""".strip()


def briefing_para(tema: Tema) -> str:
    origem = (f"Tema REAPROVEITADO da publicação de {tema.data_original}. "
              "Registre isso no briefing e escolha um ângulo, gancho ou estrutura "
              "diferente do que já foi usado."
              if tema.reaproveitado else
              "Tema novo, vindo da seção 'Pendentes' de content-queue.md.")
    return (
        f"Data de hoje: {HOJE.isoformat()}\n"
        f"Solicitante: {CONFIG['project']['default_requester']}\n\n"
        f"Tema: {tema.titulo}\n"
        f"{origem}\n\n"
        "Metadata da fila (o campo 'Formato' é apenas contexto histórico — ignore-o):\n"
        f"{tema.metadata}\n\n"
        f"{REGRAS_COMUNS}\n\n"
        "Produza o briefing completo no formato de templates/briefing.md."
    )


def revisor_aprovou(parecer: str) -> bool:
    m = re.search(r"Status:\s*\**\s*(APROVADO|REPROVADO)", parecer, re.IGNORECASE)
    if not m:
        logger.warning("Parecer do Revisor sem campo 'Status' reconhecível — tratando como reprovado.")
        return False
    return m.group(1).upper() == "APROVADO"


def produzir_post(tema: Tema) -> tuple[str, str]:
    briefing = rodar_agente("strategist", briefing_para(tema))
    salvar_artefato("briefing.md", briefing)

    post = rodar_agente("writer", f"{briefing}\n\n{REGRAS_COMUNS}")
    salvar_artefato("post-v1.md", post)

    for rodada in range(1, MAX_RODADAS_REVISAO + 1):
        parecer = rodar_agente(
            "reviewer", f"BRIEFING ORIGINAL:\n{briefing}\n\nPOST PARA AUDITAR:\n{post}")
        salvar_artefato(f"parecer-v{rodada}.md", parecer)
        if revisor_aprovou(parecer):
            logger.info("Post aprovado pelo Revisor na rodada %s.", rodada)
            return briefing, post
        if rodada == MAX_RODADAS_REVISAO:
            raise RuntimeError(
                f"Post reprovado {MAX_RODADAS_REVISAO} vezes. Nada foi enviado. "
                f"Último parecer:\n{parecer}"
            )
        logger.info("Rodada %s reprovada — devolvendo ao Redator.", rodada)
        post = rodar_agente(
            "writer",
            f"{briefing}\n\nPOST ANTERIOR:\n{post}\n\n"
            f"FEEDBACK DO REVISOR (corrija cada ponto):\n{parecer}\n\n{REGRAS_COMUNS}")
        salvar_artefato(f"post-v{rodada + 1}.md", post)

    raise RuntimeError("Fluxo de revisão terminou sem aprovação.")  # inalcançável


def formatar_para_publicacao(post: str) -> str:
    saida = rodar_agente(
        "publisher",
        f"POST APROVADO PELO REVISOR (Status: APROVADO):\n{post}\n\n"
        "Formate o texto final para colar no LinkedIn. Devolva APENAS o post final, "
        "sem comentários, análises ou contagem de caracteres, entre as marcações "
        "---INICIO-POST--- e ---FIM-POST---.",
    )
    m = re.search(r"---INICIO-POST---(.*?)---FIM-POST---", saida, re.DOTALL)
    final = (m.group(1) if m else saida).strip()
    salvar_artefato("post-final.md", final)
    return final


# --------------------------------------------------------------------------
# E-mail
# --------------------------------------------------------------------------

def montar_email(tema: Tema, post: str) -> tuple[str, str, str]:
    hashtags = " ".join(re.findall(r"#\w+", post)) or "(nenhuma encontrada)"
    caracteres = len(post)
    if not (LIMITES["recommended_min_chars"] <= caracteres <= LIMITES["recommended_max_chars"]):
        logger.warning("Post com %s caracteres, fora da faixa recomendada (%s–%s).",
                       caracteres, LIMITES["recommended_min_chars"],
                       LIMITES["recommended_max_chars"])

    html = ler("templates", "email.html")
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL).strip()
    substituicoes = {
        "{{nome_solicitante}}": CONFIG["project"]["default_requester"].split()[0],
        "{{tema}}": tema.titulo,
        "{{post_formatado}}": post,
        "{{contagem_caracteres}}": f"{caracteres} caracteres",
        "{{hashtags}}": hashtags,
    }
    for chave, valor in substituicoes.items():
        html = html.replace(chave, valor)

    texto = f"{post}\n\n---\nCaracteres: {caracteres}\nHashtags: {hashtags}\n"
    assunto = f"[LM for Business] Post pronto — {tema.titulo}"
    return assunto, texto, html


def enviar_email(assunto: str, texto: str, html: str | None = None) -> None:
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg.set_content(texto)
    if html:
        msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"]), timeout=60) as servidor:
        servidor.starttls()
        servidor.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        servidor.send_message(msg)
    logger.info("E-mail enviado para %s.", os.environ["EMAIL_TO"])


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Rotina diária de post de LinkedIn.")
    parser.add_argument("--dry-run", action="store_true",
                        help="gera o post, mas não envia e-mail nem altera a fila")
    args = parser.parse_args()

    configurar_log()
    logger.info("=== Início da execução (%s, modelo %s%s) ===",
                HOJE.isoformat(), MODELO, ", dry-run" if args.dry_run else "")
    try:
        tema = selecionar_tema()
        logger.info("Tema escolhido: %s", tema.titulo)
        _, post = produzir_post(tema)
        final = formatar_para_publicacao(post)
        assunto, texto, html = montar_email(tema, final)

        if args.dry_run:
            logger.info("dry-run: e-mail e fila não foram tocados. Post em %s", EXECUCAO_DIR)
            print(final)
            return

        enviar_email(assunto, texto, html)
        try:
            registrar_publicacao(tema)
        except Exception:
            # O e-mail já saiu: registrar a falha é essencial para não duplicar o tema.
            pendencia = LOG_DIR / "PENDENTE-REGISTRO.json"
            escrever(pendencia, json.dumps(
                {"data": HOJE.isoformat(), "tema": tema.titulo, "servico": tema.servico},
                ensure_ascii=False, indent=2))
            logger.exception("E-mail enviado, mas content-queue.md NÃO foi atualizado.")
            enviar_email(
                "[ATENÇÃO] Post enviado mas a fila não foi atualizada",
                f"O post '{tema.titulo}' foi enviado hoje, mas a atualização de "
                "content-queue.md falhou. Atualize a fila manualmente para não repetir "
                f"o tema. Detalhes em {pendencia}.")
            raise

        logger.info("=== Execução concluída: '%s' enviado e registrado. ===", tema.titulo)

    except Exception as erro:
        logger.exception("Falha na rotina de conteúdo.")
        try:
            enviar_email("[ERRO] Falha na rotina de conteúdo do LinkedIn",
                         f"{erro}\n\nVeja os logs em {LOG_DIR}.")
        except Exception:
            logger.exception("Falha também ao enviar o e-mail de erro.")
        sys.exit(1)


if __name__ == "__main__":
    main()
