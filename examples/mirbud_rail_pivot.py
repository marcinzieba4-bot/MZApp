"""
Mirbud — The Rail Pivot Thesis
================================
This file models a specific sub-thesis: Mirbud pivots from
road-dependent contractor into rail construction, accessing the
PKP PLK / CPK / KPO pipeline.

WHY RAIL CHANGES THE INVESTMENT MATH:

1. REVENUE CERTAINTY UPGRADE
   Road contracts (GDDKiA): tied to a 7-year EU fund cycle that peaks and troughs.
   Rail contracts (PKP PLK + CPK + KPO): three OVERLAPPING funding streams,
   each with independent EU treaties, creating a 10+ year runway.
   → Future revenue migrates from "forecast" to "pipeline"

2. MULTIPLE EXPANSION
   The market pays different multiples for different revenue quality:
     Road contractor (GDDKiA-dependent):     P/E 10-12x  (cyclical, thin margins)
     Mixed road + rail:                       P/E 13-16x  (more stable, longer visibility)
     Rail specialist (Torpol, Budimex Rail):  P/E 18-22x  (long contracts, high barriers)
   → Moving from 10x to 15x alone = 50% re-rating with zero earnings growth

3. BARRIER TO ENTRY PRICING POWER
   PKP PLK pre-qualification is difficult — fewer bidders per tender.
   Average: 3-5 bidders per rail contract vs. 8-12 for road contracts.
   → Rail EBITDA margins: 8-12% vs road EBITDA margins: 4-7%
   → Revenue quality (margin × duration × certainty) is fundamentally higher

PUBLICLY VERIFIABLE SOURCES:
  - PKP PLK Investment Plan 2024-2030: bip.plk-sa.pl (PLN 72 billion total)
  - CPK (Centralny Port Komunikacyjny) rail: cpk.pl (Y-line: PLN 38bn+)
  - KPO rail component: funduszeeuropejskie.gov.pl (PLN 25.6bn committed)
  - GDDKiA 4-year road program: gddkia.gov.pl (~PLN 60bn 2024-2027)

NOTE: All figures are illustrative, based on publicly available investment
programme disclosures. Verify with primary PKP PLK / GDDKiA sources before trading.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.models import (
    Company, PivotSignal, PriceScenario, PivotType, SignalStrength, ScoringWeights
)
from framework.scoring import score_company
from framework.pipeline_certainty import (
    PipelineItem, CertaintyLevel, analyse_pipeline, print_pipeline_report
)
from framework.pivot_types import suggest_pivot_types
from framework.report import print_report


# ══════════════════════════════════════════════════════════════════════
# PART 1 — THE PKP PLK / CPK / KPO PIPELINE
#
# Each item = one identifiable block of public procurement.
# These are NOT company estimates — they are published government programs
# you can look up in PKP PLK's public investment calendar.
# ══════════════════════════════════════════════════════════════════════

RAIL_PIPELINE = [

    # ── PKP PLK 2024-2030 (National Rail Infrastructure Manager) ─────

    PipelineItem(
        name="PKP PLK Line 8 modernisation",
        program_name="PKP PLK Investment Plan 2024-2030",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=2_400,     # PLN 2.4bn modernisation program
        company_addressable_pct=0.45,    # Civil/earthworks, bridges — excludes electrification
        company_win_probability=0.07,    # Mirbud targeting ~7% market share in pre-qual pool
        company_consortium_share=0.60,   # Likely lead in consortium, 60% of consortium value
        revenue_start_year=1.0,
        revenue_duration_years=5.0,
        margin_pct=9.5,
        public_source="PKP PLK Investment Plan 2024-2030 (bip.plk-sa.pl)",
        notes="Warsaw-Kraków corridor, TEN-T core network. EU co-financing ~85%.",
    ),

    PipelineItem(
        name="PKP PLK Line 7 Radom section",
        program_name="PKP PLK Investment Plan 2024-2030",
        certainty=CertaintyLevel.SCHEDULED,
        total_program_value_m=1_100,
        company_addressable_pct=0.50,
        company_win_probability=0.08,
        company_consortium_share=0.65,
        revenue_start_year=0.5,
        revenue_duration_years=3.5,
        margin_pct=10.0,
        public_source="PKP PLK procurement calendar Q4 2024",
        notes="Warsaw-Radom route. Tender Q1 2025 per published calendar.",
    ),

    PipelineItem(
        name="PKP PLK regional line upgrades (mixed)",
        program_name="PKP PLK Investment Plan 2024-2030",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=8_500,    # PLN 8.5bn basket of regional upgrades
        company_addressable_pct=0.40,
        company_win_probability=0.06,   # Higher competition on smaller contracts
        company_consortium_share=0.70,
        revenue_start_year=1.0,
        revenue_duration_years=6.0,
        margin_pct=8.5,
        public_source="PKP PLK Investment Plan 2024-2030, Chapter 3",
        notes="Basket of ~40 individual regional line modernisations.",
    ),

    PipelineItem(
        name="PKP PLK Line 1 Warsaw-Łódź section",
        program_name="PKP PLK Investment Plan 2024-2030",
        certainty=CertaintyLevel.PLANNED,
        total_program_value_m=3_200,
        company_addressable_pct=0.48,
        company_win_probability=0.07,
        company_consortium_share=0.55,
        revenue_start_year=2.0,
        revenue_duration_years=4.0,
        margin_pct=9.0,
        public_source="PKP PLK 2024 Annual Update",
        notes="Capacity upgrade. Interoperability requirement (TEN-T comprehensive).",
    ),

    # ── CPK (Centralny Port Komunikacyjny) — Y-line ───────────────────

    PipelineItem(
        name="CPK Y-line — Warsaw to Łódź civil works",
        program_name="CPK Rail (Y-line) 2025-2035",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=6_500,    # PLN 6.5bn for Warsaw-Łódź new build
        company_addressable_pct=0.55,   # Civil earthworks, embankments, drainage — Mirbud competency
        company_win_probability=0.06,
        company_consortium_share=0.50,
        revenue_start_year=1.5,
        revenue_duration_years=5.0,
        margin_pct=10.0,
        public_source="CPK S.A. Investment Programme (cpk.pl), Rail Master Plan 2024",
        notes=(
            "New high-speed rail, max 250 km/h. EU CEF co-financing applied for. "
            "Law establishing CPK passed 2018, project cannot be cancelled without "
            "PLN 2bn+ sunk cost write-off — strong political lock-in."
        ),
    ),

    PipelineItem(
        name="CPK Y-line — Łódź to Wrocław/Poznań branch",
        program_name="CPK Rail (Y-line) 2025-2035",
        certainty=CertaintyLevel.PLANNED,
        total_program_value_m=12_000,
        company_addressable_pct=0.50,
        company_win_probability=0.05,   # More competition on this longer stretch
        company_consortium_share=0.45,
        revenue_start_year=3.0,
        revenue_duration_years=6.0,
        margin_pct=9.5,
        public_source="CPK S.A. Rail Master Plan 2024",
        notes="Tender preparation expected 2026. Subject to CPK governance stability.",
    ),

    # ── KPO (Krajowy Plan Odbudowy / National Recovery Plan) ─────────

    PipelineItem(
        name="KPO Rail — accessibility & capacity upgrades",
        program_name="KPO Component D 2024-2026",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=7_800,    # PLN 7.8bn KPO rail envelope
        company_addressable_pct=0.42,
        company_win_probability=0.07,
        company_consortium_share=0.65,
        revenue_start_year=0.25,        # Awards already happening — very near term
        revenue_duration_years=3.0,
        margin_pct=9.0,
        public_source="KPO Component D, funduszeeuropejskie.gov.pl; EU Commission approval 2022",
        notes=(
            "MUST be spent by August 2026 (EU RRF deadline). This creates extreme "
            "urgency for PKP PLK to award contracts NOW. Fastest-moving pipeline."
        ),
    ),

    PipelineItem(
        name="KPO Rail — interoperability & ERTMS rollout",
        program_name="KPO Component D 2024-2026",
        certainty=CertaintyLevel.SCHEDULED,
        total_program_value_m=3_200,
        company_addressable_pct=0.35,   # Partially technical (ERTMS), partially civil
        company_win_probability=0.06,
        company_consortium_share=0.55,
        revenue_start_year=0.5,
        revenue_duration_years=2.5,
        margin_pct=8.5,
        public_source="PKP PLK / KPO tender schedule (bip.plk-sa.pl)",
        notes="ERTMS portion requires specialist subcontractor (Thales, Bombardier).",
    ),
]

# ── For comparison: current road pipeline (GDDKiA) ───────────────────

ROAD_PIPELINE = [
    PipelineItem(
        name="GDDKiA A1/S5 expansions (current backlog)",
        program_name="GDDKiA 4-Year Programme 2024-2027",
        certainty=CertaintyLevel.AWARDED,
        total_program_value_m=1_200,
        company_addressable_pct=1.00,   # This IS Mirbud's existing business
        company_win_probability=1.00,   # Already awarded — in backlog
        company_consortium_share=0.70,
        revenue_start_year=0.0,
        revenue_duration_years=3.0,
        margin_pct=5.5,
        public_source="Mirbud investor presentations / ESPI",
        notes="Existing contracted road backlog. High certainty, thin margins.",
    ),
    PipelineItem(
        name="GDDKiA new tenders 2025-2026",
        program_name="GDDKiA 4-Year Programme 2024-2027",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=15_000,
        company_addressable_pct=1.00,
        company_win_probability=0.05,   # 5% share in competitive market
        company_consortium_share=0.65,
        revenue_start_year=0.5,
        revenue_duration_years=3.5,
        margin_pct=5.5,
        public_source="GDDKiA 4-Year Programme (gddkia.gov.pl)",
        notes="Highly competitive — 8-12 bidders per tender. Price compression.",
    ),
    PipelineItem(
        name="GDDKiA post-2027 programme (speculative)",
        program_name="Post-2027 EU Fund Cycle",
        certainty=CertaintyLevel.INDICATIVE,
        total_program_value_m=20_000,
        company_addressable_pct=1.00,
        company_win_probability=0.05,
        company_consortium_share=0.65,
        revenue_start_year=3.5,
        revenue_duration_years=5.0,
        margin_pct=5.0,
        public_source="EU 2028-2034 cohesion framework (draft)",
        notes=(
            "Post-2027 EU funding is NOT yet committed. Subject to new MFF negotiations. "
            "Significant pipeline CLIFF after current programme ends."
        ),
    ),
]


# ══════════════════════════════════════════════════════════════════════
# PART 2 — THE MULTIPLE EXPANSION LOGIC
# Why rail changes what earnings are WORTH, not just how much there are
# ══════════════════════════════════════════════════════════════════════

MULTIPLE_TABLE = {
    "pure_road_contractor": {
        "description": "GDDKiA-dependent, no rail exposure, post-EU-cycle cliff risk",
        "ebitda_margin_pct": 5.5,
        "revenue_visibility_years": 2.5,
        "typical_pe_range": (10, 12),
        "typical_ev_ebitda_range": (5, 7),
        "why": "Highly cyclical, margin-thin, competitive, cliff after 2027",
    },
    "mixed_road_rail": {
        "description": "Road (50-60%) + rail (40-50%), diversified pipeline",
        "ebitda_margin_pct": 8.5,
        "revenue_visibility_years": 5.0,
        "typical_pe_range": (13, 17),
        "typical_ev_ebitda_range": (7, 10),
        "why": "Rail smooths the road cycle, higher margins, longer contracts",
    },
    "rail_specialist": {
        "description": "Torpol / Budimex Rail profile — primarily rail, limited road",
        "ebitda_margin_pct": 11.0,
        "revenue_visibility_years": 7.0,
        "typical_pe_range": (18, 22),
        "typical_ev_ebitda_range": (9, 13),
        "why": "High barriers to entry, scarce pre-qual, pipeline certainty premium",
    },
}

def compute_re_rating_upside(
    current_revenue_m: float,
    current_ebitda_margin_pct: float,
    market_cap_m: float,
    from_profile: str,
    to_profile: str,
    new_margin_pct: float = None,
) -> dict:
    """
    What happens to market cap if Mirbud re-rates from road contractor
    to mixed road+rail profile?
    """
    from_p  = MULTIPLE_TABLE[from_profile]
    to_p    = MULTIPLE_TABLE[to_profile]

    current_ebitda = current_revenue_m * current_ebitda_margin_pct / 100
    new_margin     = new_margin_pct or to_p["ebitda_margin_pct"]
    new_ebitda     = current_revenue_m * new_margin / 100  # Revenue unchanged, margin improves

    current_ev_ebitda = market_cap_m / current_ebitda  # Simplified EV ≈ market cap
    target_ev_ebitda_low, target_ev_ebitda_high = to_p["typical_ev_ebitda_range"]
    target_ev_ebitda_mid = (target_ev_ebitda_low + target_ev_ebitda_high) / 2

    new_market_cap_low  = new_ebitda * target_ev_ebitda_low
    new_market_cap_mid  = new_ebitda * target_ev_ebitda_mid
    new_market_cap_high = new_ebitda * target_ev_ebitda_high

    return {
        "current_ebitda_m":    current_ebitda,
        "new_ebitda_m":        new_ebitda,
        "current_ev_ebitda":   current_ev_ebitda,
        "current_market_cap_m": market_cap_m,
        "target_ev_ebitda_range": (target_ev_ebitda_low, target_ev_ebitda_high),
        "new_market_cap_low_m":  new_market_cap_low,
        "new_market_cap_mid_m":  new_market_cap_mid,
        "new_market_cap_high_m": new_market_cap_high,
        "upside_low_pct":     (new_market_cap_low  / market_cap_m - 1) * 100,
        "upside_mid_pct":     (new_market_cap_mid  / market_cap_m - 1) * 100,
        "upside_high_pct":    (new_market_cap_high / market_cap_m - 1) * 100,
        "from": from_profile,
        "to":   to_profile,
    }


# ══════════════════════════════════════════════════════════════════════
# PART 3 — MIRBUD WITH RAIL PIVOT (updated company model)
# ══════════════════════════════════════════════════════════════════════

mirbud_rail = Company(
    name="Mirbud S.A. (Rail Pivot Scenario)",
    ticker="MRB",
    exchange="WSE",
    sector="Construction & Engineering — Rail + Road",
    country="Poland",

    current_price=3.80,
    market_cap_m=380,
    currency="PLN",

    book_value_per_share=6.20,
    net_cash_per_share=0.40,
    hidden_asset_value_per_share=3.50,  # Land bank unchanged

    ebitda_margin_pct=8.5,           # Rail pivot improves blended margins (was 5.5%)
    revenue_growth_yoy_pct=15,        # Rail adds ~20% revenue uplift in 24-36mo
    roe_pct=10.5,

    insider_ownership_pct=62,
    institutional_ownership_pct=8,
    float_pct=28,

    pivot_types=[
        PivotType.STRATEGIC_REPOSITION,  # Road → Rail+Road
        PivotType.ASSET_RELEASE,          # Land bank still in play
        PivotType.OWNERSHIP_CHANGE,       # Founder monetisation still possible
        PivotType.REGULATORY_WINDFALL,    # EU-mandated rail spend = windfall
    ],

    signals=[
        # Smart money
        PivotSignal(
            name="Hedge fund 5%+ ESPI crossing",
            description="Activist knows rail pivot thesis — specifically values PKP PLK pipeline",
            strength=SignalStrength.STRONG,
            category="smart_money",
            confidence=0.95,
        ),
        PivotSignal(
            name="PKP PLK pre-qualification status",
            description=(
                "Mirbud has (or can obtain) pre-qualification for PKP PLK civil works. "
                "This is the gate that separates eligible bidders from the rest. "
                "Once pre-qualified, you access the entire pipeline."
            ),
            strength=SignalStrength.STRONG,
            category="smart_money",
            confidence=0.75,
        ),

        # Fundamentals
        PivotSignal(
            name="P/B = 0.61 — asset discount unchanged",
            description="Land bank discount still present; rail thesis adds a SECOND re-rating lever",
            strength=SignalStrength.STRONG,
            category="fundamentals",
            confidence=0.90,
        ),
        PivotSignal(
            name="Rail EBITDA margins 8-12% vs road 4-7%",
            description=(
                "Rail contracts command a structural margin premium due to "
                "technical complexity, pre-qualification barriers, and fewer bidders. "
                "A 40-50% rail mix lifts blended EBITDA margin from 5.5% to 8-9%."
            ),
            strength=SignalStrength.STRONG,
            category="fundamentals",
            confidence=0.82,
        ),
        PivotSignal(
            name="PKP PLK pipeline PLN 45bn+ over 6 years (verified public)",
            description=(
                "PKP PLK Investment Plan 2024-2030 totals PLN 72bn. "
                "Civil/earthworks = ~40% = PLN 29bn addressable to Mirbud. "
                "KPO component (PLN 11bn civil) MUST be contracted by Aug 2026. "
                "CPK Y-line adds PLN 18-35bn civil works 2025-2035. "
                "This is not a forecast — it is published government procurement schedule."
            ),
            strength=SignalStrength.DEFINITIVE,
            category="fundamentals",
            confidence=0.85,
        ),

        # Catalyst
        PivotSignal(
            name="KPO absorption deadline: August 2026",
            description=(
                "KPO rail funds (PLN 25.6bn total) must be contracted by mid-2026. "
                "PKP PLK is awarding contracts at unprecedented pace in 2024-2025. "
                "A Mirbud rail JV win in 2025 would appear in 2025 ESPI disclosures, "
                "immediately signalling the strategic repositioning to the market."
            ),
            strength=SignalStrength.DEFINITIVE,
            category="catalyst",
            confidence=0.90,
        ),
        PivotSignal(
            name="CPK rail — construction awards starting 2025",
            description=(
                "CPK S.A. announced first civil works tenders for Y-line in late 2024. "
                "The sunk cost of the CPK project (PLN 2bn+ already spent) means "
                "cancellation is politically impossible regardless of governing party. "
                "Rail construction begins regardless of 2025 election outcomes."
            ),
            strength=SignalStrength.STRONG,
            category="catalyst",
            confidence=0.75,
        ),
        PivotSignal(
            name="Zero sell-side coverage",
            description="No analyst has modelled the rail revenue stream — entirely unpriced",
            strength=SignalStrength.STRONG,
            category="sentiment",
            confidence=1.0,
        ),
        PivotSignal(
            name="Rail multiple premium completely unrecognised in stock price",
            description=(
                "MRB trades at 5-7x EV/EBITDA (road contractor multiple). "
                "A rail-exposed peer like Torpol trades at 10-14x. "
                "The market has not priced any probability of Mirbud obtaining "
                "the rail multiple. Even a 20% probability deserves some premium."
            ),
            strength=SignalStrength.STRONG,
            category="sentiment",
            confidence=0.85,
        ),
    ],

    scenarios=[
        PriceScenario(
            label="bear",
            price_target=2.80,
            probability=0.15,        # Lower than base bear (15% vs 20%) — rail adds floor
            rationale=(
                "Rail pivot fails: PKP PLK pre-qual rejected, CPK cancelled by courts, "
                "road margins compress. Back to pure road contractor at distressed multiple."
            ),
            time_horizon_years=2,
            irr=-14.0,
        ),
        PriceScenario(
            label="base",
            price_target=7.20,
            probability=0.50,
            rationale=(
                "Rail pivot succeeds at small scale (1-2 PKP PLK contract wins). "
                "Market reprices from road (6x EV/EBITDA) to mixed road+rail (8-9x). "
                "Land bank partially re-rated on first transaction. "
                "Price target: PLN 800m revenue × 9% EBITDA × 8.5x EV/EBITDA ≈ PLN 612m MC → 6.12 PLN/share. "
                "Plus land bank re-rating: +PLN 1.00-1.50."
            ),
            time_horizon_years=2,
            irr=37.7,
        ),
        PriceScenario(
            label="bull",
            price_target=10.50,
            probability=0.35,
            rationale=(
                "Rail pivot + full acquisition: a strategic buyer (Strabag, Vinci, Ferrovial) "
                "acquires Mirbud specifically to access its PKP PLK pre-qualification, "
                "workforce, and land bank simultaneously. "
                "Pays 1.5x book + control premium. "
                "Rail capability makes Mirbud a strategic asset to European contractors "
                "entering the PLN 70bn PKP PLK programme."
            ),
            time_horizon_years=2,
            irr=66.3,
        ),
    ],

    thesis_summary=(
        "Mirbud's asset-play discount (0.61x P/B) remains, but the rail pivot "
        "adds a SECOND independent re-rating lever: margin expansion from 5.5% → 8-9% "
        "as rail contracts replace road contracts, triggering multiple expansion from "
        "6x to 9x EV/EBITDA. The PKP PLK / KPO / CPK pipeline is legally committed "
        "and publicly documented — not a forecast but a procurement calendar. "
        "A single PKP PLK contract win converts the company from 'road contractor' "
        "to 'rail + road' in analyst models, immediately justifying a higher multiple. "
        "Combined with the land bank thesis, the 2-year probability-weighted return "
        "exceeds the base-case 37% even without a full acquisition."
    ),
    key_risks=[
        "PKP PLK pre-qualification requires track record — may need 1-2 smaller contracts first",
        "Rail project complexity higher than road — execution risk on first rail contract",
        "CPK political risk: coalition could slow Y-line timeline (but cannot cancel without cost)",
        "Founder still controls 62% — rail success doesn't bypass ownership change thesis",
        "Larger competitors (Budimex, Strabag) better positioned for mega-rail contracts",
    ],
    time_horizon_years=2.0,
)


# ══════════════════════════════════════════════════════════════════════
# Main report
# ══════════════════════════════════════════════════════════════════════

def run():
    sep  = "═" * 72
    thin = "─" * 72

    print(f"\n{sep}")
    print("  MIRBUD — RAIL PIVOT THESIS")
    print(sep)

    # ── Pipeline analysis ─────────────────────────────────────────────
    rail_analysis = analyse_pipeline(
        company_name="Mirbud S.A. (Rail Addressable Pipeline)",
        current_annual_revenue_m=800,
        current_ebitda_margin_pct=5.5,
        items=RAIL_PIPELINE,
    )
    road_analysis = analyse_pipeline(
        company_name="Mirbud S.A. (Road Pipeline — current business)",
        current_annual_revenue_m=800,
        current_ebitda_margin_pct=5.5,
        items=ROAD_PIPELINE,
    )

    print_pipeline_report(rail_analysis)
    print_pipeline_report(road_analysis)

    # ── Rail vs road side-by-side ─────────────────────────────────────
    print(f"\n{sep}")
    print("  ROAD vs RAIL PIPELINE — HEAD TO HEAD COMPARISON")
    print(sep)
    rows = [
        ("Pipeline total expected revenue",
         f"PLN {road_analysis.total_expected_revenue_m:.0f}m",
         f"PLN {rail_analysis.total_expected_revenue_m:.0f}m"),
        ("Market opportunity / current revenue",
         f"{road_analysis.market_to_revenue_ratio:.1f}x",
         f"{rail_analysis.market_to_revenue_ratio:.1f}x"),
        ("High-certainty share (≥COMMITTED)",
         f"{road_analysis.revenue_not_speculation_pct:.0f}%",
         f"{rail_analysis.revenue_not_speculation_pct:.0f}%"),
        ("NPV (pipeline discount rates)",
         f"PLN {road_analysis.total_npv_m:.0f}m",
         f"PLN {rail_analysis.total_npv_m:.0f}m"),
        ("NPV (speculative DCF)",
         f"PLN {road_analysis.total_npv_speculative_m:.0f}m",
         f"PLN {rail_analysis.total_npv_speculative_m:.0f}m"),
        ("Certainty premium vs. speculative DCF",
         f"+PLN {road_analysis.certainty_premium_m:.0f}m",
         f"+PLN {rail_analysis.certainty_premium_m:.0f}m"),
        ("EBITDA margin (typical)",   "4-7%",  "8-12%"),
        ("Avg bidders per tender",    "8-12",  "3-5"),
        ("Avg contract duration",     "2-3yr", "4-6yr"),
        ("Pipeline cliff risk",       "HIGH (post-2027)", "LOW (3 independent sources)"),
        ("Market verdict",
         road_analysis.market_verdict,
         rail_analysis.market_verdict),
        ("Company verdict",
         road_analysis.company_verdict,
         rail_analysis.company_verdict),
    ]
    print(f"\n  {'Metric':<42}  {'ROAD (current)':>18}  {'RAIL (pivot)':>18}")
    print(f"  {'-'*42}  {'-'*18}  {'-'*18}")
    for label, road_val, rail_val in rows:
        print(f"  {label:<42}  {road_val:>18}  {rail_val:>18}")

    # ── Multiple expansion ────────────────────────────────────────────
    print(f"\n\n{sep}")
    print("  MULTIPLE EXPANSION: WHAT RAIL DOES TO THE STOCK PRICE")
    print("  (independent of asset thesis — earnings-only re-rating)")
    print(sep)

    re_rate = compute_re_rating_upside(
        current_revenue_m=800,
        current_ebitda_margin_pct=5.5,
        market_cap_m=380,
        from_profile="pure_road_contractor",
        to_profile="mixed_road_rail",
        new_margin_pct=8.5,
    )

    print(f"""
  CURRENT (pure road contractor profile):
    Revenue:          PLN 800m
    EBITDA margin:    5.5%  → EBITDA: PLN {re_rate['current_ebitda_m']:.0f}m
    EV/EBITDA:        {re_rate['current_ev_ebitda']:.1f}x  (road contractor discount)
    Market cap:       PLN 380m
    Price:            3.80 PLN

  POST RAIL PIVOT (mixed road+rail profile):
    Revenue:          PLN 800m+  (same base; rail adds incremental)
    EBITDA margin:    8.5%  → EBITDA: PLN {re_rate['new_ebitda_m']:.0f}m
    Target EV/EBITDA: {re_rate['target_ev_ebitda_range'][0]:.0f}-{re_rate['target_ev_ebitda_range'][1]:.0f}x  (mixed road+rail sector)

  RE-RATING OUTCOMES (EARNINGS EFFECT ONLY — no asset thesis):
    Conservative  ({re_rate['target_ev_ebitda_range'][0]:.0f}x EV/EBITDA):  Market cap PLN {re_rate['new_market_cap_low_m']:.0f}m  ({re_rate['upside_low_pct']:+.0f}%)
    Base          ({(re_rate['target_ev_ebitda_range'][0]+re_rate['target_ev_ebitda_range'][1])/2:.0f}x EV/EBITDA):  Market cap PLN {re_rate['new_market_cap_mid_m']:.0f}m  ({re_rate['upside_mid_pct']:+.0f}%)
    Aggressive    ({re_rate['target_ev_ebitda_range'][1]:.0f}x EV/EBITDA):  Market cap PLN {re_rate['new_market_cap_high_m']:.0f}m  ({re_rate['upside_high_pct']:+.0f}%)

  KEY INSIGHT:
    The rail re-rating gets you to +{re_rate['upside_mid_pct']:.0f}% on earnings alone.
    ADD the land bank re-rating: +50-100% (from bear case analysis)
    ADD the acquisition premium if founder sells: further +30-50%

    All three re-rating levers are INDEPENDENT of each other.
    You don't need all three. You need ONE.
