# CLAUDE.md — Project instructions for Claude Code

This file tells Claude how to work in this repository. It is read automatically
at the start of every session.

## What this project is

SPX Inclusion Momentum backtest. One strategy, one codebase.
Do NOT add unrelated strategies, frameworks, or example files.

## Key files

- `examples/spx_inclusion_momentum.py` — master file: all data, signal logic, backtest engine, terminal report
- `examples/spx_inclusion_momentum_pdf.py` — PDF renderer (imports from above)
- `telegram/handler.py` — AWS Lambda: Telegram bot (webhook + daily alert)
- `telegram/template.yaml` — AWS SAM deployment template
- `telegram/setup.sh` — bot setup helper (register webhook, get chat ID)

## How to run

```bash
python examples/spx_inclusion_momentum.py        # terminal report
python examples/spx_inclusion_momentum_pdf.py    # generates PDF
```

## When adding new S&P 500 additions

Edit `_ADDITIONS_RAW` in `spx_inclusion_momentum.py`. Each row:
```python
("TICK", "Full Name", "Sector", "YYYY-MM-DD announce", "YYYY-MM-DD effective",
  mcap_at_add_bn, mom_12_1, mom_3m, ret_entry_to_announce, ret_announce_to_eff, ret_eff_to_exit)
```
Also update `_SPX_QUARTERLY` if the year/quarter is new.

## Telegram bot (AWS Lambda)

Deploy with:
```bash
export BOT_TOKEN="..."
export ALLOWED_CHAT_ID="..."
bash telegram/setup.sh deploy
export WEBHOOK_URL="<url from output>"
bash telegram/setup.sh set-webhook
```

Bot commands: `/run` `/latest` `/next` `/additions` `/help`

Daily alerts fire at 08:00 UTC on entry-window open (T-30), 7 days before
announcement, and on announcement day itself.

## Coding conventions

- Self-contained: `spx_inclusion_momentum.py` uses only stdlib (no external deps)
- PDF file may use `reportlab` and imports from the main file via `sys.path.insert`
- `telegram/handler.py` imports from `examples/` via `sys.path.insert` — no package installation needed
- No framework/, no main.py, no unrelated examples

## What NOT to do

- Do not recreate the old Pivot Opportunity Framework (POF) — it was deleted intentionally
- Do not add new example files unrelated to SPX momentum
- Do not push to main; always use the designated claude/ branch
