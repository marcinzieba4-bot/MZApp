"""
Lubawa SA (WSE: LBW)
=====================
Thesis: DEFENSE_REARMAMENT + MICRO_CAP_NEGLECT

Lubawa SA is a Polish manufacturer of protective and technical textiles for
defense, security, and industrial markets. Founded in 1951, headquartered in
Ostrów Wielkopolski.

Product portfolio:
  - Ballistic protection: vests, helmets, shields (police, military)
  - Military field equipment: inflatable tents, shelters, field hospitals
  - NATO-certified protective clothing: NBC suits, anti-drone ponchos
  - Technical textiles: tarpaulins, safety equipment, firefighter gear
  - Helicopter equipment: floats, emergency systems
  - Specialist export: ballistic protection to Middle East, Africa, Asia

WHY THIS IS MISPRICED — two independent reasons:

1. DEFENSE_REARMAMENT (Structural demand, priced at industrial multiple)
   Poland's defense spending: $301.6bn total 2026-2030 (vs $138.1bn in 2021-25)
   = +118% in just 5 years. Poland is spending 4.7% of GDP on defense in 2025,
   targeting 5% in 2026. This is a structurally committed government spend.

   Lubawa is a direct sub-contractor in this spend. Key contract examples:
     - Anti-drone ponchos for NATO (ESPI announcement Q2 2025)
     - Ballistic vests for Polish military and police (long-term framework)
     - Field hospital systems for NATO exercises

   European defense sub-contractors (quality comps):
     - Diehl Defence (Germany): ~25x EV/EBITDA
     - Safran Cabin (France): ~22x EV/EBITDA
     - Elbit Systems subsidiaries: ~18x EV/EBITDA
   Lubawa at 3.79x EV/EBITDA is priced as if none of this is happening.

2. MICRO_CAP_NEGLECT (0 analysts, 0% institutional)
   - 0 Bloomberg/FactSet analyst estimates
   - 0% institutional ownership (per public filings)
   - No English-language investor relations
   - Polish-only annual reports (not translated)
   - No investor day, no London roadshow

   When institutions discover this company, the re-rating is from 3.79x to
   the sector median. Even 10x EV/EBITDA would be +164% from current.
   At 15x (still below European defense comps): +296% from current.

Key financial metrics (data as of early 2026):
  2024 full year: Revenue PLN 510m (+35.1% YoY), Earnings PLN 100.8m (+121% YoY)
  H1 2025: Revenue PLN 312m (+52.2%), EBITDA PLN 75.9m, Profit PLN 56.9m
  Balance sheet: Net cash PLN 93.45m, Debt/Equity 0.01 (nearly debt-free)
  ROE: 29.48%, ROIC: 21.93%
  Equity: PLN 520.1m

Market structure:
  Market cap: PLN 657.88m (~€133m)
  EV: PLN 565.34m (~€114m)
  P/E: 5.86x (using FY2024 earnings of PLN 100.8m)
  EV/EBITDA: 3.79x
  Insider ownership: 51.22%
  Float: ~49%
  Simply Wall St fair value estimate: 54.6% above current price

Data as of: March 2026
Sources:
  - Lubawa SA annual report 2024 (lubawa.com/ir)
  - WSE ESPI filings (gpw.pl)
  - Simply Wall St analysis
  - stockanalysis.com/quote/wse/LBW/statistics/
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.models import (
    Company, PivotSignal, PriceScenario, PivotType,
    SignalStrength, ScoringWeights
)
from framework.scoring import score_company
from framework.pivot_types import suggest_pivot_types
from framework.report import print_report
from framework.margin_of_safety import (
    SafetyComponent, UpsideMechanism,
    analyse_margin_of_safety, print_margin_of_safety_report,
)
from framework.idea_types import (
    IdeaType, identify_idea_types, print_idea_type_report,
)


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# Shares: PLN 657.88m market cap / PLN 8.115 price ≈ 81.1m shares
# EV: PLN 565.34m (market cap PLN 657.88m - net cash PLN 93.45m = PLN 564.43m)

lubawa = Company(
    name="Lubawa SA",
    ticker="LBW",
    exchange="WSE",
    sector="Defense & Protective Equipment Manufacturing",
    country="Poland",

    current_price=8.115,          # PLN per share (January 14, 2026)
    market_cap_m=657.88,          # PLN millions
    currency="PLN",

    # Balance sheet anchors
    book_value_per_share=6.41,    # PLN 520.1m equity / 81.1m shares
    net_cash_per_share=1.15,      # PLN 93.45m net cash / 81.1m shares
    hidden_asset_value_per_share=0.0,  # No hidden assets — all on balance sheet

    # Earnings profile
    ebitda_margin_pct=24.3,       # H1 2025: PLN 75.9m / PLN 312m = 24.3%
    revenue_growth_yoy_pct=52,    # H1 2025 vs H1 2024: +52.2%
    roe_pct=29.48,

    # Ownership (!)
    insider_ownership_pct=51.22,
    institutional_ownership_pct=0,    # ZERO institutional ownership
    float_pct=49,

    pivot_types=[
        PivotType.STRATEGIC_REPOSITION,   # Commodity textile → NATO-grade defense specialist
        PivotType.REGULATORY_WINDFALL,    # Poland's mandatory 5% GDP defense spending
    ],

    thesis_summary=(
        "Lubawa SA is a micro-cap Polish defense manufacturer with P/E 5.86x and "
        "EV/EBITDA 3.79x — priced as a commodity textile maker. "
        "In reality: a growing NATO-certified ballistic protection and field equipment "
        "specialist with ROE 29.48%, revenue growing 52% YoY, and zero analyst coverage. "
        "The mispricing has TWO independent causes: (1) structural demand from NATO "
        "rearmament (Poland spending $301.6bn on defense 2026-2030) is creating a "
        "multi-year revenue runway; (2) zero institutional ownership and no English IR "
        "means institutions haven't found it yet. "
        "European defense sub-contractors trade at 15-25x EV/EBITDA. "
        "At Lubawa's current 3.79x, you pay PLN 565m EV for a business generating "
        "PLN 150m+ EBITDA/year and growing 50% annually. "
        "The catalyst is not an event — it's discovery."
    ),

    key_risks=[
        "Defense contract concentration: heavy dependence on Polish MoD procurement cycles",
        "Single-country risk: if Polish defense budget is cut (unlikely), revenues fall",
        "52-week high PLN 12.84 vs current PLN 8.115 = stock has been volatile",
        "Float ~49% but daily volumes may be thin — position building takes time",
        "Insider-controlled (51.22%): founders may not be interested in institutional engagement",
        "Currency: PLN/EUR volatility affects EUR-based investor returns",
        "Production capacity: rapid scaling requires capital investment in facilities",
    ],

    time_horizon_years=2.0,
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

lubawa.signals = [

    PivotSignal(
        name="Poland 5% GDP defense commitment — PLN 120bn+/year by 2026",
        description=(
            "Poland committed to 5% of GDP on defense in 2026 — the highest NATO member. "
            "Total 2026-2030 defense spending: $301.6bn (vs $138.1bn in 2021-2025). "
            "Lubawa is a licensed supplier to the Polish Ministry of Defense with "
            "existing framework contracts. New spend directly flows to approved vendors."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Polish Ministry of National Defense; NATO reporting",
        confidence=1.0,
    ),

    PivotSignal(
        name="NATO anti-drone poncho contract — new product line",
        description=(
            "Lubawa was awarded a NATO contract for anti-drone ponchos — protection "
            "against FPV drone fragments. This is a brand new, high-demand category "
            "created by Ukraine war experience. Lubawa is FIRST to market in Poland. "
            "NATO demand for this product across all member states = massive addressable market."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="ESPI announcement Q2 2025",
        confidence=0.95,
    ),

    PivotSignal(
        name="H1 2025 records: revenue +52%, profit +90% — acceleration confirmed",
        description=(
            "Not a one-off. H1 2025 set all-time records: PLN 312m revenue (+52.2%), "
            "PLN 56.9m net profit (+90.7%), PLN 75.9m EBITDA (+76.1%). "
            "Gross margin expanded from 32.8% to 35.2% — scaling efficiency. "
            "This is a business that is ACCELERATING, not decelerating."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="fundamentals",
        confidence=1.0,
    ),

    PivotSignal(
        name="P/E 5.86x — cheaper than any listed European defense company",
        description=(
            "Rheinmetall: 30x. Leonardo: 16x. Thales: 22x. Kongsberg: 25x. "
            "Lubawa at 5.86x P/E is not just cheap for defense — it's cheap for "
            "ANY profitable growing company. "
            "The only explanation: no one knows it exists in the institutional world."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.95,
    ),

    PivotSignal(
        name="ROE 29.48%, ROIC 21.93% — exceptional capital efficiency",
        description=(
            "Returns on capital in the 20-30% range signal a business with genuine "
            "competitive advantages: NATO certifications, approved supplier status, "
            "proprietary production processes. You can't replicate this easily. "
            "Few European companies achieve these returns at PLN 500m+ revenue scale."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.95,
    ),

    PivotSignal(
        name="Near debt-free (D/E 0.01) with PLN 93.45m net cash",
        description=(
            "EV is LOWER than market cap because of net cash. "
            "PLN 93.45m cash / PLN 657.88m market cap = 14.2% of market cap in cash. "
            "The EV/EBITDA of 3.79x is on a cash-adjusted basis — even cheaper than P/E suggests. "
            "No financial risk despite rapid growth."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=1.0,
    ),

    PivotSignal(
        name="ZERO institutional ownership, ZERO analyst coverage",
        description=(
            "0% institutional ownership. 0 Bloomberg/FactSet analyst estimates. "
            "No English annual report. No London or New York roadshow. "
            "This is the textbook 'institutional blindspot' situation. "
            "The re-rating happens when the FIRST institutional investor publishes research. "
            "The stock is not undiscovered because it's bad — it's undiscovered because "
            "of language and size barriers, not fundamental quality."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="sentiment",
        confidence=1.0,
    ),

    PivotSignal(
        name="51.22% insider ownership — management has personal financial stake",
        description=(
            "Majority founder-controlled. They have not sold despite 52-week high "
            "of PLN 12.84 (vs current PLN 8.115). "
            "Either: (a) they believe the company is worth substantially more, "
            "(b) they are waiting for the right institutional moment to sell. "
            "Either way: aligned with minority shareholders on value creation."
        ),
        strength=SignalStrength.MODERATE,
        category="smart_money",
        confidence=0.80,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

lubawa.scenarios = [

    PriceScenario(
        label="bear",
        price_target=5.00,    # PLN 5.00, -38%
        probability=0.15,
        rationale=(
            "Polish defense budget growth slows or shifts entirely to hardware imports "
            "(F-35s, K2 tanks, Abrams) with no domestic sub-contractor benefit. "
            "Revenue growth stalls at PLN 500m/year. "
            "At P/E 5x on flat earnings: PLN 100m × 5 = PLN 500m equity → PLN 6.16/share. "
            "But book value PLN 6.41 provides a floor. "
            "Hard to see below PLN 5 unless earnings genuinely collapse."
        ),
        time_horizon_years=2.0,
        irr=-22.0,
    ),

    PriceScenario(
        label="base",
        price_target=18.00,   # PLN 18.00, +122%
        probability=0.55,
        rationale=(
            "Revenue reaches PLN 750m by 2027 (sustainable growth from H1 2025 run-rate). "
            "EBITDA PLN 170m at 22.5% margin. "
            "Re-rates to 10x EV/EBITDA (conservative for defense with growth) = "
            "EV PLN 1.70bn + net cash PLN 120m = equity PLN 1.82bn / 81m shares = PLN 22.5. "
            "Assume some discount for illiquidity + Polish market = PLN 18. "
            "This requires NO multiple re-rating to European defense comps — "
            "just to 'decent industrial company' multiple."
        ),
        time_horizon_years=2.0,
        irr=49.0,
    ),

    PriceScenario(
        label="bull",
        price_target=38.00,   # PLN 38.00, +368%
        probability=0.30,
        rationale=(
            "Institutional discovery + European defense sector re-rating. "
            "Revenue PLN 900m+ (Lubawa wins international NATO framework contracts). "
            "EBITDA PLN 200m. At 15x EV/EBITDA = EV PLN 3.0bn → equity PLN 3.1bn / 81m = PLN 38. "
            "Or: Lubawa is acquired by Safran/Leonardo/Airbus Defense at "
            "strategic premium to Polish defense capability. "
            "Precedent: Safran paid ~20x for protected equipment specialists in 2021-2023."
        ),
        time_horizon_years=2.5,
        irr=86.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety
# ──────────────────────────────────────────────────────────────────────

LUBAWA_SAFETY = [
    SafetyComponent(
        name="Book value (equity)",
        value_per_share=6.41,
        confidence=0.90,
        description="PLN 520.1m equity / 81.1m shares. Net cash positive, D/E 0.01. Very solid.",
        how_to_verify="Lubawa SA annual report 2024, balance sheet",
        is_liquid=False,
    ),
    SafetyComponent(
        name="Net cash (hard floor)",
        value_per_share=1.15,
        confidence=0.95,
        description="PLN 93.45m net cash. Real, liquid, on balance sheet.",
        how_to_verify="Lubawa quarterly report — net debt disclosure",
        is_liquid=True,
    ),
    SafetyComponent(
        name="Defense framework contract backlog",
        value_per_share=4.80,
        confidence=0.80,
        description=(
            "Polish MoD framework contracts provide multi-year baseline. "
            "Backlog not publicly disclosed but estimable from order wins. "
            "At PLN 500m/year revenue, 18-month backlog = PLN 750m → "
            "NPV at 8% = ~PLN 390m / 81m shares = PLN 4.81."
        ),
        how_to_verify="ESPI contract award announcements",
        is_liquid=False,
    ),
]

LUBAWA_UPSIDE = [
    UpsideMechanism(
        name="Re-rating to 10x EV/EBITDA (basic industrial multiple)",
        price_target=18.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "Existing EBITDA of PLN 150m (annualised H1 2025) × 10x = PLN 1.5bn EV. "
            "Plus net cash PLN 93m → equity PLN 1.59bn / 81m shares = PLN 19.6. "
            "This requires ZERO growth assumption. Simply apply a normal industrial "
            "multiple to existing earnings power."
        ),
        probability=0.60,
        observable_trigger="First institutional investor discloses >1% stake via ESPI",
        months_to_trigger_estimate=18,
    ),
    UpsideMechanism(
        name="NATO international framework win + revenue to PLN 900m",
        price_target=38.00,
        requires_future_growth=True,
        growth_required_description="Revenue grows from PLN 510m to PLN 900m+ via international NATO contracts",
        correction_logic=(
            "Anti-drone ponchos, field hospital systems, NBC protection: all NATO "
            "members need what Lubawa makes. A single NATO framework win = "
            "multi-country revenue. At PLN 900m revenue × 22% margin = PLN 198m EBITDA. "
            "At 15x: EV PLN 2.97bn → PLN 38/share."
        ),
        probability=0.30,
        observable_trigger="Lubawa announces NATO framework contract for international delivery",
        months_to_trigger_estimate=24,
    ),
    UpsideMechanism(
        name="Acquisition by European defense prime at strategic premium",
        price_target=50.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "Safran, Leonardo, Airbus Defense, Rheinmetall have acquired protective "
            "equipment specialists at 18-25x EV/EBITDA. Lubawa at PLN 150m EBITDA "
            "× 20x = PLN 3bn EV = PLN 37/share + control premium = ~PLN 50."
        ),
        probability=0.15,
        observable_trigger="Strategic review announcement or ESPI major shareholder notification from foreign defense company",
        months_to_trigger_estimate=36,
    ),
]


def run():
    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print("  LUBAWA SA (WSE: LBW)")
    print("  Defense Rearmament + Micro-Cap Neglect")
    print(sep)

    # ── Idea type identification ──────────────────────────────────────
    idea_types = identify_idea_types(
        has_analyst_coverage=False,
        market_cap_m_eur=133,         # ~€133m
        institutional_pct=0,          # Zero!
        has_parent_under_pressure=False,
        has_frozen_stake=False,
        defense_revenue_pct=85,       # ~85% defense/security revenues
        has_government_pipeline=True,
        has_sotp_discount=False,
        has_ip_catalog=False,
        has_insider_cluster=False,
        chf_exposure=False,
        in_conflict_zone=False,
    )
    print(f"\n  IDENTIFIED IDEA TYPES:")
    print(thin)
    for idea_type, confidence in idea_types:
        print(f"  [{confidence:.0%}] {idea_type.value}: {idea_type.name}")

    # ── Defense spending context ──────────────────────────────────────
    print(f"\n\n  NATO REARMAMENT — THE DEMAND CONTEXT")
    print(thin)
    print("""
  Poland defense spending trajectory:
    2021-2025 (5 years total): $138.1bn
    2026-2030 (5 years total): $301.6bn  (+118%)
    2025 actual: 4.7% of GDP (highest NATO member)
    2026 target : 5.0% of GDP
    UK, Germany, Nordics, Baltics: all accelerating above 2% NATO target

  Lubawa's addressable market within Polish defense:
    Soldier equipment & protection : est. PLN 2-3bn/year by 2027
    Field systems & tents           : est. PLN 1-2bn/year
    NBC / CBRN protection           : est. PLN 500m-1bn/year
    Lubawa addressable total        : ~PLN 3.5-6bn/year
    Lubawa current revenue           : PLN 510m = ~9-14% share

  European defense sub-contractor EV/EBITDA multiples (comparable):
    Rheinmetall (Germany)  : 30x
    Leonardo (Italy)       : 16x
    Thales (France)        : 22x
    Kongsberg (Norway)     : 25x
    Chemring Group (UK)    : 12x
    QinetiQ Group (UK)     : 14x
    ─────────────────────────────
    Lubawa (Poland)        :  3.79x  ← 75-88% discount to peers
