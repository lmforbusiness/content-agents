# Runbook — rodar a rotina diária de LinkedIn na VM Oracle Cloud

Objetivo: sair do agendador local (que só dispara com o Claude Code aberto nesta
máquina) e rodar a rotina via **cron do Linux + Claude Code CLI headless**,
entregando o rascunho **direto no Gmail do próprio Leandro**.

> Eu não tenho acesso à sua conta/VM Oracle Cloud — não consigo executar estes
> passos por você. Este runbook é para você (ou quem administra a VM) seguir via
> SSH.

## Pré-requisitos

- VM Oracle Cloud já criada e acessível via SSH (você confirmou que já tem).
- Uma conta Claude que Leandro use (pode ser a conta dele, ou uma conta de
  automação da empresa — mas o Gmail conectado a ela precisa ser o do Leandro).
- Acesso ao Gmail do Leandro para autorizar o conector (ele mesmo faz esse
  consentimento, ou te dá autorização para fazer por ele).

## Passo 1 — Levar os arquivos do projeto para a VM

Duas opções:

**Opção A — Git (recomendado, facilita atualizar depois):**
```bash
# na sua máquina, dentro da pasta do projeto:
git init
git add .
git commit -m "Sistema de agentes de conteúdo LinkedIn — LM for Business"
# crie um repositório privado (GitHub/GitLab) e faça o push
git remote add origin <url-do-repo-privado>
git push -u origin main

# na VM, via SSH:
git clone <url-do-repo-privado> ~/lm-linkedin-content-agents
```

**Opção B — Copiar direto (mais rápido para um teste único):**
```bash
# da sua máquina Windows, via scp (ajuste usuário/IP/chave):
scp -r "C:\Users\renna\Documents\LM for Business\LM - Criador de conteúdo - Leandro" usuario@IP-DA-VM:~/lm-linkedin-content-agents
```

## Passo 2 — Instalar o Claude Code CLI na VM

Siga as instruções oficiais de instalação do Claude Code para Linux (a forma de
instalação muda com frequência — confira a documentação atual em
[claude.com/claude-code](https://claude.com/claude-code) em vez de fixar um
comando aqui). Confirme que funcionou com:
```bash
claude --version
```

## Passo 3 — Autenticar o Claude Code na VM

```bash
claude login
```
Isso abre um fluxo de autenticação (normalmente uma URL para abrir em qualquer
navegador — não precisa ser na própria VM). Use a conta Claude que vai operar a
rotina.

## Passo 4 — Conectar o Gmail do Leandro

Isso é feito **pela web**, em `claude.ai/settings/connectors` — não precisa ser
na VM. **O próprio Leandro deve fazer esse login e autorizar** (ou alguém com
acesso à conta Gmail dele), já que é a conta dele que vai guardar os rascunhos.
Procure "Gmail" na lista de conectores e clique em Connect.

Depois de conectado, na VM, rode uma vez de forma interativa para confirmar que
a ferramenta aparece:
```bash
cd ~/lm-linkedin-content-agents
claude
# dentro da sessão, pergunte: "quais ferramentas de Gmail estão disponíveis?"
```
Anote o nome exato da ferramenta de criar rascunho — algo como
`mcp__<id-do-conector>__create_draft`. O `<id-do-conector>` muda por conta
conectada, então **será diferente** do que já está em
`.claude/settings.json` (que hoje aponta para o conector desta sessão, não o do
Leandro).

## Passo 5 — Atualizar as permissões headless

Edite `.claude/settings.json` no projeto (na VM) e troque o ID da ferramenta de
Gmail pelo que você anotou no passo 4:
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "mcp__<id-do-conector-do-leandro>__create_draft"
    ]
  }
}
```
Isso evita que a execução headless trave esperando uma aprovação que ninguém vai
ver (não tem terminal interativo no cron).

## Passo 6 — Testar manualmente antes de automatizar

```bash
cd ~/lm-linkedin-content-agents
chmod +x deploy/run-daily-post.sh
# edite PROJECT_DIR dentro do script se o caminho não for
# ~/lm-linkedin-content-agents
./deploy/run-daily-post.sh
cat deploy/logs/$(date +%F).log
```
Confira: o `content-queue.md` foi atualizado, e o rascunho apareceu no Gmail do
Leandro.

## Passo 7 — Agendar no cron

Confira o fuso horário da VM primeiro:
```bash
timedatectl
```
Se a VM estiver em UTC (padrão comum na Oracle Cloud) e você quer 9h no horário
de Brasília (UTC-3, sem horário de verão desde 2019), o horário em UTC é 12h:
```bash
crontab -e
```
Adicione:
```
0 12 * * * /home/SEU_USUARIO/lm-linkedin-content-agents/deploy/run-daily-post.sh
```
(ajuste o caminho para o usuário/diretório reais na VM). Se a VM já estiver
configurada no fuso de São Paulo, use `0 9 * * *` diretamente.

## Passo 8 — Desligar a rotina local (evitar duplicidade)

Depois de confirmar que a versão na Oracle Cloud está funcionando sozinha por
alguns dias, me avise para eu desativar a rotina `daily-linkedin-post` que roda
nesta máquina Windows — senão os dois vão gerar posts e consumir a fila em
paralelo.

## Se, no futuro, quiser envio de verdade (não só rascunho)

O que temos hoje só cria rascunho — alguém (o Leandro) precisa abrir o Gmail e
publicar manualmente no LinkedIn. Se quiser automação ponta a ponta de verdade
(e-mail realmente entregue, sem depender de abrir rascunho), dá para trocar o
passo 4 do fluxo por um envio real via API do Gmail (escopo de envio) ou SMTP —
isso é um projeto à parte, me avise se quiser que eu desenhe.
