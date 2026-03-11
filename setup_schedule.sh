#!/usr/bin/env bash
# setup_schedule.sh — Add EventBridge monthly trigger to the Lambda
# Runs on the 1st of each month at 08:00 UTC
#
# Credentials must be set in the environment before running:
#   export AWS_ACCESS_KEY_ID=...
#   export AWS_SECRET_ACCESS_KEY=...
set -euo pipefail

: "${AWS_ACCESS_KEY_ID:?Set AWS_ACCESS_KEY_ID}"
: "${AWS_SECRET_ACCESS_KEY:?Set AWS_SECRET_ACCESS_KEY}"

FUNCTION_NAME="msci-poland-inclusion-report"
REGION="eu-west-1"
RULE_NAME="${FUNCTION_NAME}-monthly"
export AWS_DEFAULT_REGION="$REGION"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
LAMBDA_ARN="arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}"

echo "==> Creating EventBridge rule (1st of month, 08:00 UTC)..."
RULE_ARN=$(aws events put-rule \
    --name "$RULE_NAME" \
    --schedule-expression "cron(0 8 1 * ? *)" \
    --state ENABLED \
    --description "Monthly MSCI Poland report trigger" \
    --query RuleArn --output text)

echo "==> Adding Lambda as target..."
aws events put-targets \
    --rule "$RULE_NAME" \
    --targets "Id=1,Arn=${LAMBDA_ARN}"

echo "==> Granting EventBridge permission to invoke Lambda..."
aws lambda add-permission \
    --function-name "$FUNCTION_NAME" \
    --statement-id "EventBridgeMonthly" \
    --action "lambda:InvokeFunction" \
    --principal "events.amazonaws.com" \
    --source-arn "$RULE_ARN" 2>/dev/null || echo "    (permission already exists)"

echo ""
echo "✓  Monthly schedule active: runs 1st of each month at 08:00 UTC"
echo "   Rule ARN: $RULE_ARN"
