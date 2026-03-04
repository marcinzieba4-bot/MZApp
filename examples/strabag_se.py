"""
Strabag SE (VIE: STR)
======================
Thesis: OWNERSHIP_CHANGE — Rasperia sanctions resolution

Strabag SE is Europe's third-largest construction company (by revenue), a
Vienna-listed Austrian contractor with operations across 80+ countries.
Revenue: €19.2bn (2024). EBITDA: €1.43bn (7.8% margin). Backlog: €30bn+ (record).

This is NOT a cheap, distressed company. Strabag is a high-quality, well-run
construction group with exceptional execution capabilities. The pivot thesis is
purely about OWNERSHIP STRUCTURE and the artificial discount imposed by it.

The Rasperia situation (the structural constraint):
  Rasperia Trading Ltd (Cyprus) is the investment vehicle of Oleg Deripaska,
  a Russian oligarch under EU and UK sanctions since 2022. Rasperia holds 24.1%
  of Strabag's shares, which are FROZEN under EU sanctions regulations.

  Because Rasperia cannot vote, receive dividends, or transfer its stake:
  - Free float: only 14.1% (recently expanded from 10.9% via two placements)
  - Institutional investors: cannot build positions (too illiquid)
  - Index inclusion: limited by float size
  - The 24.1% stake is the "elephant in the room" that depresses the multiple

  Separately: Raiffeisen Bank International (RBI) also has an indirect exposure
  to Rasperia through a different structure. RBI provisioned €339m for Russian
  exposure (2024) and is under ECB pressure to exit Russia. The Strabag/Rasperia
  connection is part of the broader RBI Russia exposure story.

Why the discount resolves:
  EU Sanctions Package 19 (under discussion, 2025-2026) contains provisions
  that could allow Rasperia to divest the Strabag stake under a supervised
  process — where proceeds go to a special escrow or are blocked from
  reaching Deripaska, but the shares transfer to a neutral buyer.

  Two scenarios for resolution:
    A. Supervised sale: Rasperia stake sold to a long-term institutional investor
       (pension fund, sovereign wealth fund, infrastructure fund) at market price.
       Result: free float jumps from 14% to 38%, index inclusion improves,
       institutional demand surges.
    B. Share buyback by Strabag: Strabag buys back the Rasperia stake.
       Result: EPS accretion, float increases, and the "Russian overhang" disappears.

The re-rating potential AFTER resolution:
  Current EV/EBITDA: ~5.5-6.0x
  Comparable construction groups (Vinci, Bouygues, ACS): 7-10x EV/EBITDA
  Discount: 25-40% to peers — purely due to ownership structure and float
  Peer multiple target: 8-9x EV/EBITDA
  Target stock price at 8.5x EV/EBITDA: ~€135-145

The quality of the underlying business:
  - Revenue €19.2bn (2024): only ~20 construction companies in the world are larger
  - EBITDA margin 7.8%: above global construction median of 6-7%
  - Record backlog €30bn+: visibility 18-24 months
  - 80+ countries: geographic diversification reduces single-market risk
  - Haselsteiner family (32.5%): governance anchor, long-term stewardship

Already re-rated 2025:
  Stock went from ~€39.50 (year-end 2024) to ~€98.30 ATH (Feb 2026) = +149%.
  WHY? Combination of: (1) record backlog/earnings, (2) sanctions discussion
  progress, (3) two private placements expanding float, (4) European defence
  and infrastructure spending acceleration.

  Is there still asymmetry at €92?
  - EV/EBITDA still only ~5.5x vs peers at 7-10x
  - Residual overhang still not resolved
  - Full resolution → another 30-50% upside

Data as of: March 2026 (approximate; verify against primary sources)
Sources:
  - Strabag SE annual reports and Q-reports (ir.strabag.com)
  - EU sanctions register and package 19 deliberations
  - RBI annual report 2024 (Raiffeisen Group)
  - Vienna Stock Exchange disclosures
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


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# Strabag shares: ~109m shares at €92/share = ~€10bn market cap
# Book value: substantial — Strabag has net cash positive construction balance sheet
# Book value per share: ~€36/share (estimated from equity ~€3.9bn / 109m shares)
# Note: Strabag pays a significant dividend (yield ~3-4%); model in EUR.

strabag = Company(
    name="Strabag SE",
    ticker="STR",
    exchange="VIE",
    sector="Pan-European Construction",
    country="Austria",

    # ── Price / size ──
    current_price=92.00,      # EUR per share (near ATH; up 149% from year-end 2024)
    market_cap_m=10_028,      # EUR millions (~€10bn at 109m shares)
    currency="EUR",

    # ── Balance sheet anchors ──
    book_value_per_share=36.00,      # ~€3.9bn equity / 109m shares
    net_cash_per_share=8.50,         # Strabag is net cash positive (construction float)
    hidden_asset_value_per_share=0.0,  # No hidden assets per se; the discount is structural

    # ── Earnings profile ──
    ebitda_margin_pct=7.8,      # €1.43bn / €19.2bn
    revenue_growth_yoy_pct=4,   # Modest growth; backlog >30bn = 18mo visibility
    roe_pct=14.5,

    # ── Ownership ──
    insider_ownership_pct=62,       # Haselsteiner family 32.5% + management + UNIQA ~25%
    institutional_ownership_pct=14, # Very low due to tiny free float (14.1%)
    float_pct=14,                   # Only 14.1% tradeable

    # ── Pivot thesis ──
    pivot_types=[
        PivotType.OWNERSHIP_CHANGE,     # Primary: Rasperia resolution = float doubles
        PivotType.CAPITAL_STRUCTURE,    # Secondary: if Strabag buys back the frozen stake
    ],

    thesis_summary=(
        "Strabag is Europe's 3rd-largest contractor (€19.2bn revenue, €1.43bn EBITDA, "
        "€30bn+ backlog) but trades at only 5.5-6x EV/EBITDA vs peers at 7-10x. "
        "The entire discount is structural: Rasperia (Deripaska) owns 24.1% of shares "
        "frozen under EU sanctions. Free float is only 14.1%. Institutions cannot build "
        "meaningful positions; indices underweight. "
        "EU Sanctions Package 19 contains provisions for supervised divestiture of "
        "Russian-linked frozen assets. If the Rasperia stake is sold via a supervised "
        "process, free float doubles from 14% to 38%. FTSE, MSCI, and STOXX index "
        "weights increase. Institutional inflows follow mechanically. "
        "Meanwhile, Strabag's business quality is the best in 15 years: record backlog, "
        "expanding margins, pan-European infrastructure supercycle underway. "
        "The quality is not in question — only the free float. "
        "At resolution: re-rates from 5.5x to 8-9x EV/EBITDA = €135-145 target."
    ),

    key_risks=[
        "Rasperia resolution delayed: sanctions packages move slowly; EU political "
        "disagreements (Hungary, Slovakia vetoes) can block progress",
        "Deripaska legal claims: new claims of €326m (2025) against Strabag in Austrian "
        "courts add uncertainty; proceedings create headline risk",
        "RBI cross-contamination: RBI's Russia exposure (provisioned €339m) and its "
        "indirect Rasperia connection creates reputational risk for Strabag",
        "Construction cycle peak: at €30bn backlog and record margins, Strabag may be "
        "at a cycle high — backlog normalisation could disappoint",
        "Concentration of float: 14.1% free float means large trades move the stock "
        "significantly in both directions; high volatility premium",
        "European recession risk: while EU infrastructure spending is government-committed, "
        "private commercial construction (20-25% of Strabag revenue) is cyclical",
        "Already re-rated +149%: much of the obvious upside may already be captured by "
        "the stock run; the residual is the full sanctions resolution which is uncertain",
    ],

    time_horizon_years=3.0,
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

strabag.signals = [

    # Smart money / ownership
    PivotSignal(
        name="Haselsteiner family providing governance anchor",
        description=(
            "Hans-Peter Haselsteiner (founder) and family hold 32.5%. "
            "The family has been actively managing the Rasperia situation, "
            "engaging with EU institutions, and conducting the private placements "
            "to expand float. They are aligned with minority shareholders on resolution."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        source="Strabag annual report; VIE filings",
        confidence=0.90,
    ),
    PivotSignal(
        name="Two private placements in H1 2025 expanded free float from 10.9% to 14.1%",
        description=(
            "Strabag conducted two private placements in H1 2025, issuing new shares "
            "to institutional investors. This was deliberate float management — "
            "making the stock eligible for more index inclusion and institutional ownership. "
            "The direction of travel is clear: management wants more institutional shareholders."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="smart_money",
        source="Strabag Q2 2025 results; VIE stock exchange",
        confidence=0.95,
    ),
    PivotSignal(
        name="Infrastructure and defense-oriented funds accumulating",
        description=(
            "European infrastructure supercycle (€300bn EU defence + TEN-T + CEF spending) "
            "is attracting specialist funds to quality construction names. Strabag is the "
            "highest-quality liquid name in European construction."
        ),
        strength=SignalStrength.MODERATE,
        category="smart_money",
        confidence=0.75,
    ),

    # Catalyst signals
    PivotSignal(
        name="EU Sanctions Package 19 — Rasperia stake divestiture pathway",
        description=(
            "EU Sanctions Package 19 (under deliberation) includes provisions for "
            "supervised divestiture of frozen Russian assets where proceeds are blocked "
            "from reaching sanctioned persons. This creates a legal pathway for Rasperia "
            "to transfer the 24.1% Strabag stake to a neutral buyer. "
            "Timeline: Package 19 expected H1 2026."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="European Commission sanctions working group reports (2025)",
        confidence=0.65,
    ),
    PivotSignal(
        name="Record backlog €30bn+ (18-24 months revenue visibility)",
        description=(
            "Strabag's Q3 2025 backlog exceeded €30bn for the first time — "
            "driven by European infrastructure programmes (TEN-T, CEF, national highways), "
            "housing deficits, and defence/dual-use infrastructure. "
            "This is not a forecast — these are signed and awarded contracts."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="Strabag Q3 2025 quarterly report",
        confidence=1.0,
    ),
    PivotSignal(
        name="European defence infrastructure spending acceleration",
        description=(
            "EU agreed 3% GDP defence target; Germany Sondervermögen €500bn includes "
            "infrastructure. NATO secretary general called for new barracks, runways, "
            "ammunition storage — Strabag wins disproportionately from defence-grade "
            "civil construction (secure facilities, hardened infrastructure)."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="EU defence package announcements; NATO infrastructure spending plans",
        confidence=0.80,
    ),

    # Fundamental signals
    PivotSignal(
        name="EV/EBITDA 5.5-6x vs peers 7-10x — structural discount",
        description=(
            "Vinci (FR): 9.2x. Bouygues (FR): 7.4x. ACS (ES): 8.1x. Balfour Beatty (UK): "
            "7.0x. Strabag at 5.5-6x despite higher margins and larger backlog. "
            "The ENTIRE discount is explained by the free float constraint — not quality."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.90,
    ),
    PivotSignal(
        name="Dividend yield 3-4% supported by net cash position",
        description=(
            "Strabag generates significant operating cash flow (construction float "
            "means customers pay in advance on milestones). Net cash positive. "
            "Dividend has been maintained/growing. This is a cash-generating business "
            "with no debt-driven risk."
        ),
        strength=SignalStrength.MODERATE,
        category="fundamentals",
        confidence=0.95,
    ),

    # Sentiment signals
    PivotSignal(
        name="'Russian tainted' narrative depresses institutional appetite",
        description=(
            "ESG-sensitive institutions avoid Strabag due to the Deripaska connection "
            "even though: (1) Strabag has no operations in Russia, (2) the stake is "
            "frozen, (3) Strabag has taken legal action against Deripaska. "
            "When the sanctions situation resolves, ESG inflows will add to multiple "
            "re-rating from pure value buyers."
        ),
        strength=SignalStrength.STRONG,
        category="sentiment",
        confidence=0.85,
    ),
    PivotSignal(
        name="Vienna Stock Exchange discount (VIE vs LSE/Euronext coverage)",
        description=(
            "Strabag is listed in Vienna — a smaller exchange with less sell-side "
            "coverage than Paris, London, or Frankfurt. Major European construction "
            "sector analysts focus on Vinci/Bouygues/ACS. Strabag is under-modelled "
            "relative to its size and quality."
        ),
        strength=SignalStrength.MODERATE,
        category="sentiment",
        confidence=0.75,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

strabag.scenarios = [

    PriceScenario(
        label="bear",
        price_target=62.00,    # EUR 62, -33%
        probability=0.20,
        rationale=(
            "Sanctions resolution delayed 3+ years; new Deripaska court claims create "
            "negative headlines; European construction cycle peaks; backlog deteriorates. "
            "Stock de-rates back to 4.5x EV/EBITDA. "
            "This is the 'nothing resolves, cycle turns' scenario. "
            "Book value €36 provides some floor (P/B would be 1.7x at €62)."
        ),
        time_horizon_years=3.0,
        irr=-13.0,
    ),

    PriceScenario(
        label="base",
        price_target=125.00,   # EUR 125, +36%
        probability=0.55,
        rationale=(
            "Sanctions Package 19 creates partial resolution: Rasperia stake sold "
            "via supervised process to infrastructure/pension fund. Free float rises "
            "to 38%. STOXX index weight doubles. Institutional inflows. "
            "Business quality sustains: backlog €28-30bn, EBITDA €1.5bn. "
            "Re-rates from 5.5x to 7.5x EV/EBITDA. "
            "€1.5bn EBITDA × 7.5x = €11.25bn EV. Less net debt (positive cash). "
            "~€125-130/share."
        ),
        time_horizon_years=2.5,
        irr=17.0,
    ),

    PriceScenario(
        label="bull",
        price_target=165.00,   # EUR 165, +79%
        probability=0.25,
        rationale=(
            "Full Rasperia resolution + Strabag buyback of the stake (EPS accretive). "
            "MSCI Europe index inclusion (requires higher free float). "
            "European infrastructure supercycle re-rates sector to 10x EV/EBITDA. "
            "M&A: Haselsteiner family may consider merger with another EU contractor "
            "(Vinci/Strabag combination has been speculated for years). "
            "€1.6bn EBITDA × 10x = €16bn EV → €145-165/share."
        ),
        time_horizon_years=3.0,
        irr=21.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety (quality company, not a deep-value floor play)
# ──────────────────────────────────────────────────────────────────────

STRABAG_SAFETY_COMPONENTS = [

    SafetyComponent(
        name="Book value per share (net assets)",
        value_per_share=36.00,
        confidence=0.90,   # Audited, construction balance sheet well-understood
        description=(
            "€3.9bn equity / 109m shares = €36. "
            "Construction working capital is relatively safe: prepayments received, "
            "long-term payables to subcontractors. "
            "No material goodwill from acquisitions (organic growth)."
        ),
        how_to_verify="Strabag SE annual report — balance sheet (ir.strabag.com)",
        is_liquid=False,
    ),

    SafetyComponent(
        name="Net cash position",
        value_per_share=8.50,
        confidence=0.90,
        description=(
            "Strabag holds net cash (construction advance payments from clients). "
            "Unlike industrial companies, construction firms receive milestone advances. "
            "Net cash ~€927m / 109m shares = €8.50. "
            "This is a real cash floor — not a financial engineering artifact."
        ),
        how_to_verify="Strabag net debt/cash disclosure in quarterly reports",
        is_liquid=True,
    ),

    SafetyComponent(
        name="Backlog earnings cover (€30bn signed/awarded)",
        value_per_share=28.00,
        confidence=0.80,
        description=(
            "€30bn backlog at 7.8% EBITDA = €2.34bn in committed future EBITDA. "
            "Even at high discount rates, this has a present value well above current "
            "stock price. Per share: €2.34bn / 109m × discount factor (~1.3x) = "
            "conservatively €28/share of committed earnings not yet reported."
        ),
        how_to_verify="Strabag order backlog by segment, quarterly disclosures",
        is_liquid=False,
    ),
]

STRABAG_UPSIDE_MECHANISMS = [

    UpsideMechanism(
        name="Rasperia stake supervised sale → free float doubles",
        price_target=130.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "The multiple discount vs peers (5.5x vs 7-10x EV/EBITDA) is entirely "
            "explained by free float (14% vs peers 60-90%). "
            "When float doubles, institutional demand normalises, index weights increase. "
            "Re-rating from 5.5x to 7.5x EV/EBITDA on existing €1.43bn EBITDA = "
            "€1.43bn × 7.5x = €10.7bn EV → ~€130/share. "
            "No growth required — just removal of structural constraint."
        ),
        probability=0.55,
        observable_trigger=(
            "EU announcement of Rasperia divestiture framework or Strabag VIE filing "
            "showing Rasperia stake transfer notification"
        ),
        months_to_trigger_estimate=18,
    ),

    UpsideMechanism(
        name="Strabag buys back Rasperia stake (EPS accretion)",
        price_target=145.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "If Strabag buys back 24.1% of shares at market (~€2.4bn), "
            "EPS accretion from reduced share count = +31% uplift on per-share earnings. "
            "At €92 × 1.31 = ~€121 from EPS alone. "
            "Plus re-rating from 5.5x to 8x (float improvement) = additional +€25. "
            "Total ~€145. Strabag has net cash to partially fund this."
        ),
        probability=0.25,
        observable_trigger="Strabag announces share buyback programme for frozen Rasperia shares",
        months_to_trigger_estimate=24,
    ),

    UpsideMechanism(
        name="European infrastructure supercycle + MSCI index inclusion",
        price_target=165.00,
        requires_future_growth=True,
        growth_required_description=(
            "Requires: (1) full Rasperia resolution lifting free float to 38%+, "
            "(2) MSCI Europe inclusion (requires >15% free float investable), "
            "(3) European construction market staying at elevated activity levels "
            "through 2027+. MSCI inclusion triggers forced passive buying ~€1bn."
        ),
        correction_logic=(
            "MSCI Europe inclusion of a €10bn market cap company triggers €800m-1.2bn "
            "of passive inflows. At current free float, 14% of €10bn = €1.4bn is "
            "available to absorb — so €1bn of forced buying = price discovery shock. "
            "Plus: at full re-rating to 9.5x EV/EBITDA, €1.6bn EBITDA × 9.5x = €15.2bn EV."
        ),
        probability=0.20,
        observable_trigger="MSCI announces Strabag inclusion in Europe index review",
        months_to_trigger_estimate=30,
    ),
]


def run():
    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print("  STRABAG SE (VIE: STR)")
    print("  Ownership Change — Rasperia Sanctions Resolution")
    print(sep)

    # ── Ownership structure context ───────────────────────────────────
    print(f"\n  OWNERSHIP STRUCTURE (The Core of the Thesis)")
    print(thin)
    print("""
  Haselsteiner family          : 32.5%   — Governance anchor, long-term
  Rasperia Trading Ltd (frozen): 24.1%   — SANCTIONS FROZEN (Deripaska)
  UNIQA Insurance Group        : 14.9%   — Strategic holding
  Free float                   :  14.1%  — Only tradeable portion
  Management / other           :  14.4%

  The problem:
    24.1% of shares cannot be sold, voted, or have dividends paid.
    This makes Strabag appear less attractive to institutional investors:
      - Most index methodologies only count free float
      - ESG policies of major funds exclude "Russian-linked" investments
      - Illiquidity prevents meaningful position sizes (14% of €10bn = €1.4bn total)

  The opportunity:
    If Rasperia stake resolves → free float jumps from 14.1% to 38.2%
    Institutional capacity to hold: €1.4bn → €3.8bn
    Index weight: doubles or triples
    Re-rating: P/E and EV/EBITDA normalise to peers
