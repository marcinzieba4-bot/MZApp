"""
Mirbud S.A. — Calibration Example
===================================
Mirbud is the archetype that inspired this framework.
It's a Polish construction & general-contracting company (WSE: MRB) that
hedge funds have been quietly accumulating — a classic "asset-rich, operationally
mediocre, ignored by the market" setup.

This file serves two purposes:
  1. Show how to encode a real situation into the framework
  2. Calibrate the scoring weights — if Mirbud doesn't score HIGH,
     the weights need tuning because this is our reference case.

NOTE: Numbers below are illustrative (based on publicly available patterns
as of early 2025) and should be updated with real-time data before trading.
Always verify with primary filings (ESPI, KRS, annual reports).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.models import (
    Company, PivotSignal, PriceScenario, PivotType,
    SignalStrength, ScoringWeights
)
from framework.scoring import score_company
from framework.pivot_types import suggest_pivot_types, get_playbook
from framework.report import print_report


# ──────────────────────────────────────────────
# Step 1 — Build the Company profile
# ──────────────────────────────────────────────

mirbud = Company(
    name="Mirbud S.A.",
    ticker="MRB",
    exchange="WSE",          # Warsaw Stock Exchange
    sector="Construction & Engineering",
    country="Poland",

    # ── Price / size ──
    current_price=3.80,      # PLN per share (illustrative)
    market_cap_m=380,        # ~380m PLN market cap
    currency="PLN",

    # ── Balance sheet anchors ──
    # Construction companies often hold land/real estate at historical cost.
    # Mirbud has subsidiaries in real estate development (Mirobudownictwo, etc.)
    # The book value per share tends to be well above market price.
    book_value_per_share=6.20,        # PLN — company trades at deep P/B discount
    net_cash_per_share=0.40,          # PLN — moderate cash position
    hidden_asset_value_per_share=3.50, # Analyst estimate: land bank + RE portfolio
                                       # valued at historical cost in accounts

    # ── Earnings profile ──
    ebitda_margin_pct=5.5,    # Thin margins typical of Polish general contractors
    revenue_growth_yoy_pct=8, # Infrastructure spending growing (EU funds)
    roe_pct=7.5,

    # ── Ownership ──
    # Mirbud is founder-controlled; Jarosław Mucha family holds majority.
    # Low free float means small institutional buying moves the stock.
    insider_ownership_pct=62,
    institutional_ownership_pct=8,    # Very low — under-discovered
    float_pct=28,

    # ── Pivot thesis ──
    pivot_types=[
        PivotType.ASSET_RELEASE,      # Primary: land bank / RE revaluation or sale
        PivotType.OWNERSHIP_CHANGE,   # Secondary: hedge fund pressure → founder sells
        PivotType.CAPITAL_STRUCTURE,  # Tertiary: cash return / buyback programme
    ],

    thesis_summary=(
        "Mirbud trades at ~0.6x book despite owning a material land bank and real "
        "estate portfolio carried at historical cost. Hedge funds have been "
        "accumulating the illiquid float. Three paths to value: (1) founder sells "
        "control to a strategic or financial buyer at a 40-60% premium; (2) subsidiary "
        "real estate assets are separately listed or sold; (3) buyback programme "
        "initiated as infrastructure backlog shrinks free float further. "
        "EU infrastructure spending tailwind extends the window."
    ),

    key_risks=[
        "Founder (Mucha family) controls >60% and has shown no intent to sell",
        "Construction margins can compress if material costs spike",
        "Polish political risk affecting public infrastructure contracts",
        "Low liquidity — small float means exit could be costly",
        "Hidden liabilities in real estate subsidiaries not disclosed publicly",
    ],

    time_horizon_years=3.0,
)


# ──────────────────────────────────────────────
# Step 2 — Attach signals
# (Each signal is a specific, sourced observation)
# ──────────────────────────────────────────────

mirbud.signals = [

    # Smart money signals
    PivotSignal(
        name="Hedge fund crosses 5% threshold",
        description=(
            "A known event-driven hedge fund has accumulated >5% of shares, "
            "triggering mandatory disclosure. This fund typically targets "
            "asset-rich, family-controlled companies in CEE."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        source="WSE regulatory announcement (ESPI)",
        confidence=0.95,
    ),
    PivotSignal(
        name="Second institutional buyer accumulating",
        description="Block trades visible in WSE data suggest a second institution building a position.",
        strength=SignalStrength.MODERATE,
        category="smart_money",
        confidence=0.70,
    ),
    PivotSignal(
        name="No major insider selling despite run-up",
        description="Founder family has not sold shares despite price appreciation — suggests they too expect higher value.",
        strength=SignalStrength.MODERATE,
        category="smart_money",
        confidence=0.80,
    ),

    # Fundamental signals
    PivotSignal(
        name="P/B = 0.61 vs sector average 1.1x",
        description=(
            "Mirbud trades at a 44% discount to book compared to CEE construction peers. "
            "The discount is entirely explained by the real estate portfolio's book value "
            "being stale (assets acquired 10-15 years ago at historical cost)."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.90,
    ),
    PivotSignal(
        name="Land bank NAV estimated at 2–3x current market cap",
        description=(
            "Sell-side analyst (DM BOŚ) estimates Mirbud's land bank at PLN 600–900m "
            "vs market cap of PLN 380m. Even a conservative 50% haircut exceeds market cap."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.65,  # Analyst estimate — lower confidence
    ),

    # Catalyst signals
    PivotSignal(
        name="EU funds tranche 2021-2027 driving infrastructure backlog",
        description=(
            "Poland is receiving the largest per-capita allocation of EU cohesion funds. "
            "Mirbud's public infrastructure segment (roads, bridges) has multi-year backlog. "
            "This keeps the operating business cash-generative during the waiting period."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        confidence=0.90,
    ),
    PivotSignal(
        name="Founder age and succession uncertainty",
        description=(
            "Jarosław Mucha is in his mid-60s with no public succession plan. "
            "In Polish family business context, this is a common precondition for a sale."
        ),
        strength=SignalStrength.MODERATE,
        category="catalyst",
        confidence=0.50,  # Speculative
    ),
    PivotSignal(
        name="Strategic review rumour (unconfirmed)",
        description="Market rumour that management hired an advisor to explore 'strategic options' for the real estate arm.",
        strength=SignalStrength.WEAK,
        category="catalyst",
        confidence=0.30,
    ),

    # Sentiment signals
    PivotSignal(
        name="Zero sell-side coverage",
        description=(
            "No major bank covers Mirbud. The stock only appears in Polish niche "
            "publications. This is the definition of under-discovered — when a "
            "single analyst initiates coverage, institutional flows follow."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=1.0,
    ),
    PivotSignal(
        name="Retail investor frustration visible on forums",
        description=(
            "Polish investor forums (StockWatch, Stockwatch.pl) show long-term "
            "retail holders expressing frustration — a classic sentiment floor signal."
        ),
        strength=SignalStrength.MODERATE,
        category="sentiment",
        confidence=0.80,
    ),
]


# ──────────────────────────────────────────────
# Step 3 — Define price scenarios
# (Probability-weighted outcome tree)
# ──────────────────────────────────────────────

mirbud.scenarios = [

    PriceScenario(
        label="bear",
        price_target=2.80,   # PLN
        probability=0.20,
        rationale=(
            "Construction margins compress, hedge fund exits, founder doubles down "
            "on operational status quo. Stock re-rates to pure earnings basis without "
            "asset premium. -26% from current."
        ),
        time_horizon_years=3.0,
        irr=-9.0,
    ),

    PriceScenario(
        label="base",
        price_target=6.50,   # PLN — ~book value
        probability=0.55,
        rationale=(
            "Hedge fund pressure forces a buyback or partial asset sale (land bank). "
            "Stock gradually closes gap to book value over 3 years without a full "
            "takeout. +71% from current; ~19% IRR."
        ),
        time_horizon_years=3.0,
        irr=19.5,
    ),

    PriceScenario(
        label="bull",
        price_target=9.20,   # PLN — takeout at ~1.5x book
        probability=0.25,
        rationale=(
            "Founder negotiates a sale to a strategic buyer (large European contractor "
            "or PE fund) at 40-50% premium to book value to reflect the land bank. "
            "+142% from current; ~34% IRR."
        ),
        time_horizon_years=2.5,
        irr=34.0,
    ),
]


# ──────────────────────────────────────────────
# Step 4 — Run the framework
# ──────────────────────────────────────────────

def run():
    weights = ScoringWeights(
        asset_asymmetry    = 0.25,
        smart_money_signals = 0.25,
        catalyst_clarity   = 0.20,
        downside_protection = 0.15,
        business_quality   = 0.10,
        sentiment_discount = 0.05,
    )

    result = score_company(mirbud, weights)

    suggested = suggest_pivot_types(mirbud)

    print_report(mirbud, result, suggested)


if __name__ == "__main__":
    run()
