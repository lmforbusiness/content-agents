#!/usr/bin/env bash
# Wrapper chamado pelo cron na VM Oracle Cloud (Oracle Linux 9, usuário opc).
# Garante execução única por vez, limite de tempo e sincronização da fila com o Git.

set -euo pipefail

PROJETO="${PROJETO:-$HOME/content-agents}"
LOCK="/tmp/content-agents.lock"
LIMITE_MINUTOS=30

cd "$PROJETO"
mkdir -p logs

# Uma execução por vez: se a anterior ainda roda, esta desiste.
exec 9>"$LOCK"
if ! flock -n 9; then
    echo "$(date -Is) execução anterior ainda em andamento — abortando." >> logs/cron.log
    exit 0
fi

# Traz alterações feitas fora da VM (novos temas na fila, ajustes de prompt).
git pull --rebase --autostash >> logs/cron.log 2>&1 || \
    echo "$(date -Is) aviso: git pull falhou, seguindo com a cópia local." >> logs/cron.log

STATUS=0
timeout "${LIMITE_MINUTOS}m" venv/bin/python scripts/orquestrador.py "$@" || STATUS=$?

# Devolve ao Git o registro do tema publicado.
if [[ -n "$(git status --porcelain content-queue.md)" ]]; then
    git add content-queue.md
    git commit -q -m "Registro automático: post de $(date +%F)"
    git push -q >> logs/cron.log 2>&1 || \
        echo "$(date -Is) aviso: git push falhou; o registro local está salvo." >> logs/cron.log
fi

exit $STATUS
