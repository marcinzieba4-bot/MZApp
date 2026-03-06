# SPX Inclusion Momentum

Pre-position in S&P 500 addition candidates before the announcement using a 4-factor composite signal.

## Strategy in one sentence

Buy the top quintile of near-threshold S&P 500 candidates ranked by momentum + market-cap + eligibility streak, ~30 days before the quarterly rebalance announcement.

## Files

```
examples/
├── spx_inclusion_momentum.py        — Full backtest engine + terminal report (2012–2026)
├── spx_inclusion_momentum_pdf.py    — PDF report generator (post-2020 regime)
├── spx_inclusion_momentum_chart.png — Cumulative return chart (auto-generated)
└── spx_inclusion_momentum_report.pdf — Latest PDF report (auto-generated)
```

## Run

```bash
# Terminal backtest report
python examples/spx_inclusion_momentum.py

# PDF report (requires reportlab: pip install reportlab)
python examples/spx_inclusion_momentum_pdf.py
```

## Signal (4-factor composite)

| Factor | Weight | Rationale |
|--------|--------|-----------|
| 12-1 month momentum | 35% | Trend continuity |
| 3-month momentum | 20% | Short-term confirmation |
| Market cap rank | 30% | Large absent stocks = notable gap committee must fill |
| Eligibility streak | 15% | "Overdue" stocks on the waiting list |

## Backtest summary (2012–2023)

| Metric | Strategy | S&P 500 |
|--------|----------|---------|
| CAGR | +17.6% | +10.8% |
| Sharpe | 1.34 | 0.77 |
| Max drawdown | -17.1% | -24.7% |
| Win rate | 72.6% | — |

## Cycle calendar

Entry is ~30 days before each quarterly announcement. Typical hold ~75 days.

| Cycle | Rebalance entry | Announcement | Real addition |
|-------|----------------|--------------|---------------|
| 2026 Q1 | 2026-02-04 | 2026-03-06 | HOOD (Robinhood) |
| 2026 Q2 | ~2026-05-07 | ~2026-06-06 | TBD |
