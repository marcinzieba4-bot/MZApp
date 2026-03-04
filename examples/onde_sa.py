"""
Onde SA (WSE: ONDP)
====================
Thesis: STRATEGIC_REPOSITION + ASSET_RELEASE

Onde SA is a Polish renewable energy EPC (Engineering, Procurement, Construction)
contractor that also acts as a developer of wind and solar projects. The market
is pricing it as a pure EPC contractor (P/S 0.68x, EV/EBITDA ~10x), but buried
inside is a 1.36 GW developer portfolio worth substantially more than the entire
market capitalisation.

Why the market is mispricing this:
  The developer portfolio is NOT on the balance sheet at market value.
  Development rights for wind/solar in Poland are carried at cost (regulatory
  permitting, environmental studies, grid connection fees). The market value
  of a permitted, grid-connected 1 GW+ portfolio is entirely different.

  Comparable transactions in the Polish renewable market:
    - RWE paid €1.2bn for 1.4 GW Nordex/Ekoserwis portfolio (2021)
    - EDF/Électricité de France paid ~PLN 400k-700k per permitted MW in Poland
    - PGE / Polenergia: grid-connected solar at ~PLN 600k-900k/MW
    - Offshore wind development rights: PLN 2m-4m/MW

  Onde's 1.36 GW portfolio at PLN 500k-1m/MW = PLN 680m-1,360m.
  Market cap: PLN 550m (at PLN 10.10/share).
  The developer portfolio is worth MORE than the market cap, even at a discount.

Two overlapping pivots:
  1. ASSET_RELEASE
     The developer portfolio gets sold to an IPP, PE fund, or utility at a
     transaction price that forces the market to recognise its value.
     Comparable deals imply PLN 680m-1.36bn (1.2-2.5x market cap).

  2. STRATEGIC_REPOSITION
     Onde stops being an EPC contractor and becomes an IPP (Independent Power
     Producer) — building projects onto its own balance sheet rather than
     building for others' accounts. This re-rates from EPC multiples (7-10x
     EV/EBITDA) to IPP multiples (12-18x EV/EBITDA or yield-based valuation).

Pipeline certainty layer:
  PSE (Polskie Sieci Elektroenergetyczne — Polish Transmission System Operator)
  published a PLN 64-66bn grid investment plan for 2025-2034: 4,700 km of new
  lines, 28 new substations. This spend is driven by:
    - EU Green Deal obligations (65% renewable by 2030)
    - Balancing new offshore and onshore wind capacity
    - KPO electrification component (legally committed, deadline Aug 2026)
  Onde is a grid connection specialist — this pipeline is their EPC addressable market.

Data as of: March 2026 (approximate; verify against primary sources)
Sources:
  - Onde SA annual report 2024 (seinet.gpw.pl — ESPI)
  - PSE investment plan 2025-2034 (pse.pl)
  - Polish renewable developer transaction comparables
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


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# Shares outstanding: ~54.5m → PLN 550m market cap / PLN 10.10 = 54.5m shares
# Book value: Approximate, equity backed by EPC working capital + developer rights

onde = Company(
    name="Onde SA",
    ticker="ONDP",
    exchange="WSE",
    sector="Renewable Energy EPC & Development",
    country="Poland",

    # ── Price / size ──
    current_price=10.10,     # PLN per share
    market_cap_m=550,        # PLN millions (~PLN 550m)
    currency="PLN",

    # ── Balance sheet anchors ──
    book_value_per_share=7.80,            # ~PLN 425m equity / 54.5m shares
    net_cash_per_share=-1.40,             # PLN net debt: project financing, WC debt
    hidden_asset_value_per_share=14.50,   # Developer portfolio at conservative PLN 550k/MW:
                                          # 1.36 GW × 550k = PLN 748m / 54.5m shares = 13.72
                                          # Use 14.50 including grid connection prepayments

    # ── Earnings profile ──
    ebitda_margin_pct=7.0,      # PLN 56m EBITDA / PLN 804m revenue
    revenue_growth_yoy_pct=12,  # EPC contracts growing with PSE/RE capex wave
    roe_pct=5.5,

    # ── Ownership ──
    insider_ownership_pct=52,     # Founders / management hold ~52%
    institutional_ownership_pct=9, # Under-institutionalised
    float_pct=40,

    # ── Pivot thesis ──
    pivot_types=[
        PivotType.ASSET_RELEASE,          # Primary: developer portfolio sale/crystallisation
        PivotType.STRATEGIC_REPOSITION,   # Secondary: EPC → IPP model transition
        PivotType.REGULATORY_WINDFALL,    # PSE grid investment + EU RE obligations
    ],

    thesis_summary=(
        "Onde is a Polish renewable EPC contractor priced like a low-margin builder, "
        "but it owns a 1.36 GW wind and solar developer portfolio worth PLN 680m-1.36bn "
        "(at market transaction prices of PLN 500k-1m/MW). "
        "The entire market cap is PLN 550m. "
        "The developer portfolio is carried at cost in the accounts (permitting costs, "
        "studies, grid connection fees — not market value). "
        "A single portfolio transaction at even PLN 600k/MW (well below market comps) "
        "would crystallise more value than the current share price. "
        "Separately: the PSE grid investment plan (PLN 64-66bn, 2025-2034) is Onde's "
        "core addressable market — grid connections and high-voltage installation — "
        "and is legally committed by EU-treaty obligations, not a demand forecast. "
        "The stock is pricing in only the EPC business (3-5x EV/EBITDA) and ignoring "
        "the developer portfolio entirely."
    ),

    key_risks=[
        "Developer portfolio monetisation depends on finding a buyer — no guarantee of timing",
        "Polish renewable permitting: new rules (Lex Odległość 2.0) adding uncertainty "
        "to 2025+ wind projects; existing portfolio is pre-permitting so grandfathered",
        "PSE pipeline execution risk: capacity crunch (engineers, grid equipment) could "
        "delay individual projects",
        "Founder-controlled (52%): monetisation requires founder decision to sell",
        "Q1 2025 EBIT negative (PLN -3.9m vs +22.1m prior year): seasonality or "
        "start of margin deterioration — requires monitoring",
        "Renewable energy price risk if Onde transitions to IPP model: Polish RES "
        "auction prices have been falling as more capacity comes online",
        "Grid connection bottleneck: PSE has a ~3-year backlog on connection agreements "
        "which could delay Onde's own IPP development",
    ],

    time_horizon_years=3.0,
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

onde.signals = [

    # Smart money
    PivotSignal(
        name="Insider ownership 52% with founder-controlled development portfolio",
        description=(
            "The founding management team controls 52% and built the developer portfolio "
            "organically. They understand the embedded value better than the market. "
            "No insider selling despite the portfolio being worth more than the stock price. "
            "This is the classic 'patient founder waiting for the right buyer' setup."
        ),
        strength=SignalStrength.MODERATE,
        category="smart_money",
        source="WSE ESPI ownership disclosures",
        confidence=0.85,
    ),
    PivotSignal(
        name="Foreign IPP / utility strategic enquiries (market intelligence)",
        description=(
            "Several foreign utilities (Iberdrola, EDF, RWE, Ørsted) have been active "
            "in Polish developer M&A. Onde's combination of EPC expertise (= construction "
            "certainty for a buyer) + large permitted portfolio is rare in the Polish market."
        ),
        strength=SignalStrength.WEAK,
        category="smart_money",
        confidence=0.35,
    ),

    # Catalyst signals
    PivotSignal(
        name="PSE grid investment plan PLN 64-66bn (2025-2034) — COMMITTED",
        description=(
            "PSE published its 10-year investment plan: PLN 64-66bn, 4,700 km of new "
            "high-voltage lines, 28 new substations. Driven by EU obligations (65% RE "
            "by 2030) + offshore wind Baltic I/II/III grid connection requirements. "
            "Onde is a specialist in HV grid construction and substation installation. "
            "This is not a demand forecast — PSE faces EU financial penalties for failure "
            "to build sufficient grid capacity. The money will be spent."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="PSE investment plan 2025-2034 (pse.pl), published Q4 2024",
        confidence=1.0,
    ),
    PivotSignal(
        name="Polish RE offshore auction round 2025 — drives grid connection need",
        description=(
            "Poland auctioned 5.9 GW of offshore wind in 2025 (Baltic II allocation). "
            "Each GW of offshore wind requires ~1.2 GW of onshore grid reinforcement. "
            "Onde's specialisation in grid-side EPC = direct beneficiary of offshore "
            "wind ramp-up even without owning offshore wind assets."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="URE (Polish Energy Regulatory Office) auction results 2025",
        confidence=0.90,
    ),
    PivotSignal(
        name="Developer portfolio could trigger IAS 36 impairment reversal",
        description=(
            "Under IFRS, development rights cannot be written UP to market value while "
            "held as intangibles. However, a partial sale or IPO/spinoff of the developer "
            "business would force recognition at transaction value. "
            "A single portfolio sale at PLN 600k/MW on 300 MW = PLN 180m gain = 33% of "
            "current market cap from a single transaction."
        ),
        strength=SignalStrength.MODERATE,
        category="catalyst",
        confidence=0.50,
    ),

    # Fundamental signals
    PivotSignal(
        name="Developer portfolio NAV > market cap (2.0-3.5x coverage)",
        description=(
            "1.36 GW × PLN 500k/MW (floor) = PLN 680m vs market cap PLN 550m (1.24x). "
            "1.36 GW × PLN 1.0m/MW (recent transaction comps) = PLN 1,360m (2.47x). "
            "You are buying the EPC business for free if developer portfolio is worth even "
            "PLN 500k/MW. The EPC business generates PLN 56m EBITDA = worth PLN 280-420m "
            "at 5-7.5x EV/EBITDA. So total NAV: PLN 960m-1.78bn vs PLN 550m cap."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.75,
    ),
    PivotSignal(
        name="P/S 0.68x for a company with visible 10-year pipeline",
        description=(
            "Revenue 0.68x is cheap for a contractor with PSE framework access. "
            "By comparison, Polimex-Mostostal (distressed, loss-making) trades at 0.26x. "
            "Onde at 0.68x is mispriced relative to its pipeline quality."
        ),
        strength=SignalStrength.MODERATE,
        category="fundamentals",
        confidence=0.85,
    ),

    # Sentiment signals
    PivotSignal(
        name="Institutional ownership only 9% — under-discovered on WSE",
        description=(
            "Only ~9% institutional ownership vs. ~35% average for WSE mid-cap. "
            "No major Polish or foreign fund has filed a significant position. "
            "This leaves room for substantial re-rating when discovery occurs. "
            "Renewable energy EPC companies in Germany/France trade at 12-15x "
            "EV/EBITDA. Onde at ~10x is the CEE discount, not a fundamental gap."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=0.90,
    ),
    PivotSignal(
        name="Polish renewable energy narrative still early-stage",
        description=(
            "Poland is 12-18 months behind Western Europe in the institutional "
            "recognition that it is the #1 onshore wind + grid opportunity in CE Europe. "
            "When this narrative becomes mainstream, re-rating follows."
        ),
        strength=SignalStrength.MODERATE,
        category="sentiment",
        confidence=0.65,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

onde.scenarios = [

    PriceScenario(
        label="bear",
        price_target=6.50,    # PLN 6.50, -36%
        probability=0.20,
        rationale=(
            "Developer portfolio finds no buyer; EBIT continues negative in 2025-2026. "
            "PSE projects delayed by equipment supply chain. "
            "Multiple compression to 6x EV/EBITDA. "
            "Book value floor at ~PLN 7.80 provides some protection. "
            "This bear case requires the developer portfolio to be worth near zero "
            "AND the PSE pipeline to fail — both highly unlikely simultaneously."
        ),
        time_horizon_years=3.0,
        irr=-14.0,
    ),

    PriceScenario(
        label="base",
        price_target=18.00,   # PLN 18.00, +78%
        probability=0.55,
        rationale=(
            "PSE EPC revenues ramp: Onde captures ~2% of PLN 65bn = PLN 1.3bn over 10yr, "
            "growing EPC EBITDA to PLN 90-100m by 2027. Re-rates to 10-11x EV/EBITDA = "
            "PLN ~1bn EV = PLN 18.35/share. "
            "Developer portfolio remains on balance sheet but is partially recognised "
            "via a 300-500 MW partial sale at ~PLN 650k/MW = PLN 195-325m proceeds "
            "(triggers special dividend or buyback). "
            "No full IPP transformation needed."
        ),
        time_horizon_years=3.0,
        irr=21.0,
    ),

    PriceScenario(
        label="bull",
        price_target=32.00,   # PLN 32.00, +217%
        probability=0.25,
        rationale=(
            "Full developer portfolio sale at PLN 900k/MW = PLN 1.22bn proceeds. "
            "Use proceeds to buy back 40% of shares OR invest in own IPP capacity. "
            "If Onde pivots to IPP, re-rates to 15-18x EV/EBITDA. "
            "Or: foreign utility acquires Onde for the portfolio + EPC capability; "
            "precedent transactions imply 2-3x premium to current price."
        ),
        time_horizon_years=3.0,
        irr=47.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# PSE Grid Pipeline (PLN millions)
# ──────────────────────────────────────────────────────────────────────

ONDE_PIPELINE = [

    PipelineItem(
        name="PSE Grid Investment Plan — HV lines",
        program_name="PSE 10-Year Investment Plan 2025-2034 (HV transmission)",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=35_000,       # ~55% of PLN 64-66bn = transmission lines
        company_addressable_pct=0.022,      # Onde: ~PLN 770m addressable
        company_win_probability=0.35,       # Competitive market, 4-5 players
        company_consortium_share=1.0,
        revenue_start_year=0.5,
        revenue_duration_years=9.0,
        margin_pct=7.5,
        public_source="PSE investment plan 2025-2034 (pse.pl)",
        notes="EU-treaty committed spend; PSE cannot fail to build grid without EU penalty",
    ),

    PipelineItem(
        name="PSE Grid Investment Plan — substations",
        program_name="PSE 2025-2034 (28 new substations + upgrades)",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=15_000,       # Substation allocation estimate
        company_addressable_pct=0.030,      # Onde has substation specialisation
        company_win_probability=0.40,
        company_consortium_share=1.0,
        revenue_start_year=1.0,
        revenue_duration_years=8.0,
        margin_pct=8.0,
        public_source="PSE investment plan 2025-2034",
    ),

    PipelineItem(
        name="KPO RE grid connections (EU Recovery Plan)",
        program_name="KPO Component C1.1 — grid modernisation",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=8_000,        # KPO grid component (EUR-denominated, converted)
        company_addressable_pct=0.025,
        company_win_probability=0.40,
        company_consortium_share=1.0,
        revenue_start_year=0.0,             # Deadline Aug 2026 — urgent
        revenue_duration_years=2.0,
        margin_pct=7.5,
        public_source="KPO (National Recovery Plan) Component C — Polish govt website",
        notes="Aug 2026 EU absorption deadline creates urgency; underspent allocation",
    ),

    PipelineItem(
        name="Baltic I / II offshore wind — grid connection EPC",
        program_name="Polish offshore wind grid connection programme",
        certainty=CertaintyLevel.PLANNED,
        total_program_value_m=12_000,       # Grid connection cost for 5.9 GW Baltic allocation
        company_addressable_pct=0.015,
        company_win_probability=0.30,
        company_consortium_share=1.0,
        revenue_start_year=2.0,
        revenue_duration_years=6.0,
        margin_pct=8.5,
        public_source="URE offshore wind auction results; PSE offshore grid connection plan",
    ),

    PipelineItem(
        name="Onshore RE grid connections (private developers)",
        program_name="Polish onshore wind/solar grid connection backlog (private)",
        certainty=CertaintyLevel.SCHEDULED,
        total_program_value_m=5_000,        # Annual private grid connection spend estimate
        company_addressable_pct=0.040,
        company_win_probability=0.45,
        company_consortium_share=1.0,
        revenue_start_year=0.0,
        revenue_duration_years=5.0,
        margin_pct=7.0,
        public_source="URE annual report; Polish grid connection applications data",
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety
# ──────────────────────────────────────────────────────────────────────

ONDE_SAFETY_COMPONENTS = [

    SafetyComponent(
        name="Book value (EPC working capital + intangibles)",
        value_per_share=7.80,
        confidence=0.80,
        description=(
            "Net assets ~PLN 425m / 54.5m shares = PLN 7.80. "
            "Backed by receivables, WIP, equipment, development cost intangibles."
        ),
        how_to_verify="Onde SA annual report — balance sheet (ESPI)",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Developer portfolio — conservative floor (PLN 500k/MW)",
        value_per_share=12.48,
        confidence=0.60,      # Transaction comparables are real but not guaranteed
        description=(
            "1.36 GW × PLN 500k/MW = PLN 680m / 54.5m shares = PLN 12.48. "
            "This is the FLOOR estimate — actual transaction comps are PLN 700k-1.2m/MW. "
            "Confidence 60% reflects the uncertainty about: (1) the MW that are "
            "genuinely permitted and grid-connected vs in permitting; (2) timing of sale."
        ),
        how_to_verify="Transaction comparables: RWE/Ekoserwis (2021), Polenergia RE deals",
        is_liquid=False,
    ),

    SafetyComponent(
        name="EPC backlog earnings cover",
        value_per_share=3.20,
        confidence=0.75,
        description=(
            "Current EPC order book ~PLN 1.1bn. At 7% EBITDA margin = PLN 77m EBITDA "
            "over 18-24 months. This covers ~3 years of overheads even in a downturn. "
            "Per share: PLN 77m / 54.5m shares × 2.25 earnings years = PLN 3.18."
        ),
        how_to_verify="Onde quarterly results, order book disclosures",
        is_liquid=False,
    ),
]

ONDE_UPSIDE_MECHANISMS = [

    UpsideMechanism(
        name="Portfolio sale at PLN 650k/MW to foreign utility",
        price_target=22.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "1.36 GW × PLN 650k/MW = PLN 884m proceeds. After tax ~PLN 750m. "
            "If distributed: PLN 13.76/share special dividend. Remaining EPC business "
            "worth ~PLN 280m (5x EV/EBITDA). Total: PLN 14 + PLN 5.14 = ~PLN 19/share. "
            "The assets already exist. This is price correction, not growth."
        ),
        probability=0.35,
        observable_trigger="Press release: binding offer or exclusivity agreement on developer portfolio",
        months_to_trigger_estimate=18,
    ),

    UpsideMechanism(
        name="PSE pipeline de-risks EPC earnings → re-rating to 12x",
        price_target=16.50,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "PSE COMMITTED spend = demand exists. Onde capturing 2% of PLN 65bn = "
            "PLN 1.3bn over 10yr = PLN 130m/yr revenue at 7.5% = PLN 9.75m EBITDA incremental. "
            "Plus existing EPC base: EBITDA reaches PLN 90m by 2027. "
            "At 12x EV/EBITDA = PLN 1.08bn EV = PLN 19.82/share (less net debt). "
            "The PSE spend is not a forecast — it is a regulatory obligation."
        ),
        probability=0.55,
        observable_trigger="Onde reports PLN 80m+ EBITDA for any 12-month period",
        months_to_trigger_estimate=24,
    ),

    UpsideMechanism(
        name="Full IPP transition + re-rating to developer multiple",
        price_target=32.00,
        requires_future_growth=True,
        growth_required_description=(
            "Requires Onde to: (1) retain the developer portfolio rather than selling, "
            "(2) secure project financing for development, (3) achieve commissioning "
            "and PPAs/RES auction contracts. Timeline 3-5 years."
        ),
        correction_logic=(
            "At 500 MW commissioned (37% of portfolio): PLN 250m capacity at "
            "9% yield on LCOE investment = PLN 22.5m EBITDA from own generation. "
            "Add EPC: PLN 90m. Total PLN 112m at 15x (IPP multiple) = PLN 1.68bn EV."
        ),
        probability=0.20,
        observable_trigger="Onde announces FID (Final Investment Decision) on own-balance-sheet project ≥100 MW",
        months_to_trigger_estimate=36,
    ),
]


def run():
    print("\n" + "═"*76)
    print("  ONDE SA (WSE: ONDP)")
    print("  Strategic Reposition + Asset Release")
    print("  " + "─"*72)

    # ── Pipeline analysis ─────────────────────────────────────────────
    pse_analysis = analyse_pipeline(
        company_name="Onde SA",
        current_annual_revenue_m=804,
        current_ebitda_margin_pct=7.0,
        items=ONDE_PIPELINE,
    )
    print_pipeline_report(pse_analysis)

    # ── Developer portfolio valuation ────────────────────────────────
    sep  = "═" * 76
    thin = "─" * 76
    print(f"\n{sep}")
    print("  DEVELOPER PORTFOLIO VALUATION — The Hidden Asset")
    print(sep)
    portfolio_mw = 1360
    scenarios = [
        ("Floor (PLN 500k/MW)",    500_000,  "Distressed sale / partial development rights"),
        ("Conservative (700k/MW)", 700_000,  "Recent onshore wind comps (granted permitting)"),
        ("Central (900k/MW)",      900_000,  "Grid-connected, grid agreement in place"),
        ("Premium (1.2m/MW)",    1_200_000,  "Offshore adjacent / RES-auctioned premium"),
    ]
    shares = 54.5  # millions
    market_cap = 550  # PLN millions

    print(f"\n  Portfolio size: {portfolio_mw:,} MW  |  Market cap: PLN {market_cap}m  "
          f"|  Shares: {shares}m")
    print(f"\n  {'Scenario':<30} {'Portfolio Value':>16}  {'Per Share':>10}  "
          f"{'vs Market Cap':>14}  {'Multiple'}  ")
    print(f"  {'-'*30} {'-'*16}  {'-'*10}  {'-'*14}  {'-'*8}")
    for label, price_per_mw, note in scenarios:
        total_m = portfolio_mw * price_per_mw / 1_000_000
        per_share = total_m / shares
        ratio = total_m / market_cap
        print(f"  {label:<30} PLN {total_m:>10,.0f}m  {per_share:>8.2f} PLN  "
              f"{ratio:>12.2f}x  {note}")
    print(f"\n  Conclusion: even at the floor estimate, portfolio value = 1.24x market cap.")
    print(f"  The EPC business (PLN 56m EBITDA × 7x = PLN 392m) is being given away.")
    print(sep)

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=onde,
        safety_components=ONDE_SAFETY_COMPONENTS,
        upside_mechanisms=ONDE_UPSIDE_MECHANISMS,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    weights = ScoringWeights(
        asset_asymmetry     = 0.35,   # Developer portfolio hidden asset is the crux
        smart_money_signals = 0.15,
        catalyst_clarity    = 0.25,   # PSE commitment + portfolio sale potential
        downside_protection = 0.10,
        business_quality    = 0.10,
        sentiment_discount  = 0.05,
    )

    result    = score_company(onde, weights)
    suggested = suggest_pivot_types(onde)
    print_report(onde, result, suggested)


if __name__ == "__main__":
    run()
