#!/usr/bin/env bash
# setup.sh — one-shot helper for SPX Momentum Telegram bot
#
# Usage:
#   export BOT_TOKEN="123456:ABCDEF..."   # from @BotFather
#   bash telegram/setup.sh [deploy|set-webhook|get-chat-id|status|delete-webhook]
#
# Prerequisites:  aws-cli v2, aws-sam-cli, jq, curl
set -euo pipefail

BOT_TOKEN="${BOT_TOKEN:?Set BOT_TOKEN env var first}"
TG="https://api.telegram.org/bot${BOT_TOKEN}"
STACK_NAME="${STACK_NAME:-spx-momentum-bot}"
AWS_REGION="${AWS_REGION:-us-east-1}"

cmd="${1:-help}"

# ── helpers ───────────────────────────────────────────────────────────────────
tg() { curl -fsSL "${TG}/${1}" "${@:2}"; }

require() { command -v "$1" &>/dev/null || { echo "Error: $1 not found"; exit 1; }; }

# ── commands ──────────────────────────────────────────────────────────────────
case "$cmd" in

  get-chat-id)
    echo "==> Send ANY message to your bot now, then press Enter..."
    read -r
    tg getUpdates | jq '.result[-1].message.chat | {id, first_name, username}'
    ;;

  deploy)
    require sam
    CHAT_ID="${ALLOWED_CHAT_ID:?Set ALLOWED_CHAT_ID env var (run get-chat-id first)}"
    cd "$(git rev-parse --show-toplevel)"

    echo "==> Building SAM package..."
    sam build --template telegram/template.yaml

    echo "==> Deploying stack: ${STACK_NAME}"
    sam deploy \
      --stack-name "${STACK_NAME}" \
      --region     "${AWS_REGION}" \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        "BotToken=${BOT_TOKEN}" \
        "AllowedChatId=${CHAT_ID}" \
      --no-confirm-changeset \
      --no-fail-on-empty-changeset

    echo ""
    echo "==> Stack outputs:"
    aws cloudformation describe-stacks \
      --stack-name "${STACK_NAME}" \
      --region     "${AWS_REGION}" \
      --query "Stacks[0].Outputs" \
      --output table
    ;;

  set-webhook)
    require jq
    WEBHOOK_URL="${WEBHOOK_URL:?Set WEBHOOK_URL env var (copy from deploy output)}"
    echo "==> Registering webhook: ${WEBHOOK_URL}"
    tg setWebhook \
      -d "url=${WEBHOOK_URL}" \
      -d "allowed_updates=[\"message\"]" \
      -d "drop_pending_updates=true" | jq .
    ;;

  status)
    require jq
    echo "==> Webhook info:"
    tg getWebhookInfo | jq '{url, pending_update_count, last_error_message}'
    echo ""
    echo "==> Lambda functions:"
    aws lambda list-functions \
      --region "${AWS_REGION}" \
      --query "Functions[?starts_with(FunctionName,'spx-momentum')].[FunctionName,Runtime,LastModified]" \
      --output table 2>/dev/null || echo "(no Lambda functions found)"
    ;;

  delete-webhook)
    echo "==> Deleting webhook (bot will stop receiving updates)"
    tg deleteWebhook | jq .
    ;;

  help|*)
    cat <<'EOF'
SPX Momentum Telegram Bot — setup helper

Commands:
  get-chat-id     Find your Telegram chat ID (run before deploy)
  deploy          Build + deploy to AWS (requires sam, aws-cli)
  set-webhook     Register the API Gateway URL with Telegram
  status          Check webhook + Lambda status
  delete-webhook  Unregister webhook (pause bot)

Quick-start:
  1. Create bot: message @BotFather → /newbot → copy token
  2. export BOT_TOKEN="<token>"
  3. bash telegram/setup.sh get-chat-id       → message your bot, note the ID
  4. export ALLOWED_CHAT_ID="<chat_id>"
  5. bash telegram/setup.sh deploy
  6. Copy WebhookUrl from output
  7. export WEBHOOK_URL="<url>"
  8. bash telegram/setup.sh set-webhook
  9. Message /help to your bot — done!
EOF
    ;;
esac
