#!/usr/bin/env bash
# deploy.sh — Package and deploy the MSCI Poland Lambda function
# Credentials must be set in the environment before running:
#   export AWS_ACCESS_KEY_ID=...
#   export AWS_SECRET_ACCESS_KEY=...
#
# Usage: bash deploy.sh
set -euo pipefail

: "${AWS_ACCESS_KEY_ID:?Set AWS_ACCESS_KEY_ID}"
: "${AWS_SECRET_ACCESS_KEY:?Set AWS_SECRET_ACCESS_KEY}"

python deploy.py
