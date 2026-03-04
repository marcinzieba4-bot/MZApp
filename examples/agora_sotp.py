"""
Agora SA (WSE: AGO)
====================
Thesis: SOTP_DISCOUNT — Poland's Most Under-Valued Media Conglomerate

Agora SA is Poland's largest diversified media and entertainment group, founded
in 1989. It operates across five distinct business segments, each of which would
trade at a higher multiple as a standalone company than the conglomerate receives.

Segments:
  1. Helios Cinemas (Movies & Books)
     Poland's largest cinema chain by number of locations.
     54 cinemas, 304 screens, 55,000+ seats. Also owns NEXT FILM (distribution).
     IMAX partnership launched H1 2025 (Gdynia + Szczecin).
     Recovering strongly post-COVID (Q2 2024: 3.7m tickets, +27.6% YoY).
     Q2 2025 segment revenue: PLN 138m (best Q2 in history).

  2. AMS Outdoor Advertising (Outdoor segment)
     Poland's #1 OOH (out-of-home) advertising network.
     Leader in citylight, digital panels (DOOH), and transit advertising.
     Q2 2025: PLN 63.9m revenue, PLN 17.0m EBIT, PLN 27.7m EBITDA (43% margin!)
     Revenue growing double-digits driven by DOOH transition.
     AMS is growing FASTER than the overall OOH market.

  3. Gazeta Wyborcza + Digital (Press segment)
     Poland's flagship quality newspaper, founded 1989.
     ~300,000 digital subscriptions — top European quality news brand.
     ~50% of press revenue now from digital sources.
     Digital growth partially offsetting print structural decline.

  4. Radio (Eurozet)
     9 stations in top 20 most-listened in Poland.
     Includes TOK FM (news/talk), Radio ZET (mainstream).
     Stable, cash-generative, limited capex.

  5. Internet / Other
     Digital advertising network, adtech, digital portals.

The SOTP Argument:
  AMS alone — at comparable OOH company multiples (Clear Channel 7-9x EV/EBITDA,
  JCDecaux 9-12x EV/EBITDA, Stroer 10-12x) — is worth PLN 700-1,100m.
  Current total market cap: ~PLN 367m.
  AMS > entire market cap. The other four businesses are FREE.

Management target: PLN 200m EBITDA group-wide by 2026.
  Currently: ~PLN 80-100m EBITDA (H1 2025 opco improvement +30% YoY)
  Path to PLN 200m: AMS digital panel rollout + Helios recovery + digital subs

Data as of: March 2026
Sources:
  - Agora Group quarterly results (agora.pl/ir)
  - WSE ESPI filings
  - Comparable OOH transactions: Clear Channel, Stroer, JCDecaux annual reports
  - Kinepolis Group (cinema comps)
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
from framework.sotp import SOTPSegment, SOTPAnalysis, analyse_sotp, print_sotp_report
from framework.margin_of_safety import (
    SafetyComponent, UpsideMechanism,
    analyse_margin_of_safety, print_margin_of_safety_report,
)
from framework.idea_types import (
    IdeaType, identify_idea_types,
)


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# Shares: ~41m (market cap PLN 367m / PLN 8.94 price = 41.1m shares)
# AMS quarterly EBITDA: PLN 27.7m → annualised PLN 110.8m
# Helios quarterly revenue: PLN 138m Q2 2025 → annualised PLN 500-550m (seasonality)

agora = Company(
    name="Agora SA",
    ticker="AGO",
    exchange="WSE",
    sector="Diversified Media, Entertainment & Advertising",
    country="Poland",

    current_price=8.94,          # PLN per share (February 2026)
    market_cap_m=367,            # PLN millions (~41m shares × PLN 8.94)
    currency="PLN",

    # Balance sheet
    book_value_per_share=7.50,   # Estimated equity ~PLN 308m / 41m shares
    net_cash_per_share=-2.10,    # Net debt (~PLN 86m IFRS 16 leases + operational)
    hidden_asset_value_per_share=0.0,  # Assets are visible; just mispriced

    # Earnings profile
    ebitda_margin_pct=6.5,       # Group: ~PLN 95m EBITDA / PLN 1.46bn revenue
    revenue_growth_yoy_pct=7,    # FY2024 +7.24% YoY
    roe_pct=4.5,                 # Low because of conglomerate structure + debt

    # Ownership
    insider_ownership_pct=20,    # Founding shareholders, Agora Foundation
    institutional_ownership_pct=18,
    float_pct=60,

    pivot_types=[
        PivotType.ASSET_RELEASE,       # Partial sale of AMS or Helios
        PivotType.STRATEGIC_REPOSITION, # Focus strategy (exit declining assets)
    ],

    thesis_summary=(
        "Agora SA is a Polish media conglomerate where AMS Outdoor Advertising "
        "(#1 OOH in Poland, PLN 110m+ annualised EBITDA, growing double-digits) "
        "is worth more than the entire group market cap of PLN 367m. "
        "The other four businesses — Helios (Poland's largest cinema chain), "
        "Gazeta Wyborcza, radio stations, and digital media — are being given away. "
        "Management has publicly targeted PLN 200m EBITDA by 2026. "
        "At 7x EV/EBITDA on PLN 200m = PLN 1.4bn EV vs PLN 367m market cap = "
        "3.8x upside if the target is reached and the conglomerate discount narrows. "
        "Even if the target is missed and only PLN 120m EBITDA is achieved: "
        "PLN 120m × 7x = PLN 840m → still 2.3x current market cap. "
        "The missing piece: a catalyst that forces price discovery (partial sale)."
    ),

    key_risks=[
        "Controlling shareholders (Gazeta Wyborcza founders) have no financial need to sell",
        "Newspaper structural decline: GW print circulation falling 15-20%/year",
        "AMS EBITDA margin may be overstated due to IFRS 16 lease treatment",
        "Helios box office dependent on Hollywood film slate (cyclical, variable)",
        "Agora has a history of disappointing on capital allocation (overinvested in digital)",
        "Polish media regulation: government can weaponise advertising spend (PiS boycotted GW)",
        "Limited float: minority shareholders cannot force strategic change",
    ],

    time_horizon_years=3.0,
)


# ──────────────────────────────────────────────────────────────────────
# SOTP Analysis — the core of the thesis
# ──────────────────────────────────────────────────────────────────────
# Key data:
#   AMS: Q2 2025 revenue PLN 63.9m, EBITDA PLN 27.7m → annualised PLN 255.6m / PLN 110.8m
#   Helios: Q2 2025 revenue PLN 138m (best Q2 ever) → annualised ~PLN 500m (H2 seasonality)
#   Radio/Press/Internet: estimated from group totals minus AMS and Helios

sotp = SOTPAnalysis(
    company_name="Agora SA",
    ticker="AGO",
    exchange="WSE",
    currency="PLN",
    current_market_cap_m=367,
    net_debt_m=86,                  # IFRS 16 leases + bank debt ~PLN 86m
    minority_interests_m=0,
    central_costs_m=25,             # Group corporate costs not allocated
    central_cost_multiple=7.0,
    segments=[

        SOTPSegment(
            name="AMS Outdoor Advertising",
            segment_type="operations",
            annual_revenue_m=256,      # Annualised from Q2 2025 (PLN 63.9m × 4)
            ebitda_m=111,              # PLN 27.7m Q2 × 4 = PLN 110.8m
            ebitda_margin_pct=43.4,
            multiple_bear=6.0,         # Distressed OOH (pandemic-era comps)
            multiple_base=9.0,         # JCDecaux, Clear Channel comparable
            multiple_bull=12.0,        # Stroer at peak; DOOH re-rating premium
            multiple_basis="EV/EBITDA",
            natural_buyers=[
                "Clear Channel Europe (US-owned OOH; expanding in CEE)",
                "JCDecaux (FR; #1 global OOH; missing Polish market leader position)",
                "Stroer (Germany; already owns OOH networks in CEE)",
                "Private equity: OOH businesses are infrastructure-like; PE loves them",
                "Antenna Media Group (Greek media; expanding in SEE)",
            ],
            recent_comps=[
                "Clear Channel: acquired Lamar European assets at 9x EV/EBITDA (2023)",
                "JCDecaux: Polish OOH Pilot / Ewo acquired at 8-10x (2019)",
                "Stroer: CEE expansion at 8-11x EV/EBITDA (2015-2022)",
            ],
            trend="growing",
            carve_out_cost_m=10,       # IT separation, standalone listing costs
            notes="AMS is the key asset. Revenue growing double-digit from DOOH transition.",
        ),

        SOTPSegment(
            name="Helios Cinemas",
            segment_type="operations",
            annual_revenue_m=500,      # Annualised from Q2 2025 (strong Q2; H1/H2 seasonal)
            ebitda_m=55,               # Estimated: post-IFRS16 EBITDA ~11% margin
            ebitda_margin_pct=11.0,
            multiple_bear=4.0,         # Post-COVID distressed cinema (AMC levels)
            multiple_base=6.5,         # Kinepolis median; CEE cinema chains
            multiple_bull=9.0,         # Strategic premium; IMAX upgrade value-add
            multiple_basis="EV/EBITDA",
            natural_buyers=[
                "Kinepolis Group (Belgium; European cinema consolidator; done 15+ acquisitions)",
                "Vue Entertainment (UK PE-backed; expanding in CEE)",
                "CinemaCity (already in Poland; would give local monopoly — regulatory issue)",
                "Private equity: operating cash flow + IMAX premium = attractive buyout",
            ],
            recent_comps=[
                "Kinepolis: acquired Ciné Centre (Belgium) at 6x EV/EBITDA (2022)",
                "Vue: acquired Cinema City Ireland at 5.5x (2021)",
                "Cineworld European assets: sold at 4-6x distress (2023)",
            ],
            trend="growing",
            carve_out_cost_m=15,
            notes="54 cinemas, 304 screens. IMAX launch 2025. Box office recovery ongoing.",
        ),

        SOTPSegment(
            name="Radio (Eurozet / Group Radio)",
            segment_type="operations",
            annual_revenue_m=180,      # Estimated radio segment revenue
            ebitda_m=30,               # ~17% EBITDA margin for radio
            ebitda_margin_pct=17.0,
            multiple_bear=4.0,         # Declining traditional radio
            multiple_base=6.0,         # Digital audio + podcast transition
            multiple_bull=8.0,         # Strategic buyer premium (Bauer Media, RMF)
            multiple_basis="EV/EBITDA",
            natural_buyers=[
                "Bauer Media (Germany; already owns radio in Poland)",
                "RMF Group (Polish radio; horizontal consolidation)",
                "Eurozet management buyout",
            ],
            recent_comps=[
                "Bauer Media: Central European radio acquisitions at 5-7x EV/EBITDA",
            ],
            trend="stable",
            carve_out_cost_m=5,
            notes="9 top-20 stations. TOK FM premium news brand.",
        ),

        SOTPSegment(
            name="Gazeta Wyborcza (Digital + Print Press)",
            segment_type="operations",
            annual_revenue_m=350,      # Estimated press segment revenue
            ebitda_m=15,               # ~4% EBITDA margin (digitising, losing print)
            ebitda_margin_pct=4.3,
            multiple_bear=1.0,         # Declining print; worth very little
            multiple_base=3.0,         # Digital subscriptions: 300k @ PLN 30/month = PLN 108m ARR
            multiple_bull=5.0,         # If fully digital: NYT-style re-rating
            multiple_basis="EV/EBITDA",
            natural_buyers=[
                "Axiom Media (digital news roll-up)",
                "Foreign PE: turnaround thesis on digital transition",
                "Management buyout (editorial independence value)",
            ],
            recent_comps=[
                "Digital subscription businesses: 3-6x revenue if ARR > PLN 100m",
            ],
            trend="declining",
            carve_out_cost_m=0,
            notes="300k digital subs. 50% revenue digital. Legacy asset with declining print.",
        ),

        SOTPSegment(
            name="Internet & Digital Advertising",
            segment_type="operations",
            annual_revenue_m=170,      # Estimated digital/internet segment
            ebitda_m=12,               # ~7% margin
            ebitda_margin_pct=7.1,
            multiple_bear=3.0,
            multiple_base=5.0,
            multiple_bull=7.0,
            multiple_basis="EV/EBITDA",
            natural_buyers=["Digital ad network aggregators", "Warsaw-based adtech"],
            recent_comps=[],
            trend="stable",
            carve_out_cost_m=0,
            notes="Digital portals, ad network, online classifieds.",
        ),
    ]
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

agora.signals = [

    PivotSignal(
        name="AMS quarterly EBITDA PLN 27.7m → annualised PLN 111m > market cap",
        description=(
            "Q2 2025: AMS EBIT PLN 17m, EBITDA PLN 27.7m. Annualised: PLN 68m EBIT, "
            "PLN 111m EBITDA. At 9x EV/EBITDA = PLN 999m. "
            "Total market cap of AGORA = PLN 367m. "
            "AMS alone at a modest comparable multiple = 2.7x entire market cap. "
            "The other four businesses are valued at NEGATIVE PLN 632m by the market."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="fundamentals",
        confidence=0.90,
    ),

    PivotSignal(
        name="Management target PLN 200m EBITDA by 2026 — stated publicly",
        description=(
            "President Bartosz Hojka publicly stated the target of PLN 200m EBITDA "
            "for 2026. 'The almost thirty per cent increase in EBITDA is a significant "
            "step on the path to PLN 200m EBITDA, which is our goal for 2026.' "
            "If achieved: PLN 200m × 7x = PLN 1.4bn EV → PLN 1.31bn equity "
            "(less debt) → 3.6x current market cap."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Agora Group Q1 2025 results press conference",
        confidence=0.85,
    ),

    PivotSignal(
        name="Helios Q2 2025 — best Q2 in cinema segment history",
        description=(
            "Q2 2025 Helios revenue PLN 138m — best Q2 result in segment history. "
            "Box office recovery continuing. IMAX partnerships (2 new locations Gdynia/Szczecin) "
            "launched. Premium formats are margin-accretive. "
            "This business is recovering strongly, not declining."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.90,
    ),

    PivotSignal(
        name="AMS is Poland's #1 OOH — natural M&A target for JCDecaux/Clear Channel",
        description=(
            "JCDecaux and Clear Channel are the two global OOH leaders. Neither "
            "is the market leader in Poland. AMS is. This makes AMS a strategic "
            "acquisition target — OOH is a local duopoly/monopoly business, "
            "and the incumbent wins disproportionately from DOOH transition. "
            "Transaction: either would pay 9-12x EV/EBITDA."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        confidence=0.70,
    ),

    PivotSignal(
        name="H1 2025 operating profit up ~30% YoY — earnings inflection",
        description=(
            "Group operating profit grew ~30% in H1 2025. "
            "The improvement is broad-based: AMS DOOH, Helios premium, digital subscriptions. "
            "This is not a one-off. The business is at an inflection point."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.85,
    ),

    PivotSignal(
        name="Zero international coverage — under the radar for international funds",
        description=(
            "No international analyst coverage. No English IR presentations in London/NY. "
            "Agora is purely a domestic Polish stock story. "
            "The first international fund that runs an SOTP analysis discovers: "
            "AMS alone > market cap."
        ),
        strength=SignalStrength.MODERATE,
        category="sentiment",
        confidence=0.90,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

agora.scenarios = [

    PriceScenario(
        label="bear",
        price_target=5.50,    # PLN 5.50, -38%
        probability=0.20,
        rationale=(
            "PLN 200m EBITDA target missed; AMS digital panel rollout delayed; "
            "Helios affected by weak film slate (Hollywood strikes aftermath). "
            "Group EBITDA stays at PLN 60-70m. Conglomerate discount widens. "
            "Book value ~PLN 7.50 provides some floor but net debt pressures it. "
            "Worst case: PLN 5-6 range as conglomerate discount reaches 50%."
        ),
        time_horizon_years=3.0,
        irr=-15.0,
    ),

    PriceScenario(
        label="base",
        price_target=22.00,   # PLN 22.00, +146%
        probability=0.55,
        rationale=(
            "PLN 150m EBITDA reached (75% of target). "
            "Partial sale of AMS to strategic buyer at 9x = PLN 999m. "
            "Remaining group (Helios + Radio + Press + Digital) at PLN 367m cap. "
            "AMS proceeds distributed: PLN 24.36/share. "
            "Or: without sale, market re-rates to 5x EV/EBITDA: "
            "PLN 150m × 5x = PLN 750m EV → PLN 664m equity → PLN 16.2/share. "
            "Blended: PLN 22."
        ),
        time_horizon_years=3.0,
        irr=35.0,
    ),

    PriceScenario(
        label="bull",
        price_target=45.00,   # PLN 45.00, +403%
        probability=0.25,
        rationale=(
            "PLN 200m EBITDA achieved 2026. "
            "Strategic acquirer bids for AMS at 12x = PLN 1.33bn. "
            "Agora distributes AMS proceeds + retains Helios + Radio. "
            "Or: PE buys WHOLE company at 8x PLN 200m EBITDA = PLN 1.6bn EV → "
            "PLN 1.51bn equity / 41m shares = PLN 36.8 + control premium = PLN 45+."
        ),
        time_horizon_years=3.0,
        irr=72.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety
# ──────────────────────────────────────────────────────────────────────

AGORA_SAFETY = [
    SafetyComponent(
        name="AMS value (conservative 6x EV/EBITDA)",
        value_per_share=14.88,        # PLN 111m × 6 = PLN 666m - debt PLN 86m = PLN 580m / 41m
        confidence=0.70,
        description="AMS at 6x EV/EBITDA (distressed OOH comp) > current market cap.",
        how_to_verify="Comparable OOH transaction multiples (Clear Channel, JCDecaux)",
        is_liquid=False,
    ),
    SafetyComponent(
        name="Helios asset value (54 cinemas, equipment)",
        value_per_share=5.37,         # PLN 55m × 4x bear / 41m shares
        confidence=0.60,
        description="Cinema assets: 54 cinemas, 304 screens. Even at 4x EBITDA.",
        how_to_verify="Kinepolis, Vue cinema M&A comparables",
        is_liquid=False,
    ),
    SafetyComponent(
        name="Gazeta Wyborcza digital subscriptions",
        value_per_share=1.83,         # 300k subs × PLN 30/mo × 12 = PLN 108m ARR × 0.7x
        confidence=0.50,
        description="300k digital subs at PLN 30/month = PLN 108m ARR. Worth 0.5-1x ARR.",
        how_to_verify="Polish digital media subscription values",
        is_liquid=False,
    ),
]

AGORA_UPSIDE = [
    UpsideMechanism(
        name="AMS partial sale triggers SOTP price discovery",
        price_target=32.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "AMS sold at 9x EV/EBITDA = PLN 999m. Agora receives PLN 999m for 100% "
            "of AMS (or PLN 600m+ for 65% stake). One transaction and the market "
            "immediately reprices the remaining business. "
            "After AMS sale: remaining businesses worth PLN 300-500m. "
            "Total equity: PLN 900m+ / 41m shares = PLN 21+. "
            "AMS sale proceeds alone = PLN 24+ per Agora share."
        ),
        probability=0.30,
        observable_trigger="Agora ESPI: 'strategic review of Outdoor segment' or binding offer",
        months_to_trigger_estimate=24,
    ),
    UpsideMechanism(
        name="PLN 200m EBITDA by 2026 + multiple re-rating",
        price_target=28.00,
        requires_future_growth=True,
        growth_required_description="EBITDA must grow from ~PLN 95m to PLN 200m by 2026 (management target)",
        correction_logic=(
            "PLN 200m × 7x EV/EBITDA = PLN 1.4bn EV → equity PLN 1.31bn / 41m = PLN 31.9. "
            "With modest conglomerate discount (15%): PLN 27.1. "
            "This requires EBITDA to more than double — ambitious but management has committed."
        ),
        probability=0.40,
        observable_trigger="H2 2025 results show EBITDA run-rate > PLN 160m",
        months_to_trigger_estimate=18,
    ),
    UpsideMechanism(
        name="PE buyout of entire Agora at modest EV/EBITDA",
        price_target=45.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "At PLN 200m EBITDA target, Agora at 8x = PLN 1.6bn EV → "
            "PLN 1.514bn equity / 41m shares = PLN 36.9. "
            "Control premium of 20% = PLN 44+. "
            "PE buyer gets: AMS (infrastructure cash flow), Helios (recovery upside), "
            "GW (digital brand). Package worth more than parts to a media PE."
        ),
        probability=0.15,
        observable_trigger="Non-binding offer or exclusivity agreement for Agora",
        months_to_trigger_estimate=36,
    ),
]


def run():
    sep  = "═" * 76

    print(f"\n{sep}")
    print("  AGORA SA (WSE: AGO)")
    print("  Sum-of-Parts Discount — AMS Alone > Market Cap")
    print(sep)

    # ── Idea type identification ──────────────────────────────────────
    idea_types = identify_idea_types(
        has_analyst_coverage=False,
        market_cap_m_eur=74,           # ~€74m (PLN 367m / 4.95)
        institutional_pct=18,
        has_parent_under_pressure=False,
        has_frozen_stake=False,
        defense_revenue_pct=0,
        has_government_pipeline=False,
        has_sotp_discount=True,        # The core thesis
        has_ip_catalog=False,
        has_insider_cluster=False,
        chf_exposure=False,
        in_conflict_zone=False,
    )
    print(f"\n  IDENTIFIED IDEA TYPES:")
    print("─" * 76)
    for idea_type, confidence in idea_types:
        print(f"  [{confidence:.0%}] {idea_type.value}")

    # ── SOTP analysis ─────────────────────────────────────────────────
    analyse_sotp(sotp)
    print_sotp_report(sotp)

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=agora,
        safety_components=AGORA_SAFETY,
        upside_mechanisms=AGORA_UPSIDE,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    weights = ScoringWeights(
        asset_asymmetry     = 0.35,   # SOTP: hidden value is the whole thesis
        smart_money_signals = 0.15,
        catalyst_clarity    = 0.20,
        downside_protection = 0.10,
        business_quality    = 0.10,
        sentiment_discount  = 0.10,
    )

    result    = score_company(agora, weights)
    suggested = suggest_pivot_types(agora)
    print_report(agora, result, suggested)

    # ── Key questions ─────────────────────────────────────────────────
    print(f"\n{sep}")
    print("  THE THREE KEY QUESTIONS FOR THIS THESIS")
    print(sep)
    print("""
  Q1: Is AMS really worth PLN 700-1,100m?
      → YES. Q2 2025 EBITDA annualised = PLN 111m.
        Comparable OOH companies (Stroer, JCDecaux, Clear Channel) at 8-12x.
        AMS is GROWING (DOOH transition) — not a declining print ad business.
        At 9x (conservative): PLN 111m × 9 = PLN 999m vs PLN 367m market cap.

  Q2: Why hasn't the discount closed already?
      → Controlling shareholders (Gazeta Wyborcza founders) show no urgency to sell.
        The newspaper heritage creates emotional attachment.
        Agora's management historically preferred to grow vs. divest.
        BUT: the financial pressure of under-performance vs. peers is building.
        Management committed to PLN 200m EBITDA = de facto admission that
        current structure must deliver or something changes.

  Q3: What actually triggers value realisation?
      → Most likely: strategic review of AMS forced by institutional pressure,
        or an unsolicited offer from JCDecaux/Clear Channel that management
        has to disclose to shareholders (ESPI).
        The least likely: management spontaneously decides to maximise shareholder value.
        The most likely: financial pressure + board change over 2-3 years.

  PATIENCE REQUIRED: This is a 2-3 year idea, not a 6-month trade.
  The discount is real. The assets are real. The catalyst is uncertain.
""")
    print(sep)


if __name__ == "__main__":
    run()