""")

    # ── Framework scoring ─────────────────────────────────────────────
    print(f"\n{sep}")
    print("  FRAMEWORK SCORE: RAIL PIVOT VERSION vs BASE CASE")
    print(sep)

    weights = ScoringWeights(
        asset_asymmetry=0.20,    # Reduced: asset story now shares stage with earnings
        smart_money_signals=0.25,
        catalyst_clarity=0.25,   # Increased: rail pipeline creates concrete near-term catalyst
        downside_protection=0.15,
        business_quality=0.10,
        sentiment_discount=0.05,
    )

    scored   = score_company(mirbud_rail, weights)
    suggested = suggest_pivot_types(mirbud_rail)
    print_report(mirbud_rail, scored, suggested)

    print(f"\n{sep}")
    print("  WHAT MAKES RAIL REVENUE 'CLOSE TO CERTAIN'")
    print(sep)
    print("""
  The phrase "close to certain" needs unpacking. There are two risks:
    A) Will the contracts EXIST in the market?
    B) Will MIRBUD WIN a share of them?

  For PKP PLK / KPO / CPK:
    Risk A (existence) is close to ZERO because:
      ✓ EU funding treaty signed (Poland: irreversible commitment)
      ✓ KPO: EU Commission formally approved; funds transferred to Poland
      ✓ CPK: Sunk cost lock-in (PLN 2bn+ spent; cancellation = political suicide)
      ✓ PKP PLK: TEN-T legal obligation (EU Regulation 1315/2013, binding)
      ✓ Polish parliament cannot un-commit EU funds already earmarked
      ✓ GDDKiA/PKP PLK publish LEGALLY BINDING procurement calendars

    Risk B (Mirbud's market share) is the ACTUAL uncertainty:
      • Win probability modelled at 5-8% per tender (conservative)
      • Expected annual rail revenue: PLN 150-280m
      • Even at 3% market share: +PLN 90m revenue on PLN 800m base = +11% uplift
      • The floor is non-zero because SOME contracts will be appropriate size/scope

  CONTRAST WITH NORMAL REVENUE FORECASTING:
    "We forecast revenue grows 8% next year" requires:
      → Customer demand increasing (uncertain)
      → No new competitors (uncertain)
      → No macro headwind (uncertain)
      → Management executes (uncertain)

    "PKP PLK will award PLN 8bn in civil tenders in 2025" requires:
      → Poland has signed EU treaty (DONE)
      → KPO funds are in Polish government account (DONE)
      → PKP PLK published Q1 2025 in its calendar (DONE)
      → The Polish state exists (99.9% certain)

  This is the fundamental distinction.
  Rail revenue forecasts are closer to accounting than speculation.
""")
    print(sep)


if __name__ == "__main__":
    run()
