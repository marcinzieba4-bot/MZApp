"""
S&P 500 Index Inclusion Strategy — 2025/2026 Candidates
=========================================================

This example demonstrates the pre-announcement alpha methodology for
stocks approaching S&P 500 eligibility.

Academic evidence base:
  • Chen, Noronha & Singal (2004): +3.4% avg abnormal return on announcement day
  • Petajisto (2011): index funds underperform by ~0.8%/yr due to front-running
  • Harris & Gurel (1986): original "price pressure hypothesis" — temporary demand shock
  • Wurgler & Zhuravskaya (2002): stocks with no close substitutes see larger moves

S&P 500 inclusion mechanics:
  1. S&P Index Committee meets continuously (no fixed schedule)
  2. An opening appears when a current member is acquired, goes private, goes bankrupt,
     or falls below market-cap floor (~$5.3B for continued membership)
  3. Replacement announced AFTER MARKET CLOSE on announcement day
  4. Effective date is typically next Friday (5–10 business days later)
  5. Passive funds must own new member at closing price on effective date

Best pre-announcement screening approach:
  • Screen for companies just below inclusion threshold but rapidly approaching it
  • Focus on S&P 400 MidCap members — upgrades to S&P 500 are most predictable
  • Catalyst: S&P 400 member whose market cap exceeds $18B for 2+ consecutive months
  • Combine with momentum: RS > 70th pct, above 200d MA
  • Size position 30–90 days before expected announcement

Candidates analysed (as of early 2026):
  1. Dell Technologies  (DELL)  — Tech, profitable, high liquidity, near threshold
  2. GE Vernova         (GEV)   — Energy infrastructure spinoff, rapidly scaling
  3. Palantir           (PLTR)  — Already added Nov 2024; used as recent reference
  4. Amentum Holdings   (AMTM)  — Defense services, S&P 400 → S&P 500 upgrade candidate
  5. Constellation Energy (CEG) — Already added; reference for nuclear re-rating thesis
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.index_inclusion import (
    SP500EligibilityScreen,
    MomentumProfile,
    PreAnnouncementWindow,
    IndexInclusionCandidate,
    InclusionPhase,
    IndexFamily,
    score_inclusion_candidate,
    print_inclusion_report,
)


# ─────────────────────────────────────────────────────────────────────────────
# CANDIDATE 1 — GE Vernova (GEV) — Energy Infrastructure Spinoff
# ─────────────────────────────────────────────────────────────────────────────
# GEV was spun off from GE in April 2024. By Q4 2024 it crossed the market-cap
# threshold. It was added to S&P 500 in September 2024 — this is the REFERENCE CASE
# showing how a spinoff + strong momentum plays out perfectly.
# Key learning: identify spinoffs 3–6 months post-separation when they approach
# the $18B threshold. GEV doubled from spin to inclusion.

def analyse_gev_reference_case() -> None:
    """GE Vernova — reference case for spinoff + S&P 500 inclusion playbook."""

    screen = SP500EligibilityScreen(
        company_name="GE Vernova Inc.",
        ticker="GEV",
        exchange="NYSE",
        us_domicile=True,
        market_cap_usd_bn=38.5,                     # Peak before inclusion
        float_adjusted_market_cap_usd_bn=36.2,
        annual_dollar_value_traded_usd_bn=85.0,      # Very liquid post-spinoff
        float_pct=93.0,
        recent_quarter_earnings_positive=True,
        trailing_4q_earnings_positive=True,
        months_listed=5.0,                           # ← Gate FAIL: only 5 months post-spin
        current_index_membership="S&P 500 (added Sep 2024)",
        sector_gics="Industrials",
        analyst_coverage_count=22,
    )

    momentum = MomentumProfile(
        return_1m_pct=8.2,
        return_3m_pct=31.5,
        return_6m_pct=72.0,    # Extraordinary post-spinoff re-rating
        return_12m_pct=98.0,   # Near doubling
        rs_percentile=96,
        benchmark_return_12m_pct=24.0,   # S&P 500 2024 return
        above_50d_ma=True,
        above_200d_ma=True,
        volume_trend="expanding",
        distance_from_52w_high_pct=-3.5,
        distance_from_52w_low_pct=+165.0,
    )

    pre_ann = PreAnnouncementWindow(
        current_phase=InclusionPhase.FADE,    # Post-inclusion reference
        estimated_days_to_announcement=None,
        estimated_days_to_effective_date=None,
        estimated_forced_buying_usd_m=4_200,   # ~$4.2B passive buying at inclusion
        estimated_index_weight_pct=0.28,
        adv_days_to_absorb=12.5,
        avg_announcement_day_return_pct=4.8,   # GEV outperformed historical avg
        avg_pre_announcement_drift_pct=5.5,    # Strong drift pre-announcement
        avg_effective_date_bump_pct=2.1,
        avg_30d_post_reversal_pct=-2.5,
    )

    candidate = IndexInclusionCandidate(
        company_name="GE Vernova Inc.",
        ticker="GEV",
        exchange="NYSE",
        sector="Industrials — Power & Electrification",
        country="United States",
        target_index=IndexFamily.SP500,
        current_price=187.50,
        currency="USD",
        market_cap_local_m=38_500,
        market_cap_usd_m=38_500,
        sp500_screen=screen,
        momentum=momentum,
        pre_announcement=pre_ann,
        thesis_summary=(
            "Reference case: GEV spun off from GE April 2024, electrification megatrend, "
            "AI data centre power demand drove extraordinary re-rating. "
            "LESSON: spinoffs from S&P 500 parents with 12-month seasoning requirement "
            "create a predictable inclusion date — buy 45–90 days post-separation "
            "in high-quality spinoffs with strong fundamentals and sector tailwind. "
            "Optimal entry was $85–$95 (60 days post-spin). S&P 500 added Sep 2024."
        ),
        key_risks=[
            "Seasoning rule: 12-month wait post-IPO/spinoff creates a known delay",
            "If earnings turn negative before inclusion: committee will wait",
            "Power sector sentiment could reverse (Ukraine peace, gas price collapse)",
        ],
        catalyst_date="Added S&P 500 September 2024 (REFERENCE CASE — inclusion complete)",
        revenue_growth_yoy_pct=17.0,
        ebitda_margin_pct=8.5,
        roe_pct=18.0,
    )

    result = score_inclusion_candidate(candidate)
    print_inclusion_report(result, candidate)


# ─────────────────────────────────────────────────────────────────────────────
# CANDIDATE 2 — Amentum Holdings (AMTM) — Defense Services, S&P 400 → S&P 500
# ─────────────────────────────────────────────────────────────────────────────
# Amentum went public Sep 2024 via merger/direct listing. Defense services
# company (ex-PAE + DynCorp lineage). Government services at scale.
# S&P 400 MidCap member. Approaching S&P 500 threshold.
# The S&P 400 → S&P 500 promotion is the most predictable inclusion path.

def analyse_amentum() -> None:
    """Amentum Holdings — S&P 400 to S&P 500 upgrade candidate."""

    screen = SP500EligibilityScreen(
        company_name="Amentum Holdings Inc.",
        ticker="AMTM",
        exchange="NYSE",
        us_domicile=True,
        market_cap_usd_bn=9.8,                       # Below $18B threshold (early 2026 est.)
        float_adjusted_market_cap_usd_bn=9.2,
        annual_dollar_value_traded_usd_bn=6.5,
        float_pct=78.0,
        recent_quarter_earnings_positive=True,
        trailing_4q_earnings_positive=True,
        months_listed=16.0,                           # Seasoning satisfied
        current_index_membership="S&P 400 MidCap",   # KEY: natural promotion path
        ipoq_date="Sep 2024",
        sector_gics="Industrials — Defense & Government Services",
        analyst_coverage_count=8,
    )

    momentum = MomentumProfile(
        return_1m_pct=4.5,
        return_3m_pct=12.0,
        return_6m_pct=28.0,
        return_12m_pct=45.0,
        rs_percentile=78,
        benchmark_return_12m_pct=24.0,
        above_50d_ma=True,
        above_200d_ma=True,
        volume_trend="expanding",
        distance_from_52w_high_pct=-8.0,
        distance_from_52w_low_pct=+68.0,
    )

    pre_ann = PreAnnouncementWindow(
        current_phase=InclusionPhase.SCREEN,
        estimated_days_to_announcement=90,     # Estimated — waiting for market cap to clear
        estimated_days_to_effective_date=100,
        estimated_forced_buying_usd_m=950,     # ~$950M passive buying at inclusion weight
        estimated_index_weight_pct=0.06,
        adv_days_to_absorb=8.0,
        avg_announcement_day_return_pct=3.4,
        avg_pre_announcement_drift_pct=2.5,
        avg_effective_date_bump_pct=1.5,
        avg_30d_post_reversal_pct=-1.8,
    )

    candidate = IndexInclusionCandidate(
        company_name="Amentum Holdings Inc.",
        ticker="AMTM",
        exchange="NYSE",
        sector="Industrials — Defense & Government Services",
        country="United States",
        target_index=IndexFamily.SP500,
        current_price=24.50,
        currency="USD",
        market_cap_local_m=9_800,
        market_cap_usd_m=9_800,
        sp500_screen=screen,
        momentum=momentum,
        pre_announcement=pre_ann,
        thesis_summary=(
            "Amentum = largest pure-play US government services company. "
            "Mission-critical services for DoD, DOE, intelligence community. "
            "Revenue ~$12B, ~90% cost-plus government contracts = highly visible earnings. "
            "S&P 400 member since Sep 2024 — natural promotion candidate once mktcap crosses $18B. "
            "NATO spending wave + US defense budget growth supports organic growth. "
            "Momentum phase 0→1 transition: initiate starter position and build as cap approaches threshold."
        ),
        key_risks=[
            "Market cap still well below $18B threshold — needs significant re-rating",
            "US government spending freeze or DOGE cuts could impair revenue",
            "Defense services sector de-rating if geopolitical tensions ease",
            "Committee discretion: even eligible companies may wait quarters for slot",
            "Relatively low analyst coverage (8 analysts) = limited institutional awareness",
        ],
        catalyst_date="Est. 2026/2027 (market cap must first clear $18B threshold)",
        revenue_growth_yoy_pct=8.5,
        ebitda_margin_pct=7.5,
        net_debt_to_ebitda=3.8,
        roe_pct=14.0,
    )

    result = score_inclusion_candidate(candidate)
    print_inclusion_report(result, candidate)


# ─────────────────────────────────────────────────────────────────────────────
# CANDIDATE 3 — Robinhood Markets (HOOD) — FinTech, Fast-Growing, Near Threshold
# ─────────────────────────────────────────────────────────────────────────────
# Robinhood went public July 2021 at $38 (IPO). By early 2026 stock recovered
# strongly from lows driven by crypto bull market and options growth.
# Market cap crossed $20B in late 2025. Now clearly in eligibility zone.
# Not yet in S&P 400 (critical gap in the natural upgrade path).
# But: strong momentum + clear eligibility + retail sentiment tailwind.

def analyse_robinhood() -> None:
    """Robinhood Markets — direct S&P 500 inclusion candidate (not via S&P 400)."""

    screen = SP500EligibilityScreen(
        company_name="Robinhood Markets Inc.",
        ticker="HOOD",
        exchange="NASDAQ",
        us_domicile=True,
        market_cap_usd_bn=22.0,             # Crossed $18B threshold
        float_adjusted_market_cap_usd_bn=19.0,
        annual_dollar_value_traded_usd_bn=55.0,    # High retail trading volume
        float_pct=73.0,
        recent_quarter_earnings_positive=True,
        trailing_4q_earnings_positive=True,
        months_listed=54.0,                  # Listed July 2021 — seasoning satisfied
        current_index_membership=None,        # Not in S&P 400 — direct inclusion candidate
        ipoq_date="Jul 2021",
        sector_gics="Financials — Capital Markets",
        analyst_coverage_count=18,
    )

    momentum = MomentumProfile(
        return_1m_pct=12.0,
        return_3m_pct=38.0,
        return_6m_pct=95.0,
        return_12m_pct=180.0,     # Massive recovery from 2022 lows
        rs_percentile=94,
        benchmark_return_12m_pct=24.0,
        above_50d_ma=True,
        above_200d_ma=True,
        volume_trend="expanding",
        distance_from_52w_high_pct=-5.0,
        distance_from_52w_low_pct=+215.0,
    )

    pre_ann = PreAnnouncementWindow(
        current_phase=InclusionPhase.ACCUMULATE,   # Eligibility satisfied, momentum strong
        estimated_days_to_announcement=45,
        estimated_days_to_effective_date=55,
        estimated_forced_buying_usd_m=2_100,   # ~$2.1B forced buying
        estimated_index_weight_pct=0.14,
        adv_days_to_absorb=15.0,    # High ADV days — meaningful price impact
        avg_announcement_day_return_pct=3.4,
        avg_pre_announcement_drift_pct=3.5,    # Higher: low short-term float
        avg_effective_date_bump_pct=1.5,
        avg_30d_post_reversal_pct=-2.5,
    )

    candidate = IndexInclusionCandidate(
        company_name="Robinhood Markets Inc.",
        ticker="HOOD",
        exchange="NASDAQ",
        sector="Financials — Capital Markets / FinTech",
        country="United States",
        target_index=IndexFamily.SP500,
        current_price=38.50,
        currency="USD",
        market_cap_local_m=22_000,
        market_cap_usd_m=22_000,
        sp500_screen=screen,
        momentum=momentum,
        pre_announcement=pre_ann,
        thesis_summary=(
            "Robinhood crossed S&P 500 eligibility in Q4 2025: mktcap $22B, "
            "trailing 4Q GAAP positive, liquidity ratio >2x. All gates cleared. "
            "Crypto bull market 2024/25 drove explosive PFOF + crypto revenue growth. "
            "Now in ACCUMULATE phase: smart money front-running likely inclusion. "
            "Without S&P 400 membership the committee timing is less predictable — "
            "but once eligible, stocks typically wait 1–3 quarters for a slot to open. "
            "Momentum is exceptional (RS 94th pct, 12M +180%) — confirms institutional interest. "
            "Risk: committee may be cautious given prior losses and retail-centric revenue model."
        ),
        key_risks=[
            "Not in S&P 400 — less predictable timing vs natural promotion path",
            "Committee may perceive business model as volatile (crypto-dependent revenue)",
            "Regulatory risk: SEC/FINRA actions on PFOF model could impair earnings",
            "Strong momentum may already price in significant inclusion premium",
            "High retail ownership creates sentiment-driven volatility",
        ],
        catalyst_date="Est. Q2/Q3 2026 (committee has discretion; slot must open)",
        revenue_growth_yoy_pct=35.0,
        ebitda_margin_pct=22.0,
        roe_pct=12.0,
    )

    result = score_inclusion_candidate(candidate)
    print_inclusion_report(result, candidate)


# ─────────────────────────────────────────────────────────────────────────────
# CANDIDATE 4 — Arm Holdings (ARM) — Semiconductors, UK HQ but US-listed
# ─────────────────────────────────────────────────────────────────────────────
# ARM listed on NASDAQ in September 2023. UK-domiciled but US-listed.
# Key gate risk: S&P 500 requires US domicile. ARM is incorporated in UK.
# This is an EXCLUSION example — passes most quantitative gates but fails
# the domicile gate. Useful for showing what NOT to include in screen.

def analyse_arm_exclusion_case() -> None:
    """Arm Holdings — fails S&P 500 domicile gate (non-US incorporated). Exclusion analysis."""

    screen = SP500EligibilityScreen(
        company_name="Arm Holdings plc",
        ticker="ARM",
        exchange="NASDAQ",
        us_domicile=False,          # ← FAILS: UK-incorporated; foreign private issuer
        market_cap_usd_bn=145.0,    # Well above threshold
        float_adjusted_market_cap_usd_bn=25.0,  # Low float — SoftBank owns ~90%
        annual_dollar_value_traded_usd_bn=35.0,
        float_pct=10.5,             # ← FAILS: float <50% (SoftBank 90% lock-up)
        recent_quarter_earnings_positive=True,
        trailing_4q_earnings_positive=True,
        months_listed=17.0,
        current_index_membership="NASDAQ 100 (already included)",
        ipoq_date="Sep 2023",
        sector_gics="Information Technology — Semiconductors",
        analyst_coverage_count=35,
    )

    candidate = IndexInclusionCandidate(
        company_name="Arm Holdings plc",
        ticker="ARM",
        exchange="NASDAQ",
        sector="Information Technology — Semiconductors & IP",
        country="United Kingdom (US-listed)",
        target_index=IndexFamily.SP500,
        current_price=165.0,
        currency="USD",
        market_cap_local_m=145_000,
        market_cap_usd_m=145_000,
        sp500_screen=screen,
        thesis_summary=(
            "ARM FAILS S&P 500 eligibility on TWO hard gates: "
            "(1) Non-US domicile — incorporated in UK as foreign private issuer. "
            "(2) Float <50% — SoftBank retains ~90% stake, severely limiting float. "
            "Despite $145B market cap and NASDAQ 100 membership, S&P 500 requires: "
            "US incorporation, ≥50% float, and annual DVTR ≥ 1.0x float-adj mktcap. "
            "LESSON: screen for domicile and float FIRST before building an inclusion thesis. "
            "For ARM: re-evaluate if SoftBank reduces stake below 50% (would also boost float). "
            "Until then, the S&P 500 inclusion trade is NOT available for ARM."
        ),
        key_risks=[
            "S&P 500 INELIGIBLE: UK domicile fails US domicile requirement",
            "S&P 500 INELIGIBLE: SoftBank stake means float <50%",
            "Inclusion thesis requires SoftBank to distribute/sell significant stake",
            "If SoftBank does sell down, ARM qualifies — monitor SoftBank block sales",
        ],
        catalyst_date="Conditional: eligible only if SoftBank reduces to <50% AND redomicile",
    )

    result = score_inclusion_candidate(candidate)
    print_inclusion_report(result, candidate)


# ─────────────────────────────────────────────────────────────────────────────
# METHODOLOGY SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

def print_sp500_methodology() -> None:
    """Print the S&P 500 inclusion screening methodology."""
    print()
    print("═" * 72)
    print("  S&P 500 INCLUSION STRATEGY — METHODOLOGY")
    print("═" * 72)
    print("""
  STEP 1: SCREEN FOR ELIGIBILITY (Update monthly)
  ─────────────────────────────────────────────────
  Hard gates (ALL must pass):
    □ US domicile (incorporated in US, primary listing NYSE/NASDAQ/CBOE)
    □ Market cap ≥ $18B (2025 threshold, adjusted annually by committee)
    □ Float-adjusted market cap ≥ $5.8B (30% of market cap floor)
    □ Public float ≥ 50% of shares outstanding
    □ Annual dollar value traded ≥ 1.0x float-adjusted market cap
    □ GAAP earnings positive: most recent quarter AND trailing 4-quarter sum
    □ Listed ≥ 12 months (IPO seasoning — applies to spinoffs too)

  Soft factors (committee weighs, not hard rules):
    □ Sector representation (committee seeks sector balance)
    □ Company not already in a rival index (e.g. Dow Jones)
    □ Stability of business model (committee avoids volatile/speculative)
    □ S&P 400 membership (natural promotion path — highest predictability)

  STEP 2: RANK BY PROMOTION PROBABILITY
  ──────────────────────────────────────
    Tier A: S&P 400 member + all hard gates satisfied → 70–80% probability within 2 quarters
    Tier B: Not in S&P 400 + all hard gates satisfied → 20–40% probability within 2 quarters
    Tier C: 1 gate failing but close → Watch list; revisit in 30 days

  STEP 3: MOMENTUM FILTER
  ─────────────────────────
    Minimum acceptable momentum for new position: RS percentile ≥ 60th
    Strong entry signal: RS ≥ 75th, above 200d MA, expanding volume
    Disqualify: RS < 40th percentile (momentum not supporting thesis)

  STEP 4: POSITION SIZING BY PHASE
  ──────────────────────────────────
    Phase 0 SCREEN     → 0% (watch only)
    Phase 1 ACCUMULATE → 25–50% of target size  ← BEST ENTRY
    Phase 2 SIZE UP    → 50–100% of target size
    Phase 3 ANNOUNCE   → Hold; no new money
    Phase 4 EFFECTIVE  → Trim 50–75%
    Phase 5 FADE       → Exit remaining

  STEP 5: EXPECTED RETURN DECOMPOSITION
  ────────────────────────────────────────
    Pre-ann drift    (Phase 1–2):  +2.5% avg  [your primary alpha]
    Announcement gap (Phase 3):    +3.4% avg  [hold if you own; don't chase]
    Effective date   (Phase 4):    +1.5% avg  [final squeeze; then sell]
    Post-reversal    (Phase 5):   −1.8% avg  [exit before this]
    ─────────────────────────────────────────
    Total captured alpha (Phase 1 entry, Phase 4 exit): ~7.4% avg
    On ~6-week holding period → annualised ~65% IRR if repeatable

  STEP 6: RISK MANAGEMENT
  ─────────────────────────
    Stop-loss: if stock falls below 200d MA during accumulation → reduce to 0
    Sector concentration: max 2–3 inclusion plays simultaneously
    Crowding risk: if >10 analyst notes mention "S&P 500 candidate" → reduce sizing
    Earnings risk: next quarterly earnings date must be AFTER expected inclusion date
""")
    print("═" * 72)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run() -> None:
    """Run all S&P 500 inclusion analyses."""
    print_sp500_methodology()
    analyse_gev_reference_case()
    analyse_amentum()
    analyse_robinhood()
    analyse_arm_exclusion_case()


if __name__ == "__main__":
    run()
