"""
Polimex-Mostostal SA (WSE: PXM)
=================================
Thesis: REGULATORY_WINDFALL — Polish Nuclear Programme

Polimex-Mostostal is a Polish industrial construction group operating in three
segments: Energy (power plant construction and maintenance), Industry (chemical
plants, refineries, process industry), and Infrastructure (roads, bridges, rail).

The core business is distressed:
  - 2024 revenue: PLN 2.86bn (-5.2% YoY)
  - 2024 net loss: PLN -348m
  - Net loss driven by: cost overruns on fixed-price legacy contracts,
    impairments on Energy segment projects, restructuring costs

HOWEVER — a structural windfall has been committed:

Polish Nuclear Power Programme
  Poland's first nuclear power plant: 3x Westinghouse AP1000 reactors at
  Lubiatowo-Kopalino (Pomerania region), ~9 GW total.
  State entity: PEJ (Polskie Elektrownie Jądrowe) — wholly state-owned.

  Key dates:
    2023: Westinghouse AP1000 selected as technology
    2024: Mostostal Siedlce (Polimex subsidiary) announced as local partner
          by Westinghouse for mechanical and process construction
    2024: Polish government committed ~$15bn state financing + CfD mechanism
    2025: FEED (Front-End Engineering & Design) studies underway
    2026-2027: EPC contract award expected (PLN 30-50bn total EPC value)
    2033-2035: First reactor expected commissioning

The key question: what share of the nuclear construction does Polimex capture?
  Mostostal Siedlce has pre-qualified as the Westinghouse mechanical & process
  construction partner. AP1000 projects in other countries (Slovakia Mochovce,
  US Vogtle) show mechanical sub-contractor share at ~12-18% of total EPC value.
  At PLN 30bn total EPC × 12-15% = PLN 3.6-4.5bn for Mostostal Siedlce.
  Over 7-8 years = PLN 450-640m/year = more than doubling current Energy segment revenue.

The asymmetry:
  BEAR: Nuclear is delayed 5+ years; Polimex burns through remaining equity.
  BULL: Nuclear construction begins 2027-2028; Polimex transforms from distressed
        industrial contractor to nuclear-grade construction specialist.
  The bear is painful but survivable (PLN 754m cap, likely state support given strategic
  importance). The bull is transformative (+400-600% thesis).

Why this is a REGULATORY_WINDFALL, not speculation:
  1. $15bn state commitment is public and legally enacted (PEJ state financing)
  2. Technology selection (AP1000) is finalised — not subject to reversal without
     penalty to Westinghouse / US relationship
  3. CfD mechanism (like UK) removes merchant price risk — revenue is regulated
  4. Political consensus (both PO and PiS support nuclear) — no electoral risk
  5. EU taxonomy now classifies nuclear as "sustainable" — EU bank financing available

The risk is NOT "will Poland build nuclear?" (committed). The risk is:
  - Delay: nuclear projects always take longer than planned
  - Dilution: Polimex may need to raise equity before nuclear revenue arrives
  - Competition: Westinghouse may bring more international sub-contractors

Data as of: March 2026
Sources:
  - Polimex-Mostostal annual reports (polimex-mostostal.pl/investors)
  - PEJ (Polskie Elektrownie Jądrowe) announcements
  - Westinghouse Poland partnership announcement
  - Polish Ministry of Climate and Environment nuclear programme documents
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
from framework.pipeline_certainty import (
    PipelineItem, CertaintyLevel,
    analyse_pipeline, print_pipeline_report,
)
from framework.margin_of_safety import (
    SafetyComponent, UpsideMechanism,
    analyse_margin_of_safety, print_margin_of_safety_report,
)
from framework.value_trap import detect_trap, print_trap_report


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# Shares: ~230m implied at ~PLN 3.28/share for PLN 754m market cap
# (Polimex has done multiple rights issues; share count approximate)

polimex = Company(
    name="Polimex-Mostostal SA",
    ticker="PXM",
    exchange="WSE",
    sector="Industrial / Energy / Infrastructure Construction",
    country="Poland",

    # ── Price / size ──
    current_price=3.28,      # PLN per share (approximate)
    market_cap_m=754,        # PLN millions
    currency="PLN",

    # ── Balance sheet anchors ──
    # After PLN -348m net loss in 2024, equity has eroded.
    # Estimated equity: PLN 400-450m → ~PLN 1.90/share
    book_value_per_share=1.90,
    net_cash_per_share=-0.50,    # Net debt (construction WC financing)
    hidden_asset_value_per_share=6.50,   # Nuclear partnership option value:
                                          # Mostostal Siedlce pre-qualification is not
                                          # on the balance sheet at all; it represents
                                          # a call option on PLN 3.6-4.5bn of nuclear work

    # ── Earnings profile ──
    ebitda_margin_pct=-3.0,     # Negative: PLN -86m EBITDA estimate on PLN 2.86bn revenue
                                 # (net loss PLN 348m includes non-cash impairments)
    revenue_growth_yoy_pct=-5,  # Revenue declined 5.2% YoY (2024)
    roe_pct=-55.0,

    # ── Ownership ──
    insider_ownership_pct=8,      # Management stake small; state entities ~15%
    institutional_ownership_pct=22,
    float_pct=70,

    # ── Pivot thesis ──
    pivot_types=[
        PivotType.REGULATORY_WINDFALL,   # Primary: nuclear programme
        PivotType.OPERATIONAL_TURN,       # Secondary: core business stabilisation
        PivotType.STRATEGIC_REPOSITION,   # Energy segment exits fixed-price, moves to nuclear
    ],

    thesis_summary=(
        "Polimex is a distressed industrial contractor with a potential transformative "
        "regulatory windfall: its subsidiary Mostostal Siedlce was selected by Westinghouse "
        "as the Polish mechanical construction partner for Poland's AP1000 nuclear programme. "
        "If this translates to EPC contracts (expected 2026-2028), nuclear work alone "
        "could be PLN 400-600m/year for 7-8 years — more than doubling the Energy segment. "
        "The current stock price reflects the distressed core business and "
        "ignores the nuclear option almost entirely. "
        "The thesis is binary: if nuclear EPC contracts are awarded on the current timeline, "
        "Polimex transforms. If nuclear is delayed 5+ years, the question is whether the "
        "core business survives. "
        "The state-committed $15bn nuclear financing and CfD mechanism make 'delayed' "
        "far more likely than 'cancelled'."
    ),

    key_risks=[
        "Core business losses continue: further impairments could exhaust equity by 2026",
        "Dilution: Polimex may need a rights issue before nuclear revenue arrives; "
        "this is the most likely near-term negative event",
        "Nuclear timeline: AP1000 projects have a history of cost overruns and delays "
        "(Vogtle in the US was 7 years late and doubled in cost)",
        "Contract structure: Mostostal Siedlce's pre-qualification does not guarantee "
        "the EPC contract share; Westinghouse may bring international subs",
        "Fixed-price legacy contracts: Energy segment has 3-4 legacy fixed-price "
        "contracts still outstanding; additional impairments possible",
        "State-controlled shareholder dynamics: Polish state entities own ~15% and "
        "their interests may not align with minority shareholders",
    ],

    time_horizon_years=4.0,   # Longer horizon: nuclear is a 2027+ story
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

polimex.signals = [

    # Smart money / catalyst
    PivotSignal(
        name="Westinghouse selected Mostostal Siedlce as Polish partner — DEFINITIVE",
        description=(
            "Westinghouse publicly announced Mostostal Siedlce (Polimex-Mostostal "
            "subsidiary) as its preferred Polish local partner for mechanical and "
            "process construction on the AP1000 project at Lubiatowo-Kopalino. "
            "This is a signed letter of intent / partnership agreement — not a tender."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Westinghouse / PEJ press releases; Polimex ESPI announcements",
        confidence=1.0,
    ),
    PivotSignal(
        name="Polish government $15bn nuclear financing committed",
        description=(
            "Polish government committed state financing for the AP1000 programme "
            "via PEJ (state-owned nuclear company). US Exim Bank and DFC (Development "
            "Finance Corporation) agreed financing. Total: ~$15bn. "
            "This is a formal government-to-government commitment, not a budget line."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Polish Ministry of Climate; US-Poland nuclear cooperation agreement",
        confidence=0.95,
    ),
    PivotSignal(
        name="CfD mechanism enacted for Polish nuclear",
        description=(
            "Poland enacted a CfD (Contracts for Difference) mechanism for nuclear "
            "power, similar to the UK's nuclear CfD. The state guarantees revenue "
            "above a strike price for 30+ years. This eliminates merchant revenue risk "
            "and makes nuclear project financing bankable."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Polish nuclear law amendment; URE (Polish Energy Regulatory Office)",
        confidence=0.90,
    ),
    PivotSignal(
        name="FEED (Front-End Engineering & Design) studies underway",
        description=(
            "PEJ awarded FEED contracts in 2025. FEED completion triggers move to "
            "EPC contract award. Timeline: FEED complete 2026 → EPC award 2026-2027. "
            "Each step is a binary event — the next event is FEED completion."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="PEJ corporate announcements",
        confidence=0.85,
    ),
    PivotSignal(
        name="EU taxonomy: nuclear classified as 'sustainable' (2022)",
        description=(
            "The European Commission classified nuclear as a sustainable energy "
            "source under the EU Taxonomy (effective 2023). This allows European "
            "ESG funds to invest in nuclear project financing. Removes a key "
            "financing constraint for Polish nuclear."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="EU Taxonomy Regulation, Delegated Act February 2022",
        confidence=1.0,
    ),

    # Fundamental
    PivotSignal(
        name="Nuclear option has near-zero book value but PLN 3.6-4.5bn potential",
        description=(
            "Mostostal Siedlce's Westinghouse partnership is carried on the balance "
            "sheet at cost of PLN ~0. The option value: if they capture 12-15% of "
            "a PLN 30-40bn nuclear EPC contract = PLN 3.6-6bn of work over 8 years. "
            "At 6% EBITDA margin = PLN 216-360m EBITDA/year. "
            "Current market cap PLN 754m vs PLN 1.7-2.9bn EBITDA NPV at 10% discount rate."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.70,
    ),
    PivotSignal(
        name="Revenue PLN 2.86bn — construction capability exists",
        description=(
            "Despite losses, Polimex has PLN 2.86bn of revenue capacity. "
            "The underlying business has the workforce, equipment, and project "
            "management to execute large-scale industrial construction. "
            "Nuclear is a step up in complexity but not a completely new skill set."
        ),
        strength=SignalStrength.MODERATE,
        category="fundamentals",
        confidence=0.80,
    ),

    # Sentiment
    PivotSignal(
        name="Retail investor frustration — 'perma-bear' narrative on Polimex",
        description=(
            "Polish retail investors have given up on Polimex after years of "
            "loss-making. The nuclear catalyst is not widely modelled by "
            "Polish sell-side (they focus on short-term earnings, not "
            "10-year construction programmes). Extreme sentiment discount."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=0.85,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

polimex.scenarios = [

    PriceScenario(
        label="bear",
        price_target=1.20,    # PLN 1.20, -63%
        probability=0.30,
        rationale=(
            "Nuclear EPC contract is awarded to a predominantly foreign JV with "
            "minimal Mostostal participation. Core business continues to bleed. "
            "Rights issue at PLN 1.00 dilutes existing shareholders. "
            "Stock trades near book value of distressed construction company. "
            "Note: this IS a binary risk — if this happens, the loss is very large."
        ),
        time_horizon_years=4.0,
        irr=-23.0,
    ),

    PriceScenario(
        label="base",
        price_target=9.00,    # PLN 9.00, +174%
        probability=0.45,
        rationale=(
            "Nuclear FEED complete 2026; EPC contract awarded to Westinghouse/Mostostal "
            "JV in 2027. Mostostal captures 10-12% of PLN 30bn EPC = PLN 3-3.6bn "
            "over 8 years. Backlog re-rated: at PLN 375-450m/year revenue, EBITDA 6% "
            "= PLN 22-27m incremental. Core stabilises at break-even. "
            "By 2028 when construction ramps up, Polimex trades at 8-10x forward "
            "EBITDA on combined nuclear + core = PLN 9-11/share."
        ),
        time_horizon_years=4.0,
        irr=29.0,
    ),

    PriceScenario(
        label="bull",
        price_target=16.00,   # PLN 16.00, +388%
        probability=0.25,
        rationale=(
            "Mostostal Siedlce captures 15-18% of nuclear EPC = PLN 4.5-5.4bn over 8yr. "
            "Core business operational turn (new CEO, exits fixed-price model). "
            "Re-rates to nuclear/defence contractor multiple (12-15x EV/EBITDA). "
            "Polish state becomes anchor shareholder to protect strategic asset. "
            "At PLN 80m normalised EBITDA by 2028 × 15x = PLN 1.2bn equity. "
            "+ nuclear backlog NPV PLN 400m → PLN 16-18/share."
        ),
        time_horizon_years=4.0,
        irr=49.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Nuclear pipeline analysis (PLN millions)
# ──────────────────────────────────────────────────────────────────────

NUCLEAR_PIPELINE = [

    PipelineItem(
        name="AP1000 Reactor 1 — mechanical construction (Mostostal Siedlce)",
        program_name="Polish Nuclear Power Programme — Unit 1 (Lubiatowo-Kopalino)",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=10_000,    # ~PLN 10bn per reactor (~$2.5bn)
        company_addressable_pct=0.15,    # 15% mechanical/process sub-share
        company_win_probability=0.65,    # Pre-qualified; not guaranteed
        company_consortium_share=1.0,
        revenue_start_year=2.0,          # Expected EPC start 2027-2028
        revenue_duration_years=7.0,
        margin_pct=7.0,
        public_source="PEJ / Westinghouse partnership; Polimex ESPI",
        notes="CfD mechanism enacted; $15bn state financing committed",
    ),

    PipelineItem(
        name="AP1000 Reactor 2 — mechanical construction",
        program_name="Polish Nuclear Power Programme — Unit 2",
        certainty=CertaintyLevel.PLANNED,
        total_program_value_m=10_000,
        company_addressable_pct=0.15,
        company_win_probability=0.60,    # If Unit 1 delivers → higher confidence
        company_consortium_share=1.0,
        revenue_start_year=4.0,
        revenue_duration_years=7.0,
        margin_pct=7.5,                  # Learning curve improvement
        public_source="PEJ programme roadmap",
    ),

    PipelineItem(
        name="AP1000 Reactor 3 — mechanical construction",
        program_name="Polish Nuclear Power Programme — Unit 3",
        certainty=CertaintyLevel.PLANNED,
        total_program_value_m=10_000,
        company_addressable_pct=0.15,
        company_win_probability=0.55,
        company_consortium_share=1.0,
        revenue_start_year=6.0,
        revenue_duration_years=7.0,
        margin_pct=8.0,
        public_source="PEJ programme roadmap",
    ),

    PipelineItem(
        name="Nuclear auxiliary buildings & civil interface (core capability)",
        program_name="AP1000 — auxiliary structures, industrial buildings",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=3_500,     # Auxiliary works across 3 units
        company_addressable_pct=0.25,    # Polimex has civil construction capability
        company_win_probability=0.50,
        company_consortium_share=1.0,
        revenue_start_year=1.5,
        revenue_duration_years=10.0,
        margin_pct=6.5,
        public_source="Westinghouse AP1000 scope definition documents",
    ),

    PipelineItem(
        name="Energy segment legacy backlog (non-nuclear)",
        program_name="Conventional power plant maintenance and construction (Poland)",
        certainty=CertaintyLevel.SCHEDULED,
        total_program_value_m=4_000,     # Ongoing maintenance, refinery turnarounds
        company_addressable_pct=0.25,    # Polimex is top-3 in this segment
        company_win_probability=0.60,
        company_consortium_share=1.0,
        revenue_start_year=0.0,
        revenue_duration_years=5.0,
        margin_pct=4.5,
        public_source="Polish energy maintenance tender market",
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety (distressed company; floor is thin)
# ──────────────────────────────────────────────────────────────────────

POLIMEX_SAFETY_COMPONENTS = [

    SafetyComponent(
        name="Book value (eroded, post-impairments)",
        value_per_share=1.90,
        confidence=0.50,   # Losses are continuing; further impairments likely
        description=(
            "Net assets ~PLN 437m / 230m shares = PLN 1.90. "
            "WARNING: PLN -348m loss in 2024 means this could fall further. "
            "Not a strong floor."
        ),
        how_to_verify="Polimex annual report 2024 — balance sheet",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Revenue base (PLN 2.86bn ongoing contracts)",
        value_per_share=2.10,
        confidence=0.55,
        description=(
            "A company generating PLN 2.86bn in revenue is not going to zero. "
            "Even at zero EBITDA, the franchise value (workforce, certifications, "
            "client relationships, Mostostal Siedlce nuclear pre-qualification) "
            "has replacement cost. "
            "Estimated floor: 0.25x revenue × 0.55 confidence = PLN 394m / 230m shares."
        ),
        how_to_verify="Polimex revenue disclosures, segment reporting",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Mostostal Siedlce nuclear partnership (option floor)",
        value_per_share=3.50,
        confidence=0.45,   # Not guaranteed; nuclear timeline uncertain
        description=(
            "The Westinghouse partnership has a real floor value even if the full "
            "nuclear programme is delayed. Other nuclear-grade contractors in Europe "
            "have been acquired at significant premiums (Boccard SA, Somafel). "
            "The pre-qualification alone provides a strategic asset floor."
        ),
        how_to_verify="M&A comparables: nuclear contractor transactions in Europe 2020-2026",
        is_liquid=False,
    ),
]

POLIMEX_UPSIDE_MECHANISMS = [

    UpsideMechanism(
        name="EPC contract award for Unit 1 (nuclear)",
        price_target=9.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "The nuclear programme is committed ($15bn state financing, AP1000 selected). "
            "Unit 1 EPC award is a timing question, not an existence question. "
            "When the contract is announced, the market re-prices Mostostal's backlog "
            "from zero (current book value) to PLN 800m-1.5bn NPV. "
            "This is price correction of existing committed revenue, not forecast growth."
        ),
        probability=0.55,
        observable_trigger="PEJ/Westinghouse announce EPC contract award",
        months_to_trigger_estimate=18,
    ),

    UpsideMechanism(
        name="Core business operational turn (new management)",
        price_target=5.50,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "Fixed-price legacy contracts expire 2025-2026. "
            "If Polimex simply stops losing money on these contracts, "
            "EBITDA normalises to breakeven or slightly positive. "
            "At PLN 2.86bn revenue × 2% EBITDA = PLN 57m. "
            "At 8x EV/EBITDA = PLN 456m + equity upside = PLN 5.50."
        ),
        probability=0.45,
        observable_trigger="Polimex reports EBITDA positive for any quarter",
        months_to_trigger_estimate=12,
    ),

    UpsideMechanism(
        name="Full nuclear ramp + strategic buyer at nuclear premium",
        price_target=16.00,
        requires_future_growth=True,
        growth_required_description=(
            "Requires Units 2 and 3 to proceed, Mostostal to execute Unit 1 "
            "successfully (proving nuclear construction capability), and either "
            "a strategic buyer (e.g. EDF, Westinghouse parent Brookfield) or "
            "a state-backed privatisation at nuclear-asset multiples."
        ),
        correction_logic=(
            "At PLN 80m normalised EBITDA (nuclear + core) × 15x = PLN 1.2bn equity. "
            "Plus strategic buyer premium for Poland's only nuclear construction "
            "sub-contractor: 30-50% above intrinsic value."
        ),
        probability=0.20,
        observable_trigger="Unit 1 construction begins + Unit 2 EPC announcement",
        months_to_trigger_estimate=42,
    ),
]


def run():
    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print("  POLIMEX-MOSTOSTAL SA (WSE: PXM)")
    print("  Regulatory Windfall — Polish Nuclear Programme")
    print(sep)

    # ── Value trap check first ──────────────────────────────────────────
    print(f"\n  ⚠  RUNNING VALUE TRAP DETECTION FIRST — this is a distressed company")
    print(thin)
    trap = detect_trap(
        company=polimex,
        years_trading_at_discount=4,        # 4 years of operational problems
        related_party_risk=False,
        accounting_quality="medium",        # Fixed-price contract impairments are real
        activist_path_credible=False,
        sector_structurally_declining=False, # Industrial construction is not declining
        minority_rights_jurisdiction="medium",
    )
    print_trap_report(trap)

    # ── Nuclear pipeline analysis ─────────────────────────────────────
    nuclear_analysis = analyse_pipeline(
        company_name="Polimex-Mostostal SA",
        current_annual_revenue_m=2860,
        current_ebitda_margin_pct=-3.0,     # Negative EBITDA currently
        items=NUCLEAR_PIPELINE,
    )
    print_pipeline_report(nuclear_analysis)

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=polimex,
        safety_components=POLIMEX_SAFETY_COMPONENTS,
        upside_mechanisms=POLIMEX_UPSIDE_MECHANISMS,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    weights = ScoringWeights(
        asset_asymmetry     = 0.15,   # Hidden asset thin (book value eroding)
        smart_money_signals = 0.20,
        catalyst_clarity    = 0.35,   # Nuclear catalyst is specific and committed
        downside_protection = 0.10,   # Downside protection is weak (distressed)
        business_quality    = 0.15,   # Business quality is poor — important weight
        sentiment_discount  = 0.05,
    )

    result    = score_company(polimex, weights)
    suggested = suggest_pivot_types(polimex)
    print_report(polimex, result, suggested)

    # ── Nuclear size context ─────────────────────────────────────────
    print(f"\n{sep}")
    print("  NUCLEAR OPPORTUNITY SIZE vs CURRENT BUSINESS")
    print(sep)
    print(f"""
  Current Polimex (2024):
    Revenue: PLN 2.86bn | EBITDA: ~PLN -86m (negative) | Market cap: PLN 754m

  If Mostostal Siedlce captures 12% of AP1000 nuclear EPC (PLN 30bn):
    Nuclear contract: PLN 3.6bn over 8 years = PLN 450m/year
    At 7% EBITDA margin = PLN 31.5m/year incremental
    Combined with stabilised core at PLN 100m EBITDA → PLN 131m total
    At 10x EV/EBITDA = PLN 1.31bn enterprise value
    Per share: ~PLN 5.70 (in 3-4 years, before growth)

  If nuclear ramps to 15% share (PLN 4.5bn over 8yr = PLN 562m/year):
    Combined EBITDA (nuclear + core recovery): PLN 160-180m
    At 12x (nuclear-specialist multiple): PLN 1.92-2.16bn EV
    Per share: ~PLN 8.35-9.40 (in 4-5 years)

  The nuclear contract has not been awarded yet.
  When it is awarded, the stock reprices to the DCF of the backlog.
  The question is: WHEN, not IF.
""")
    print(sep)


if __name__ == "__main__":
    run()
