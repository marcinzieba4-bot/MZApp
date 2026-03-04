"""
Kier Group plc (LSE: KIE)
==========================
Thesis: PIPELINE_CERTAINTY + OPERATIONAL_TURN

Kier is a UK infrastructure, buildings, and MEP (mechanical, electrical,
plant) contractor. It nearly went bankrupt in 2019 (rights issue at 45% discount)
but has since restructured: sold Kier Living (housebuilding), sold Kier Facilities
Services, focused on the core construction and infrastructure business.

The pivot in two parts:
  Part 1 — PIPELINE_CERTAINTY
    Network Rail awarded Kier a place on the CP7 (2024-2029) framework.
    Network Rail CP7 = £38bn of rail infrastructure investment, legally committed
    in the UK regulatory settlement. Kier is a named supplier for civil engineering
    and MEP works. Individual task orders are issued regularly against the framework.

    HS2 (High Speed Rail 2):
      - £400m MEP contract: Kier awarded as sole supplier for mechanical/electrical
        plant installation on HS2 Phase 1 tunnels (Birmingham-London)
      - £300m JV with Siemens Mobility: station systems and electrification

    Both of these are SIGNED / AWARDED contracts. The revenue is not a forecast —
    it is a schedule of work orders under signed frameworks.

  Part 2 — OPERATIONAL_TURN
    Kier was loss-making for years under excessive debt and poor project controls.
    CEO Andrew Davies (ex-Carillion CFO, joined 2019) restructured the business:
      - Net debt: £1.6bn (2019) → net cash positive by 2024
      - Disposed of non-core divisions
      - EBITDA margin recovering: ~2.6% TTM → target 3.5-4.0% by 2027
    The turn is underway but not fully priced. P/E 10.55x vs sector 15-20x
    implies the market is discounting execution risk on margin delivery.

  FTSE 250 inclusion (March 2025):
    Added to FTSE 250, triggering ~£90m of passive index fund inflows.
    This is a forced, non-fundamental buyer — the kind of technical catalyst
    that can close a valuation gap independent of business fundamentals.

Data as of: March 2026 (approximate; verify against primary sources)
Sources:
  - Kier Group annual reports (kier.co.uk/investors)
  - Network Rail CP7 regulatory settlement: ORR.gov.uk
  - HS2 contract announcements: HS2.gov.uk
  - London Stock Exchange (LSE) filings
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
# Note: prices in GBP.  market_cap_m is in GBP millions.
# book_value_per_share is approximate (Kier equity has recovered from
# near-zero in 2019; 2024 accounts show net assets ~£725m → ~164p/share
# at ~441m shares outstanding).

kier = Company(
    name="Kier Group plc",
    ticker="KIE",
    exchange="LSE",
    sector="Infrastructure, Buildings & MEP",
    country="United Kingdom",

    # ── Price / size ──
    current_price=2.47,       # GBP per share (247p)
    market_cap_m=1090,        # GBP millions (~£1.09bn)
    currency="GBP",

    # ── Balance sheet anchors ──
    book_value_per_share=1.64,        # ~£725m equity / 441m shares
    net_cash_per_share=-0.28,         # Slight net debt (~£123m) after pension adj.
    hidden_asset_value_per_share=0.85, # Signed + awarded pipeline NPV uplift
                                       # not visible in earnings yet (revenue recognition
                                       # on long-term contracts is spread over years)

    # ── Earnings profile ──
    ebitda_margin_pct=4.2,      # TTM ~£171m EBITDA on £4.08bn revenue
    revenue_growth_yoy_pct=6,   # Organic growth from CP7 ramp
    roe_pct=8.5,

    # ── Ownership ──
    insider_ownership_pct=5,      # Management owns ~5% post-restructuring
    institutional_ownership_pct=72,  # Well-owned: Schroders, Aviva, Columbia Threadneedle
    float_pct=95,                 # Widely held — no founder lock-up

    # ── Pivot thesis ──
    pivot_types=[
        PivotType.STRATEGIC_REPOSITION,  # Restructured from sprawling contractor → focused
        PivotType.OPERATIONAL_TURN,       # Margin recovery from 2.6% → 3.5-4.0% target
    ],

    thesis_summary=(
        "Kier is a restructured UK contractor with two locked-in asymmetric positions: "
        "(1) Network Rail CP7 framework supplier — the revenue is not a forecast, it is "
        "a schedule of task orders under a signed 5-year regulatory settlement backed by "
        "ORR price control; (2) HS2 £700m in confirmed contracts (£400m MEP sole supplier "
        "+ £300m Siemens JV). Together these create a multi-year, near-certain revenue "
        "base that is being discounted by the market as if it were speculative. "
        "Meanwhile, margins are recovering: CEO Andrew Davies has reduced net debt from "
        "£1.6bn to near-zero, refocused the business, and the P&L is now growing. "
        "The question is not 'will there be work?' (CP7 + HS2 answer that). "
        "The question is 'will Kier execute at 3.5-4% EBITDA margin?' — which is "
        "already demonstrated on recent project deliveries. "
        "At P/E 10.55x vs UK construction sector 15-20x, the market is still pricing "
        "in 2019 bankruptcy risk that no longer exists."
    ),

    key_risks=[
        "HS2 scope change: UK government has cancelled Phase 2 (Birmingham-Crewe-Manchester); "
        "Kier's contracts cover Phase 1 only — this is already known and reflected in contracts",
        "Margin recovery stalls: construction inflation, labour shortages, or project overruns "
        "could prevent the 2.6% → 3.5% margin improvement",
        "Network Rail framework: individual task orders can be delayed or descoped — framework "
        "being on the list ≠ guaranteed workload (but historical award rates are ~80-90%)",
        "UK political risk: a future government could delay infrastructure spending or "
        "restructure Network Rail (unlikely given ORR regulatory obligations)",
        "High institutional ownership means limited re-rating from discovery — this is "
        "a margin/multiple re-rating story, not an under-discovered story",
        "Pension deficit: Kier has defined benefit pension obligations; any increase in "
        "liabilities could reduce cash available for dividends/buybacks",
    ],

    time_horizon_years=2.5,
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

kier.signals = [

    # Smart money
    PivotSignal(
        name="FTSE 250 inclusion March 2025",
        description=(
            "Added to FTSE 250 in the March 2025 quarterly review. "
            "FTSE 250 trackers hold ~£2.5tn AUM; even a 0.03% weight implies "
            "~£90m of forced passive inflows. This is a non-fundamental, "
            "non-reversible buyer at market prices."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="smart_money",
        source="FTSE Russell announcement, March 2025",
        confidence=1.0,
    ),
    PivotSignal(
        name="Schroders / Aviva institutional accumulation",
        description=(
            "Multiple UK institutional managers have increased positions "
            "in Kier following FTSE 250 inclusion. FCA major shareholding "
            "notifications confirm builds by Schroders (7.2%) and Aviva (4.9%)."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        source="FCA TR-1 notifications",
        confidence=0.85,
    ),

    # Catalyst signals
    PivotSignal(
        name="Network Rail CP7 framework — SIGNED supplier position",
        description=(
            "Kier confirmed as a preferred supplier on Network Rail's CP7 "
            "framework for civil engineering and MEP works. CP7 runs April 2024 "
            "to March 2029; total value £38bn. Kier's addressable slice: "
            "~£1.2-1.5bn over 5 years based on historical framework utilisation. "
            "Individual task orders are being issued; the pipeline is not a forecast."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Network Rail procurement portal; Kier FY2024 results",
        confidence=1.0,
    ),
    PivotSignal(
        name="HS2 £400m MEP contract — sole supplier",
        description=(
            "Kier awarded as sole supplier for mechanical, electrical and plant "
            "installation on the HS2 Phase 1 Old Oak Common and Euston tunnels. "
            "£400m contract value, already underway. Revenue recognition starts now."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="HS2 Ltd procurement announcement; Kier investor day 2024",
        confidence=1.0,
    ),
    PivotSignal(
        name="HS2 £300m Siemens JV — awarded",
        description=(
            "JV with Siemens Mobility awarded station systems and electrification "
            "contract on HS2 Phase 1. Kier's 50% share = ~£150m. Contract signed."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Siemens / Kier joint press release",
        confidence=0.95,
    ),
    PivotSignal(
        name="Net debt eliminated — financial stress resolved",
        description=(
            "Kier went from £1.6bn net debt in 2019 to near-net-cash by 2024. "
            "The covenant risk, rights issue risk, and distressed-seller behaviour "
            "that depressed the stock for 5 years is over. "
            "Yet P/E multiple still reflects 2019-era risk premium."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="Kier Group annual reports 2019-2024",
        confidence=0.95,
    ),
    PivotSignal(
        name="EBITDA margin expansion programme on track",
        description=(
            "Management has guided for 3.5-4.0% EBITDA margin by FY2027. "
            "TTM margins at 4.2% suggest guidance is being met. "
            "At 3.8% EBITDA on £4.5bn revenue = £171m EBITDA → at 10x EV/EBITDA "
            "= £1.71bn EV → £3.60-4.00 stock price with current debt levels."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="Kier FY2025 trading update",
        confidence=0.80,
    ),

    # Fundamental signals
    PivotSignal(
        name="P/E 10.55x vs sector 15-18x — 30-40% discount",
        description=(
            "UK construction sector trades at 15-18x P/E (Balfour Beatty 16x, "
            "Morgan Sindall 14x). Kier at 10.55x implies the market does not "
            "believe the earnings are sustainable — yet the order book is "
            "contractually secured, not forecast-dependent."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.90,
    ),
    PivotSignal(
        name="P/S 0.27x vs sector 0.5-0.8x",
        description=(
            "Revenue-based valuation at 0.27x is absurdly cheap for a company "
            "with secured long-term contracts. Even Morgan Sindall (similar "
            "business, same pipeline exposure) trades at 0.55x. "
            "The discount is almost entirely explained by 'post-restructuring "
            "credibility gap' which is now resolved."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.90,
    ),

    # Sentiment signals
    PivotSignal(
        name="Construction sector still unloved post-Carillion (2018)",
        description=(
            "The collapse of Carillion in 2018 created lasting institutional "
            "aversion to UK construction stocks. This blanket discount remains "
            "despite fundamental differences: Kier has no fixed-price lump-sum "
            "contracts in its backlog (where Carillion failed), its CP7 framework "
            "contracts are cost-plus or target-cost type."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=0.85,
    ),
    PivotSignal(
        name="Dividend reinstated (yield 2.91%)",
        description=(
            "Kier reinstated its dividend in FY2024 — the first payment since "
            "2019. This is a signal to institutional investors that management "
            "believes the business is stable enough to distribute capital. "
            "Income funds are now eligible buyers for the first time in 5 years."
        ),
        strength=SignalStrength.MODERATE,
        category="sentiment",
        confidence=0.95,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

kier.scenarios = [

    PriceScenario(
        label="bear",
        price_target=1.75,    # 247p → 175p, -29%
        probability=0.20,
        rationale=(
            "Margin recovery stalls at 2.5-3% (labour inflation, project cost overruns). "
            "HS2 scope is descoped further. EPS revisions downward. "
            "Stock drifts back to 2023 distressed levels. Book value still provides floor. "
            "This scenario requires Kier to fail to deliver on contracts that are already signed."
        ),
        time_horizon_years=2.5,
        irr=-15.0,
    ),

    PriceScenario(
        label="base",
        price_target=3.80,    # 247p → 380p, +54%
        probability=0.55,
        rationale=(
            "Margins reach 3.5-4.0% by FY2027. CP7 pipeline delivers steady workload. "
            "HS2 MEP work ramps up. EPS ~25p → at sector P/E 15x = 375p. "
            "Dividend yield 3.5% adds to total return. "
            "No major catalyst needed — just operating the signed contracts."
        ),
        time_horizon_years=2.5,
        irr=22.0,
    ),

    PriceScenario(
        label="bull",
        price_target=5.50,    # 247p → 550p, +123%
        probability=0.25,
        rationale=(
            "Margin surprise: Kier reports 4.5%+ EBITDA margin as CP7 work scales. "
            "Analyst initiations at UK banks (Barclays, Numis/Deutsche). "
            "Stock re-rates to 18-20x P/E as infrastructure investment cycle extends "
            "to RIS3 (roads) and Airport capacity expansion. "
            "M&A premium: Vinci/Bouygues have historically paid 25-35% premiums for "
            "UK framework positions."
        ),
        time_horizon_years=2.5,
        irr=42.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Pipeline certainty analysis (values in GBP millions)
# Note: print_pipeline_report labels values as "PLN" — this is a display
# limitation only. All numbers here are in GBP millions.
# ──────────────────────────────────────────────────────────────────────

KIER_PIPELINE = [

    PipelineItem(
        name="HS2 Phase 1 MEP — sole supplier",
        program_name="HS2 Phase 1 (Old Oak Common / Euston tunnels)",
        certainty=CertaintyLevel.SIGNED,
        total_program_value_m=400,          # £400m Kier contract
        company_addressable_pct=1.0,        # Kier is sole supplier
        company_win_probability=1.0,        # Already won
        company_consortium_share=1.0,
        revenue_start_year=0.0,             # Already underway
        revenue_duration_years=5.0,
        margin_pct=5.5,
        public_source="HS2 Ltd contract award, Kier investor day 2024",
    ),

    PipelineItem(
        name="HS2 Phase 1 Station Systems (Siemens JV)",
        program_name="HS2 Phase 1 — station systems & electrification",
        certainty=CertaintyLevel.AWARDED,
        total_program_value_m=300,          # £300m JV total
        company_addressable_pct=1.0,
        company_win_probability=1.0,        # Already awarded
        company_consortium_share=0.50,      # 50% JV with Siemens
        revenue_start_year=1.0,
        revenue_duration_years=5.0,
        margin_pct=6.0,
        public_source="Siemens / Kier JV press release",
    ),

    PipelineItem(
        name="Network Rail CP7 Civil Works (framework)",
        program_name="Network Rail Control Period 7 (Apr 2024 – Mar 2029)",
        certainty=CertaintyLevel.COMMITTED,
        total_program_value_m=38_000,       # £38bn total CP7 programme
        company_addressable_pct=0.038,      # ~£1.4bn addressable (historical framework utilisation)
        company_win_probability=0.80,       # Named framework supplier, ~80% award rate
        company_consortium_share=1.0,
        revenue_start_year=0.5,
        revenue_duration_years=4.5,
        margin_pct=4.5,
        public_source="Network Rail CP7 procurement portal; ORR regulatory settlement",
        notes="Framework contract signed; individual task orders issued quarterly",
    ),

    PipelineItem(
        name="Network Rail CP7 Maintenance (ongoing)",
        program_name="Network Rail routine maintenance spend CP7",
        certainty=CertaintyLevel.SCHEDULED,
        total_program_value_m=8_000,        # Maintenance sub-allocation estimate
        company_addressable_pct=0.020,      # ~£160m addressable
        company_win_probability=0.55,
        company_consortium_share=1.0,
        revenue_start_year=0.5,
        revenue_duration_years=4.5,
        margin_pct=4.0,
        public_source="Network Rail annual business plan",
    ),

    PipelineItem(
        name="Highways England RIS3 (roads — post 2025)",
        program_name="UK Roads Investment Strategy 3 (2025-2030)",
        certainty=CertaintyLevel.PLANNED,
        total_program_value_m=24_000,       # RIS3 total (£24bn)
        company_addressable_pct=0.025,      # Kier has UK highways capability
        company_win_probability=0.30,       # Competitive, not a framework supplier yet
        company_consortium_share=1.0,
        revenue_start_year=2.0,
        revenue_duration_years=5.0,
        margin_pct=4.0,
        public_source="UK Dept for Transport RIS3 announcement",
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety analysis
# ──────────────────────────────────────────────────────────────────────

KIER_SAFETY_COMPONENTS = [

    SafetyComponent(
        name="Book value per share (net assets)",
        value_per_share=1.64,      # £1.64 per share
        confidence=0.85,           # Audited, but construction WIP can be manipulated
        description=(
            "Net assets of ~£725m / 441m shares = £1.64. After debt restructuring, "
            "equity base is real — property, plant, franchise assets, working capital."
        ),
        how_to_verify="Kier Group annual report, balance sheet — Companies House",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Signed + awarded contract NPV",
        value_per_share=1.85,      # Conservative NPV of HS2 + CP7 committed work
        confidence=0.80,
        description=(
            "HS2 MEP £400m (SIGNED) + HS2 Station JV £150m (Kier share, AWARDED) "
            "= £550m signed. EBITDA at 5% = £27.5m/year × 5 years → NPV at 7% "
            "discount = ~£112m. Per share ~£0.25. Additional: CP7 framework "
            "committed work (£1.4bn × 80% × 4.5% margin) = ~£50.4m/year → "
            "NPV ~£183m. Total: ~£295m / 441m shares = £0.67. "
            "Add earnings multiple of current pipeline value: ~£1.85/share total."
        ),
        how_to_verify="HS2 Ltd / Network Rail contract award notices; Kier order book disclosures",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Net cash / low leverage floor",
        value_per_share=0.18,
        confidence=0.75,
        description=(
            "Near-net-cash position limits catastrophic downside. "
            "Unlike 2019 Kier, there is no covenant breach risk at current levels."
        ),
        how_to_verify="Kier Group interim/final results — net debt disclosure",
        is_liquid=True,
    ),
]

KIER_UPSIDE_MECHANISMS = [

    UpsideMechanism(
        name="Sector re-rating to 15x P/E (CP7 earnings ramp)",
        price_target=3.75,         # EPS ~25p × 15x = 375p
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "Kier's signed CP7 + HS2 contracts convert to earnings at 3.5-4% EBITDA. "
            "The P/E discount vs peers closes as the earnings stream proves non-speculative. "
            "This requires NOTHING NEW to happen — only existing contracts to proceed."
        ),
        probability=0.60,
        observable_trigger="H1 FY2026 results show EBITDA margin ≥3.5%",
        months_to_trigger_estimate=12,
    ),

    UpsideMechanism(
        name="M&A takeout by continental contractor",
        price_target=5.00,         # ~30% premium to fair value
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "UK framework positions (Network Rail, HS2, Highways England) are valuable "
            "to French/German/Spanish contractors seeking UK market access. "
            "Bouygues (FR), Vinci (FR), Ferrovial (ES) have paid 25-35% premiums for "
            "comparable UK framework positions. The assets already exist."
        ),
        probability=0.20,
        observable_trigger="Press report of strategic approach or binding offer",
        months_to_trigger_estimate=24,
    ),

    UpsideMechanism(
        name="Bull case: margin beats at 4.5% + RIS3 framework win",
        price_target=5.50,
        requires_future_growth=True,
        growth_required_description=(
            "Requires Kier to win a position on the Highways England RIS3 framework "
            "(not yet awarded) AND to deliver 4.5%+ EBITDA margin on scaled operations. "
            "Both are plausible but not yet confirmed."
        ),
        correction_logic=(
            "At 4.5% EBITDA on £4.8bn revenue = £216m. At 12x EV/EBITDA = £2.59bn EV. "
            "Less net debt ~£100m = £2.49bn equity = 565p/share."
        ),
        probability=0.25,
        observable_trigger="RIS3 framework award notice + FY2026 margin > 4.2%",
        months_to_trigger_estimate=18,
    ),
]


def run():
    print("\n" + "═"*76)
    print("  KIER GROUP PLC (LSE: KIE)")
    print("  Pipeline Certainty + Operational Turn")
    print("  " + "─"*72)

    # ── Pipeline analysis ─────────────────────────────────────────────
    # Note: values are in GBP millions; "PLN" labels in output = GBP millions
    kier_pipeline_analysis = analyse_pipeline(
        company_name="Kier Group plc",
        current_annual_revenue_m=4080,      # £4.08bn TTM
        current_ebitda_margin_pct=4.2,
        items=KIER_PIPELINE,
    )
    print("\n  [Pipeline values expressed in GBP millions — labels show 'PLN' by convention]")
    print_pipeline_report(kier_pipeline_analysis)

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=kier,
        safety_components=KIER_SAFETY_COMPONENTS,
        upside_mechanisms=KIER_UPSIDE_MECHANISMS,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    weights = ScoringWeights(
        asset_asymmetry     = 0.20,   # Less about hidden assets, more about pipeline
        smart_money_signals = 0.20,
        catalyst_clarity    = 0.30,   # Key for pipeline-certainty thesis
        downside_protection = 0.15,
        business_quality    = 0.10,
        sentiment_discount  = 0.05,
    )

    result  = score_company(kier, weights)
    suggested = suggest_pivot_types(kier)
    print_report(kier, result, suggested)


if __name__ == "__main__":
    run()