""")
    print(thin)

    # ── Peers comparison ─────────────────────────────────────────────
    print("\n  PEER VALUATION COMPARISON")
    print(thin)
    peers = [
        ("Strabag SE (STR, VIE)",     "€19.2bn", "7.8%", "€10.0bn", "5.5-6.0x", "14%"),
        ("Vinci SA (DG, EPA)",        "€71.5bn", "8.2%", "€65.0bn", "9.2x",     "85%"),
        ("Bouygues SA (EN, EPA)",     "€40.4bn", "6.1%", "€28.0bn", "7.4x",     "78%"),
        ("ACS Group (ACS, BME)",      "€35.0bn", "7.4%", "€28.2bn", "8.1x",     "80%"),
        ("Balfour Beatty (BBY, LSE)", "£9.3bn",  "5.8%", "£2.8bn",  "7.0x",     "95%"),
    ]
    print(f"\n  {'Company':<32} {'Revenue':>10}  {'EBITDA%':>8}  {'MktCap':>10}  "
          f"{'EV/EBITDA':>10}  {'Float':>8}")
    print(f"  {'-'*32} {'-'*10}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*8}")
    for name, rev, eb, cap, ev_ebitda, fl in peers:
        marker = " ← CHEAP" if "Strabag" in name else ""
        print(f"  {name:<32} {rev:>10}  {eb:>8}  {cap:>10}  {ev_ebitda:>10}  {fl:>8}{marker}")

    print(f"\n  If Strabag re-rates from 5.5x to 8.5x (midpoint of peers):")
    print(f"    €1.43bn EBITDA × 8.5x = €12.2bn EV")
    print(f"    Plus net cash €0.9bn → Equity €13.1bn / 109m shares = ~€120/share")
    print(f"    Current price €92 → upside: +30%  (before MSCI / float expansion)")

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=strabag,
        safety_components=STRABAG_SAFETY_COMPONENTS,
        upside_mechanisms=STRABAG_UPSIDE_MECHANISMS,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    # Note: for Strabag, the scoring weights differ — this is NOT an asset-play.
    # It's a quality company with an ownership constraint.
    weights = ScoringWeights(
        asset_asymmetry     = 0.10,   # Not an asset play; assets = backlog + cash
        smart_money_signals = 0.25,   # Float expansion signals are key
        catalyst_clarity    = 0.30,   # Sanctions resolution is the specific catalyst
        downside_protection = 0.20,   # High quality business limits downside
        business_quality    = 0.10,   # Business quality is excellent
        sentiment_discount  = 0.05,
    )

    result    = score_company(strabag, weights)
    suggested = suggest_pivot_types(strabag)
    print_report(strabag, result, suggested)

    # ── Timeline ─────────────────────────────────────────────────────
    print(f"\n{sep}")
    print("  SANCTIONS RESOLUTION PATHWAY — OBSERVABLE EVENTS")
    print(sep)
    print("""
  What to monitor (in order of likelihood):

  1. EU Sanctions Package 19 text finalized
     → Look for "supervised divestiture" or "competent authority sale" language
     → Source: EUR-Lex, Official Journal of the EU

  2. Austrian financial intelligence (A-FIU) application from Rasperia
     → Rasperia would need Austrian authority permission to transfer shares
     → Source: Austrian Finance Ministry statements

  3. Strabag VIE announcement: "Transfer notification received"
     → Strabag is required to announce any change in major shareholding
     → Source: ESPI equivalent on Vienna Stock Exchange (OeKB)

  4. RBI Russia exit progress
     → RBI exiting Russia (ECB pressure) removes the indirect Rasperia connection
     → Source: RBI quarterly reports

  5. Deripaska court cases (€326m new claims)
     → Resolution or dismissal removes headline risk
     → Source: Austrian courts public records

  TIMING ESTIMATE: H2 2026 for meaningful sanctions progress (Package 19).
  Full resolution: 2027. Trade window: 12-24 months from now.
""")
    print(sep)


if __name__ == "__main__":
    run()
