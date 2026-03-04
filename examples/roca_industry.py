"""
ROCA Industry SA (BVB: ROC1)
==============================
Thesis: CONSOLIDATION — Romanian Industrial Roll-Up

ROCA Industry is a Romanian industrial holding company listed on the Bucharest
Stock Exchange (BVB). It is building a platform of Romanian manufacturing and
industrial businesses through serial acquisitions.

The business model:
  ROCA acquires profitable Romanian SME industrial companies that are:
  - Too small to list independently (sub-€20m EBITDA)
  - In fragmented sectors with no dominant player
  - Owner-managed with succession needs (founders retiring)
  - Under-capitalised for growth but with strong core operations

  After acquisition, ROCA:
  - Brings group accounting, reporting, and governance
  - Provides access to capital markets (bonds, bank credit)
  - Identifies cross-selling and shared services synergies
  - Grows each business organically while acquiring more

  Portfolio companies (as of Q4 2025):
    BICO            — industrial component manufacturing
    EVOLOR          — paint and coating systems
    ECO EURO DOORS  — prefabricated door systems
    ELECTROPLAST    — plastic injection moulding for industrial/auto
    VELTA DOORS     — specialist door and partition systems (acquired 2024)

Why this is interesting:
  1. Extreme valuation: EV/EBITDA ~2.8x for a growing industrial platform
     (Romanian BVB Main Market industrials trade at 4-6x; Western EU equivalents
     at 8-12x EV/EBITDA for comparable quality roll-ups)

  2. Structural discount: BVB Main Market is still emerging-market classified
     by most institutional indices. Limited sell-side coverage. International
     investors systematically underweight Romanian equities.

  3. Growth catalyst: Upgraded from AeRO (SME market) to BVB Main Market
     in March 2024. This is the path to MSCI inclusion and institutional discovery.
     BVB Main Market → MSCI EM → Emerging market institutional buying.

  4. M&A pipeline: ROCA raised RON 140.7m via private placement (2024) and
     RON 50m via bond issuance — explicitly for acquisitions. The capital is
     already raised; acquisitions will happen.

  5. Romanian macro tailwind: Romania's GDP per capita ~60% of EU27 average.
     As wages and consumption rise, industrial companies benefit from:
     - Construction boom (PNRR — Romania's KPO equivalent, €28.5bn)
     - Auto/manufacturing FDI (Stellantis, Continental, etc. expanding)
     - Housing and commercial construction demand
     - EU structural fund absorption (road, energy, rail projects)

The re-rating path:
  ROCA at 2.8x EV/EBITDA → 7x EV/EBITDA (Romanian peer average)
  = +150% on multiple expansion alone, without any earnings growth
  At 10x EV/EBITDA (quality European roll-up premium):
  = +257% on multiple alone

Why the discount exists (and will resolve):
  - Sub-€50m market cap: below most institutional minimum ticket sizes
  - Romanian BVB: lacks liquidity and infrastructure for foreign investors
  - No sell-side coverage: zero analyst estimates on Bloomberg/FactSet
  - Recent AeRO → Main Market upgrade: institutional processes require
    18-24 months before new listings are added to approved investment lists

Data as of: March 2026
Sources:
  - ROCA Industry SA reports (bvb.ro, roca.ro)
  - BVB Main Market listing data
  - Romanian GDP and structural fund data (Romanian Ministry of Finance)
  - PNRR absorption data (Romanian Ministry of European Investments)
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
from framework.value_trap import detect_trap, print_trap_report


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# RON = Romanian Lei. ~4.95 RON = 1 EUR (March 2026, approximate)
# Market cap RON 178m ÷ ~21m shares = ~RON 8.50/share
# EBITDA margin 9.98% × RON 629m revenue = RON 62.8m EBITDA
# EV: if market cap RON 178m + net debt ~RON 95m = EV ~RON 273m
# EV/EBITDA: 273/62.8 = ~4.3x (slightly higher than 2.8x if debt included)
# NOTE: ROCA has been actively adding debt for acquisitions; the EV/EBITDA
# including acquisition debt is ~4-4.5x (still extremely cheap for the sector).

roca = Company(
    name="ROCA Industry SA",
    ticker="ROC1",
    exchange="BVB",
    sector="Industrial Manufacturing (Serial Acquirer)",
    country="Romania",

    # ── Price / size ──
    current_price=8.50,       # RON per share (approximate)
    market_cap_m=178,         # RON millions (~€36m at 4.95 RON/EUR)
    currency="RON",

    # ── Balance sheet anchors ──
    # After acquisitions, net assets include: property, equipment, brand value,
    # customer relationships, goodwill. Estimated equity: RON 130-150m.
    book_value_per_share=6.60,        # ~RON 140m equity / 21m shares
    net_cash_per_share=-4.50,         # Net debt from acquisitions (bonds + bank credit)
                                       # RON 95m net debt / 21m shares
    hidden_asset_value_per_share=3.20,  # Synergy value not yet captured in earnings;
                                        # goodwill from recent acquisitions carried at cost

    # ── Earnings profile ──
    ebitda_margin_pct=9.98,    # Q3 2025 annualised: RON 629m revenue × 9.98%
    revenue_growth_yoy_pct=18, # Inorganic (acquisitions) + organic
    roe_pct=11.5,

    # ── Ownership ──
    insider_ownership_pct=40,      # Founders / management hold ~40%
    institutional_ownership_pct=5, # Very under-institutionalised
    float_pct=55,

    # ── Pivot thesis ──
    pivot_types=[
        PivotType.CONSOLIDATION,        # Primary: Romanian industrial roll-up
        PivotType.ASSET_RELEASE,         # Secondary: individual businesses could be spun off
        PivotType.CAPITAL_STRUCTURE,     # Tertiary: listing at full multiple → NAV closes
    ],

    thesis_summary=(
        "ROCA Industry is a Romanian industrial holding company trading at ~4x EV/EBITDA "
        "(including acquisition debt) for a profitable, growing platform of Romanian "
        "manufacturing businesses. Western European comparable roll-ups (Lifco SE, "
        "Indutrade, Diploma PLC) trade at 15-25x EV/EBITDA. Romanian peers at 5-8x. "
        "The discount is entirely explained by: (1) tiny market cap (€36m) — too small "
        "for most institutions, (2) BVB Main Market recency (upgraded March 2024), "
        "(3) zero sell-side coverage. "
        "ROCA has explicitly raised capital for 2-3 new acquisitions in 2025-2026. "
        "Each acquisition is value-creative at the 2.8-4x acquisition price vs "
        "the 8-12x re-rating target. "
        "The catalyst path: BVB → MSCI EM → institutional discovery → re-rating. "
        "This is a 3-5 year patient play in the tradition of Nordic industrial roll-ups."
    ),

    key_risks=[
        "Acquisition integration: managing 5+ acquired businesses simultaneously "
        "requires significant management bandwidth; integration failures common",
        "Debt burden: RON 95m net debt on RON 178m market cap = high leverage ratio; "
        "interest costs could squeeze earnings if rates stay elevated",
        "Romanian governance risk: minority protection weaker than Western EU; "
        "ROCA's founders control 40% with limited independent board oversight",
        "Liquidity: thin float means entering or exiting a meaningful position "
        "takes weeks/months; bid-ask spreads are wide",
        "BVB illiquidity: daily volume often below RON 500k — position sizing is limited",
        "Economic sensitivity: Romanian industrial manufacturing is cyclical; "
        "EU recession or Romanian credit market stress could hurt all portfolio companies",
        "Currency risk: RON is not EUR; while stable (managed float), EUR-based "
        "investors carry FX exposure; RON depreciation would reduce EUR returns",
        "MSCI inclusion timeline: BVB MSCI EM upgrade expected ~2027-2028 at earliest",
    ],

    time_horizon_years=4.0,   # Longer timeline: BVB institutional discovery is slow
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

roca.signals = [

    # Smart money
    PivotSignal(
        name="RON 140.7m private placement (2024) — institutions bought in",
        description=(
            "ROCA conducted a RON 140.7m private placement in 2024 at a price "
            "above the then-market price, attracting Romanian and regional institutional "
            "investors. This is a SIGNAL: sophisticated buyers paid above-market to "
            "get exposure. The capital was raised explicitly for M&A pipeline."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        source="ROCA Industry capital raise announcement (BVB 2024)",
        confidence=0.90,
    ),
    PivotSignal(
        name="Founder-management alignment (40% ownership)",
        description=(
            "ROCA's management team holds ~40%. Every acquisition is done with the "
            "owners' own wealth at stake. This is the strongest possible alignment: "
            "management is not paid to acquire — they benefit only if the acquisitions "
            "create value. The roll-up is capital-allocator driven, not fee-driven."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        confidence=0.90,
    ),

    # Catalyst signals
    PivotSignal(
        name="BVB Main Market upgrade (March 2024) — institutional eligibility",
        description=(
            "ROCA moved from AeRO (SME market, sub-institutional) to BVB Main Market "
            "in March 2024. This makes it eligible for: Romanian pension funds, "
            "regional CEE funds, and eventually (after track record) MSCI EM indices. "
            "The institutional clock starts from March 2024."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="BVB Main Market listing announcement, March 2024",
        confidence=1.0,
    ),
    PivotSignal(
        name="RON 50m bond issue for acquisitions (2025)",
        description=(
            "ROCA issued RON 50m in bonds in 2025, specifically to fund the next "
            "acquisition wave. This is not balance sheet management — it is "
            "announcement of intent. 1-2 acquisitions expected in 2025-2026 "
            "will expand the revenue and EBITDA base."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="ROCA Industry bond prospectus, BVB",
        confidence=0.90,
    ),
    PivotSignal(
        name="PNRR (Romanian recovery plan) €28.5bn — manufacturing demand",
        description=(
            "Romania's PNRR includes €28.5bn of investment: roads, rail, energy, "
            "digitisation. ROCA's portfolio companies (BICO industrial components, "
            "ELECTROPLAST automotive parts, EVOLOR industrial coatings) are "
            "direct beneficiaries of the construction and manufacturing demand surge."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="Romanian PNRR implementation reports; European Commission",
        confidence=0.80,
    ),
    PivotSignal(
        name="MSCI EM potential inclusion (2027-2028 horizon)",
        description=(
            "BVB has been applying for MSCI EM upgrade (from Frontier Market). "
            "If successful, MSCI EM passive trackers would need to buy ALL "
            "BVB Main Market constituents. For ROCA: even a 0.02% weight in "
            "MSCI EM implies ~€60-80m of forced buying vs €36m current market cap."
        ),
        strength=SignalStrength.MODERATE,
        category="catalyst",
        source="MSCI market classification reviews; BVB MSCI eligibility work",
        confidence=0.45,  # Uncertain timing
    ),

    # Fundamental signals
    PivotSignal(
        name="EV/EBITDA ~4x vs Romanian industrial peers at 6-8x",
        description=(
            "ROCA trades at 4x EV/EBITDA (including acquisition debt). "
            "Comparable Romanian industrials on BVB Main Market: "
            "Teraplast 5.8x, Antibiotice 8.2x, Transgaz 6.5x. "
            "Romanian multiple at 6-8x = 50-100% upside from multiple alone. "
            "Western EU comparable (Lifco SE): 25x EV/EBITDA. "
            "ROCA is not Lifco, but the directional gap is enormous."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.90,
    ),
    PivotSignal(
        name="Revenue growth +18% YoY with 9.98% EBITDA margin maintained",
        description=(
            "Most roll-ups sacrifice margin for growth. ROCA has grown revenue "
            "+18% while keeping EBITDA margin stable at 9.98%. "
            "This suggests acquisition integration is working: not just adding "
            "revenue but maintaining profitability."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.85,
    ),

    # Sentiment signals
    PivotSignal(
        name="Stock down 26% in 2025 — sentiment at low",
        description=(
            "ROCA fell 26% in 2025 despite growing earnings. "
            "The fall was driven by: (1) general BVB market weakness in H1 2025, "
            "(2) concerns about debt levels post-acquisitions, "
            "(3) lack of institutional sponsorship to defend the price. "
            "Fundamental deterioration has NOT occurred — this is sentiment."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=0.80,
    ),
    PivotSignal(
        name="Zero institutional sell-side coverage on Bloomberg/FactSet",
        description=(
            "ROCA has no Bloomberg estimates, no FactSet consensus, no major "
            "bank research. It is completely invisible to systematic institutional "
            "investors (quant funds, index-aware managers). "
            "When the first research note is published, discovery follows."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=1.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

roca.scenarios = [

    PriceScenario(
        label="bear",
        price_target=4.50,    # RON 4.50, -47%
        probability=0.20,
        rationale=(
            "Romanian recession; construction/manufacturing slowdown; "
            "ROCA's debt becomes expensive; integration issues at 2024 acquisitions; "
            "MSCI EM upgrade delayed indefinitely. "
            "At 3x EV/EBITDA (distressed) and lower earnings: "
            "EV = RON 60m EBITDA × 3x = RON 180m. Less net debt RON 95m = RON 85m equity. "
            "/ 21m shares = RON 4.05. "
            "Book value floor at RON 6.60 provides some buffer."
        ),
        time_horizon_years=4.0,
        irr=-15.0,
    ),

    PriceScenario(
        label="base",
        price_target=18.00,   # RON 18.00, +112%
        probability=0.55,
        rationale=(
            "2-3 new acquisitions in 2025-2026. Revenue grows to RON 900-1000m. "
            "EBITDA: RON 88-100m at 9.5% margin. "
            "BVB institutional discovery: first sell-side coverage 2026. "
            "Re-rates from 4x to 6-7x EV/EBITDA (Romanian peer average). "
            "EV = RON 90m × 6.5x = RON 585m. Less net debt RON 120m = RON 465m equity. "
            "/ 21m shares = RON 22.14 (assume some dilution → RON 18-20)."
        ),
        time_horizon_years=4.0,
        irr=21.0,
    ),

    PriceScenario(
        label="bull",
        price_target=35.00,   # RON 35.00, +312%
        probability=0.25,
        rationale=(
            "MSCI EM upgrade accelerated; ROCA becomes the benchmark Romanian "
            "industrial holding. Revenue RON 1.5bn (5 new acquisitions). "
            "EBITDA RON 150-180m. Re-rates to 10-12x EV/EBITDA "
            "(international quality roll-up premium for proven track record). "
            "EV = RON 165m × 11x = RON 1.815bn. Less debt RON 150m = RON 1.665bn equity. "
            "/ 25m shares (mild dilution) = RON 66. "
            "Conservative cut to 50% of theoretical max = RON 33-35."
        ),
        time_horizon_years=4.0,
        irr=43.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety
# ──────────────────────────────────────────────────────────────────────

ROCA_SAFETY_COMPONENTS = [

    SafetyComponent(
        name="Book value (net assets post-acquisitions)",
        value_per_share=6.60,
        confidence=0.75,
        description=(
            "~RON 140m equity / 21m shares = RON 6.60. "
            "Assets: property, equipment, brands (EVOLOR), customer lists. "
            "Includes acquisition goodwill — requires monitoring for impairment risk."
        ),
        how_to_verify="ROCA annual report — balance sheet (bvb.ro disclosures)",
        is_liquid=False,
    ),

    SafetyComponent(
        name="EBITDA earnings power (existing businesses)",
        value_per_share=5.80,
        confidence=0.80,
        description=(
            "Even if no new acquisitions occur, existing businesses generate "
            "RON 62.8m EBITDA/year. At 3.5x distressed EV (floor), minus debt: "
            "RON 62.8m × 3.5x = RON 220m EV. Less RON 95m debt = RON 125m equity. "
            "/ 21m shares = RON 5.95 ≈ RON 5.80 (slight confidence haircut)."
        ),
        how_to_verify="ROCA quarterly results; segment EBITDA disclosures",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Replacement cost of manufacturing assets",
        value_per_share=4.20,
        confidence=0.60,
        description=(
            "ROCA's portfolio companies own factories, equipment, brands. "
            "Replacement cost (acquiring comparable businesses from scratch) "
            "would cost substantially more at current Romanian M&A multiples. "
            "Conservative replacement value: RON 88m / 21m shares = RON 4.20."
        ),
        how_to_verify="Transaction comparables: Romanian industrial M&A 2022-2025",
        is_liquid=False,
    ),
]

ROCA_UPSIDE_MECHANISMS = [

    UpsideMechanism(
        name="Multiple re-rating to Romanian industrial peer (6.5x EV/EBITDA)",
        price_target=18.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "ROCA's current 4x EV/EBITDA vs Romanian industrial median 6.5x. "
            "The gap is entirely explained by lack of institutional coverage. "
            "At 6.5x on RON 63m EBITDA = RON 410m EV. Less debt RON 95m = RON 315m. "
            "/ 21m shares = RON 15. Plus earnings growth to RON 75m next year = RON 18. "
            "This requires NO operational change — just the market to value it "
            "like other Romanian industrials."
        ),
        probability=0.50,
        observable_trigger="First Bloomberg/Refinitiv sell-side estimate published for ROCA",
        months_to_trigger_estimate=18,
    ),

    UpsideMechanism(
        name="2-3 acquisitions materialise, revenue reaches RON 1bn",
        price_target=22.00,
        requires_future_growth=True,
        growth_required_description=(
            "Requires successful completion and integration of 2-3 additional "
            "acquisitions using the raised capital (RON 190m available). "
            "Historical ROCA acquisitions have been at 3-5x EBITDA — deploying "
            "RON 190m acquires RON 38-63m of EBITDA at those prices."
        ),
        correction_logic=(
            "At RON 100m EBITDA total (existing + acquired), at 7x EV/EBITDA "
            "(re-rated peer multiple): RON 700m EV. Less debt RON 120m = RON 580m equity. "
            "/ 22m shares (mild dilution) = RON 26. Conservative: RON 22."
        ),
        probability=0.45,
        observable_trigger="ROCA announces 2nd acquisition in 2025-2026 cycle",
        months_to_trigger_estimate=12,
    ),

    UpsideMechanism(
        name="MSCI EM inclusion + strategic acquirer at EU multiple",
        price_target=35.00,
        requires_future_growth=True,
        growth_required_description=(
            "Requires: (1) BVB MSCI EM inclusion (2027-2028), (2) ROCA growing to "
            "RON 150-180m EBITDA (RON 1.5bn revenue), (3) either MSCI-driven re-rating "
            "or a Western European industrial holding (Lifco, Bergman & Beving, "
            "Indutrade) acquiring ROCA as a Romanian platform entry."
        ),
        correction_logic=(
            "At RON 165m EBITDA × 11x EV/EBITDA = RON 1.815bn EV. "
            "Less debt RON 150m = RON 1.665bn equity / 25m shares = RON 66.6. "
            "50% conservative cut = RON 33. "
            "Or: acquisition at 7-9x by Western roll-up = RON 35-45."
        ),
        probability=0.20,
        observable_trigger="MSCI announces BVB EM status OR ROCA receives strategic approach",
        months_to_trigger_estimate=36,
    ),
]


def run():
    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print("  ROCA INDUSTRY SA (BVB: ROC1)")
    print("  Consolidation — Romanian Industrial Roll-Up")
    print(sep)

    # ── Portfolio overview ───────────────────────────────────────────
    print(f"\n  PORTFOLIO COMPANIES (as of Q4 2025)")
    print(thin)
    portfolio = [
        ("BICO SA",              "Industrial component manufacturing",      "~12%", "Hardware, B2B"),
        ("EVOLOR SA",            "Paint and coating systems",                "~18%", "Construction/industrial"),
        ("ECO EURO DOORS SA",    "Prefabricated door systems",               "~22%", "Construction supply chain"),
        ("ELECTROPLAST SA",      "Plastic injection moulding",               "~28%", "Auto / industrial"),
        ("VELTA DOORS / other",  "Specialist doors & partitions (2024 acq)", "~20%", "Commercial construction"),
    ]
    print(f"\n  {'Company':<25} {'Sector':<35} {'Rev Share':>10}  {'Customer Base'}")
    print(f"  {'-'*25} {'-'*35} {'-'*10}  {'-'*20}")
    for name, sector, share, customers in portfolio:
        print(f"  {name:<25} {sector:<35} {share:>10}  {customers}")

    # ── Comparable roll-ups ──────────────────────────────────────────
    print(f"\n\n  COMPARABLE ROLL-UP VALUATIONS")
    print(thin)
    comps = [
        ("ROCA Industry (ROC1, BVB)",  "Romania", "€37m",   "4.0x",  "Platform building"),
        ("Teraplast (TRP, BVB)",        "Romania", "€280m",  "5.8x",  "Romanian industrial"),
        ("Transgaz (TGN, BVB)",         "Romania", "€1.2bn", "6.5x",  "Romanian infrastructure"),
        ("Lifco AB (LIFCO B, OSTO)",    "Sweden",  "€9.0bn", "25.0x", "Nordic roll-up benchmark"),
        ("Indutrade AB (INDT, OSTO)",   "Sweden",  "€6.8bn", "22.0x", "Nordic roll-up benchmark"),
        ("Diploma PLC (DPLM, LSE)",     "UK",      "€5.5bn", "18.5x", "UK roll-up"),
    ]
    print(f"\n  {'Company':<34} {'Country':<10} {'MktCap':>8}  {'EV/EBITDA':>10}  {'Note'}")
    print(f"  {'-'*34} {'-'*10} {'-'*8}  {'-'*10}  {'-'*25}")
    for name, country, cap, ev_ebitda, note in comps:
        marker = " ←" if "ROCA" in name else ""
        print(f"  {name:<34} {country:<10} {cap:>8}  {ev_ebitda:>10}  {note}{marker}")

    print(f"\n  Note: ROCA is an early-stage platform vs Lifco/Indutrade (20+ year track record).")
    print(f"  Target: re-rate to Romanian industrial peer (6-8x), not Nordic benchmark (20-25x).")
    print(f"  That target alone = +50-100% from current levels.")

    # ── Value trap check ─────────────────────────────────────────────
    print(f"\n\n  VALUE TRAP CHECK (small-cap, emerging market — always run this)")
    print(thin)
    trap = detect_trap(
        company=roca,
        years_trading_at_discount=1,         # Recent listing on Main Market; not a long discount
        related_party_risk=False,
        accounting_quality="medium",          # Romanian IFRS, audit quality improving
        activist_path_credible=False,
        sector_structurally_declining=False,  # Industrial manufacturing is not declining
        minority_rights_jurisdiction="weak",  # Romania: weaker minority rights than Western EU
    )
    print_trap_report(trap)

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=roca,
        safety_components=ROCA_SAFETY_COMPONENTS,
        upside_mechanisms=ROCA_UPSIDE_MECHANISMS,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    weights = ScoringWeights(
        asset_asymmetry     = 0.20,
        smart_money_signals = 0.20,
        catalyst_clarity    = 0.25,   # BVB Main Market upgrade + acquisitions = specific
        downside_protection = 0.10,
        business_quality    = 0.15,   # Profitable, growing, proven track record
        sentiment_discount  = 0.10,   # Extreme sentiment discount (down 26%, no coverage)
    )

    result    = score_company(roca, weights)
    suggested = suggest_pivot_types(roca)
    print_report(roca, result, suggested)

    # ── Currency context ─────────────────────────────────────────────
    print(f"\n{sep}")
    print("  CURRENCY AND MARKET ACCESS NOTES")
    print(sep)
    print("""
  Currency: RON (Romanian Lei). Exchange rate: ~4.95 RON = 1 EUR (March 2026)
  Market cap in EUR: ~€36m

  Execution considerations for EUR-based investors:
    - Minimum ticket: RON 50,000+ per trade to get meaningful fill
    - Settlement: T+2 on BVB (same as EU)
    - Broker access: Interactive Brokers has BVB access; most EU brokers do
    - FX: RON managed float vs EUR; limited devaluation risk historically
    - Repatriation: no capital controls on EUR/RON for EU entities

  Why the size matters for the thesis:
    - At €36m market cap, a €5m position = 14% of market cap
    - This is too large for most institutions → but ideal for family offices,
      high-conviction small-cap funds, and sophisticated private investors
    - The eventual institutional buyer (MSCI EM, regional fund) will face
      exactly this constraint — and will pay up to get exposure

  "Small is beautiful" until the stock reaches €150-200m market cap,
  at which point institutional access becomes practical and the re-rating
  becomes self-reinforcing.
""")
    print(sep)


if __name__ == "__main__":
    run()
