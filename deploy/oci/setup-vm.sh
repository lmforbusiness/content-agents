#!/usr/bin/env bash
# Preparação da VM Oracle Cloud (Oracle Linux 9, shape VM.Standard.E2.1.Micro,
# usuário opc) para rodar a rotina diária de conteúdo.
#
# Pode ser executado mais de uma vez: cada etapa verifica se já está feita.
# Nada aqui cria recurso pago — só usa a instância e o disco que já existem.
#
#   bash deploy/oci/setup-vm.sh

set -euo pipefail

PROJETO="${PROJETO:-$HOME/content-agents}"
SWAP=/swapfile
TAMANHO_SWAP=2G

echo "== 1/6 Swap (${TAMANHO_SWAP}) =="
if swapon --show | grep -q "$SWAP"; then
    echo "swap já ativa, nada a fazer."
else
    sudo fallocate -l "$TAMANHO_SWAP" "$SWAP" || sudo dd if=/dev/zero of="$SWAP" bs=1M count=2048
    sudo chmod 600 "$SWAP"
    sudo mkswap "$SWAP"
    sudo swapon "$SWAP"
    grep -q "^$SWAP" /etc/fstab || echo "$SWAP none swap sw 0 0" | sudo tee -a /etc/fstab
fi
echo "vm.swappiness=10" | sudo tee /etc/sysctl.d/99-swap.conf > /dev/null
sudo sysctl --system > /dev/null
free -h

echo "== 2/6 Fuso horário =="
sudo timedatectl set-timezone America/Sao_Paulo
timedatectl | grep "Time zone"

echo "== 3/6 Pacotes (python3.12, git, cronie, logrotate) =="
sudo dnf install -y python3.12 python3.12-pip git cronie logrotate
sudo systemctl enable --now crond

echo "== 4/6 Ambiente virtual e dependências =="
cd "$PROJETO"
[[ -d venv ]] || python3.12 -m venv venv
venv/bin/pip install --no-cache-dir --upgrade pip
venv/bin/pip install --no-cache-dir -r requirements.txt
mkdir -p logs

echo "== 5/6 Rotação de logs =="
sudo tee /etc/logrotate.d/content-agents > /dev/null <<CONF
$PROJETO/logs/*.log {
    su $USER $USER
    weekly
    rotate 4
    compress
    missingok
    notifempty
    copytruncate
}
CONF
sudo logrotate -d /etc/logrotate.d/content-agents > /dev/null && echo "configuração de logrotate válida."

echo "== 6/6 Cron (9h no horário de Brasília) =="
LINHA="0 9 * * * $PROJETO/deploy/oci/run-diario.sh >> $PROJETO/logs/cron.log 2>&1"
chmod +x "$PROJETO/deploy/oci/run-diario.sh"
if crontab -l 2>/dev/null | grep -qF "run-diario.sh"; then
    echo "entrada de cron já existe:"
else
    (crontab -l 2>/dev/null; echo "$LINHA") | crontab -
    echo "entrada de cron criada:"
fi
crontab -l | grep "run-diario.sh"

echo
echo "Pronto. Falta apenas criar o .env:"
echo "  cp $PROJETO/.env.example $PROJETO/.env && chmod 600 $PROJETO/.env && nano $PROJETO/.env"
echo "Depois, teste sem enviar nada:"
echo "  cd $PROJETO && venv/bin/python scripts/orquestrador.py --dry-run"
