# Pivot Opportunity Framework (POF)

> Find companies where smart money sees more than the market prices in.

## The Core Idea

The best asymmetric investments occur when **three things align simultaneously**:

1. **The company trades below its potential value** — not just current earnings value, but the value it *could* realise if a specific change occurs
2. **A credible pivot mechanism exists** — not hope, but a concrete catalyst with observable preconditions
3. **The market hasn't priced it yet** — usually because the company is ignored, misunderstood, or misclassified

The Mirbud situation is the canonical example: a Polish construction company trading at 0.6x book value, with hedge funds accumulating the float, while the market treats it as a vanilla low-margin contractor.

---

## Framework Architecture

```
framework/
├── models.py       — Data structures (Company, PivotSignal, PriceScenario)
├── scoring.py      — Six-dimension scoring engine → Pivot Score (0–10)
├── pivot_types.py  — Eight pivot type playbooks with signal checklists
├── screener.py     — Batch ranking of a company watchlist
└── report.py       — Terminal report renderer

examples/
└── mirbud_analysis.py  — Reference calibration case (MRB: WSE)
```

---

## The Six Scoring Dimensions

| Dimension | Weight | What it measures |
|---|---|---|
| **Asset Asymmetry** | 25% | Hidden / undervalued assets vs. market price |
| **Smart Money Signals** | 25% | Quality of institutional interest (activists, HFs, PE) |
| **Catalyst Clarity** | 20% | How concrete and near-term is the trigger event |
| **Downside Protection** | 15% | How floored is the bear-case price |
| **Business Quality** | 10% | Can the core survive the 3-year wait? |
| **Sentiment Discount** | 5% | Under-coverage = more re-rating room |

### Conviction Tiers

| Score | Tier | Action |
|---|---|---|
| ≥ 7.0 + asymmetry ≥ 2.5x | **HIGH** | Size position, monitor weekly |
| 5.0 – 6.9 | **MEDIUM** | Starter position, set price alerts |
| 3.0 – 4.9 | **WATCH** | On radar, revisit in 6 months |
| < 3.0 | **PASS** | Not enough asymmetry today |

---

## The Eight Pivot Types

| Type | Typical Return | Base Rate | Core Signal |
|---|---|---|---|
| **Asset Release** | 50–200% | ~55% | P/B < 0.7, stale appraisals |
| **Ownership Change** | 30–80% | ~65% | 13D filing, aged founder |
| **Operational Turn** | 100–300% | ~45% | Margins 5–10pp below peers |
| **Strategic Reposition** | 80–250% | ~50% | Conglomerate discount, new CEO |
| **Capital Structure** | 30–100% | ~60% | Net cash > 30% of market cap |
| **Regulatory Windfall** | 50–400% | ~40% | Pending legislation, deadline |
| **Consolidation** | 40–100% | ~55% | Fragmented industry, recent M&A comps |
| **Tech Adoption** | 100–500% | ~35% | First-mover digitisation, CTO hire |

---

## Asymmetry Ratio

```
Asymmetry = (Bull price target − Current price) / (Current price − Bear price target)
```

- > 3x is attractive
- > 5x is exceptional
- Mirbud example: **5.4x**

---

## Quick Start

```bash
# Run the Mirbud reference analysis
python main.py --example mirbud

# List all available examples
python main.py --list
```

### Add your own company

```python
from framework.models import Company, PivotSignal, PriceScenario, PivotType, SignalStrength
from framework.scoring import score_company
from framework.report import print_report
from framework.pivot_types import suggest_pivot_types

company = Company(
    name="Your Company",
    ticker="XYZ",
    exchange="NYSE",
    sector="Industrials",
    country="USA",
    current_price=12.50,
    market_cap_m=250,
    book_value_per_share=18.00,
    # ... fill other fields
)

company.signals = [
    PivotSignal(
        name="Activist crossed 5%",
        description="...",
        strength=SignalStrength.STRONG,
        category="smart_money",
    ),
    # ... add more signals
]

company.scenarios = [
    PriceScenario(label="bear", price_target=9.0,  probability=0.20, rationale="..."),
    PriceScenario(label="base", price_target=18.0, probability=0.55, rationale="..."),
    PriceScenario(label="bull", price_target=28.0, probability=0.25, rationale="..."),
]

result = score_company(company)
print_report(company, result, suggest_pivot_types(company))
```

---

## Signal Categories

Each `PivotSignal` has a `category`:

- **`smart_money`** — Institutional accumulation, activist filings, insider buying
- **`fundamentals`** — Balance sheet ratios, P/B, NAV estimates, margin gaps
- **`catalyst`** — Specific near-term events that could trigger the pivot
- **`sentiment`** — Coverage gaps, retail frustration, analyst neglect

---

## Calibration Notes (from Mirbud)

The Mirbud analysis scores **6.7 / 10 (MEDIUM)** with **5.4x asymmetry**. This is intentional — the framework correctly identifies that Mirbud is a genuine opportunity (high asset asymmetry, excellent downside protection, smart money present) but *not yet* HIGH conviction because **the founder hasn't signalled intent to sell**.

When the catalyst fires (13D upgrade, strategic review announcement, or confirmed sale process), the Catalyst Clarity score jumps from ~4 to ~8, pushing total score above 7.5 — that's when you size up.

> **Rule of thumb:** Use the framework to build the watchlist at MEDIUM. Size the position when the catalyst confirms.