""")

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=lubawa,
        safety_components=LUBAWA_SAFETY,
        upside_mechanisms=LUBAWA_UPSIDE,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    weights = ScoringWeights(
        asset_asymmetry     = 0.15,
        smart_money_signals = 0.10,
        catalyst_clarity    = 0.25,   # NATO spending wave is the catalyst
        downside_protection = 0.15,
        business_quality    = 0.25,   # Business quality is exceptional
        sentiment_discount  = 0.10,   # Extreme sentiment discount
    )

    result    = score_company(lubawa, weights)
    suggested = suggest_pivot_types(lubawa)
    print_report(lubawa, result, suggested)

    # ── The institutional moment ──────────────────────────────────────
    print(f"\n{sep}")
    print("  THE INSTITUTIONAL MOMENT — WHAT TRIGGERS DISCOVERY")
    print(sep)
    print("""
  The stock is cheap. The business is excellent. So why is it at 3.79x EV/EBITDA?

  The answer is mechanical, not fundamental:

  1. Under-size threshold: PLN 657m / 81m shares = too small for most
     institutional mandates (minimum €200m market cap for large funds)
     → Lubawa at €133m is just below the threshold

  2. No English IR: Annual reports are in Polish only.
     Fund managers at Invesco, Fidelity, JPMorgan cannot read the filing.
     → Simple solution: Lubawa publishes an English version → discovery follows

  3. No sell-side coverage: Not a single analyst models this stock.
     → The first analyst note from Trigon DM, BM PKO BP, or a foreign broker
       triggers immediate institutional interest

  4. The WSE itself is in the process of being reclassified by MSCI
     to Developed Market (2026). This triggers a new wave of institutional
     inflows to Poland generally, including to under-covered names.

  WHO COULD DISCOVER IT:
    - CEE-specialist fund (Quant Capital, Wood & Co, Trigon, Ipopema)
    - Defense-focused ETF rebalancing (HANetf MSCI Europe Aerospace, etc.)
    - Family office in UK/Germany looking at European defense beneficiaries
    - European PE acquiring a defense platform (Advent, Bain Capital)

  WHEN YOU KNOW IT'S HAPPENING:
    - ESPI notification: foreign entity crosses 5% threshold
    - Polish broker publishes first research note (search: Lubawa LBW research)
    - Volume spike on WSE (daily volume > PLN 2m for consecutive weeks)
""")
    print(sep)


if __name__ == "__main__":
    run()
