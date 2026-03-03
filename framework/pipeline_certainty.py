"""
Pipeline Certainty — Near-Certain Future Revenue Framework
===========================================================
The central insight this module formalises:

  In most industries, "future revenue" is a FORECAST — you model
  customer demand, market share, price trends, and apply a discount
  rate to account for all the uncertainty in those assumptions.

  In EU-funded infrastructure, "future revenue" is a PIPELINE —
  the money is legally committed in signed treaties, publicly listed
  in procurement calendars, and the government faces financial penalties
  for NOT spending it. You're not forecasting demand; you're reading
  a public schedule.

  These are categorically different risk profiles.

Why this matters for valuation:
  - A normal DCF discounts uncertain future cash flows at 10-15%
  - A pipeline DCF should discount at 5-8% for signed/scheduled items
    (risk is execution, not existence)
  - The difference in NPV between these two discount rates for the same
    cash flow stream is 30-50% higher valuation

The module answers: "How much of this company's future revenue is
already written down somewhere in a government document — and how
certain is that document?"

Applicable to:
  - Rail: PKP PLK Investment Plan (Poland), Network Rail CP7 (UK), SNCF Réseau
  - Roads: GDDKiA Multi-Year Programme (Poland), Highways England RIS
  - Utilities: Ofgem RIIO-T3 (UK transmission), EU TYNDP
  - Defence: multi-year framework contracts, NATO spending commitments
  - Healthcare: government capitation contracts, NHS ISFE programmes
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import math


# ──────────────────────────────────────────────────────────────────────
# Certainty levels — the core taxonomy
# ──────────────────────────────────────────────────────────────────────

class CertaintyLevel(Enum):
    """
    How certain is it that this revenue will exist in the market?
    (Separate from whether THIS company wins it.)
    """
    SIGNED         = "signed"       # Contract signed, revenue recognition only needs time
    AWARDED        = "awarded"      # Won the tender, contract being finalised (~95%)
    PREFERRED      = "preferred"    # Lowest bidder, evaluation complete, pending protest (~88%)
    TENDERED       = "tendered"     # Bid submitted, result pending (~40% win rate)
    SCHEDULED      = "scheduled"    # Named in public procurement calendar, tender upcoming
    COMMITTED      = "committed"    # EU/govt funding earmarked, project defined but not yet tendered
    PLANNED        = "planned"      # In multi-year investment programme, subject to review
    INDICATIVE     = "indicative"   # Government signals intent; no formal commitment yet


# Probability that the MARKET OPPORTUNITY exists (not that this company wins it)
MARKET_EXISTENCE_PROBABILITY = {
    CertaintyLevel.SIGNED:     1.00,
    CertaintyLevel.AWARDED:    0.97,
    CertaintyLevel.PREFERRED:  0.92,
    CertaintyLevel.TENDERED:   0.85,   # Tender is open → work almost certainly proceeds
    CertaintyLevel.SCHEDULED:  0.82,
    CertaintyLevel.COMMITTED:  0.75,
    CertaintyLevel.PLANNED:    0.62,
    CertaintyLevel.INDICATIVE: 0.45,
}

# Appropriate discount rate for NPV calculation
# (Signed = near-riskless; Indicative = normal project risk)
PIPELINE_DISCOUNT_RATE = {
    CertaintyLevel.SIGNED:     0.06,
    CertaintyLevel.AWARDED:    0.07,
    CertaintyLevel.PREFERRED:  0.07,
    CertaintyLevel.TENDERED:   0.09,
    CertaintyLevel.SCHEDULED:  0.09,
    CertaintyLevel.COMMITTED:  0.10,
    CertaintyLevel.PLANNED:    0.12,
    CertaintyLevel.INDICATIVE: 0.15,
}

# What a "normal" DCF analyst would use for comparable speculative revenue
SPECULATIVE_DISCOUNT_RATE = 0.15


# ──────────────────────────────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────────────────────────────

@dataclass
class PipelineItem:
    """
    A single identifiable block of future work in the public market.
    This is NOT a company order — it's a programme/tender in the market
    that the company could compete for.
    """
    name: str
    program_name: str                   # e.g. "PKP PLK Investment Plan 2024-2030"
    certainty: CertaintyLevel
    total_program_value_m: float        # Total value of this programme/contract
    company_addressable_pct: float      # % of the program the company can technically bid
    company_win_probability: float      # Realistic market share / competitive position (0-1)
    company_consortium_share: float     # If JV/consortium: company's % of that contract (0-1)
    revenue_start_year: float           # Years from now when revenue recognition begins
    revenue_duration_years: float       # How many years the contract spans
    margin_pct: float                   # Expected EBITDA margin on this type of work
    public_source: str                  # Where you can verify this
    notes: str = ""

    @property
    def addressable_value_m(self) -> float:
        return self.total_program_value_m * self.company_addressable_pct

    @property
    def expected_revenue_m(self) -> float:
        """Expected value to the company: addressable × win prob × consortium share"""
        return (self.addressable_value_m
                * self.company_win_probability
                * self.company_consortium_share
                * MARKET_EXISTENCE_PROBABILITY[self.certainty])

    @property
    def expected_annual_revenue_m(self) -> float:
        return self.expected_revenue_m / max(self.revenue_duration_years, 0.5)

    @property
    def expected_ebitda_m(self) -> float:
        return self.expected_revenue_m * self.margin_pct / 100

    @property
    def npv_m(self) -> float:
        """
        NPV using pipeline-appropriate discount rate.
        Models a uniform annual cash flow starting at revenue_start_year.
        """
        r = PIPELINE_DISCOUNT_RATE[self.certainty]
        annual_cf = self.expected_ebitda_m / max(self.revenue_duration_years, 0.5)
        npv = 0.0
        for yr in range(int(self.revenue_duration_years)):
            t = self.revenue_start_year + yr + 0.5  # mid-year convention
            npv += annual_cf / (1 + r) ** t
        return npv

    @property
    def npv_speculative_m(self) -> float:
        """What a standard DCF would give (higher discount rate)"""
        r = SPECULATIVE_DISCOUNT_RATE
        annual_cf = self.expected_ebitda_m / max(self.revenue_duration_years, 0.5)
        npv = 0.0
        for yr in range(int(self.revenue_duration_years)):
            t = self.revenue_start_year + yr + 0.5
            npv += annual_cf / (1 + r) ** t
        return npv

    @property
    def certainty_premium_m(self) -> float:
        """Extra NPV value vs. standard speculative DCF, due to low discount rate"""
        return self.npv_m - self.npv_speculative_m


@dataclass
class PipelineAnalysis:
    company_name: str
    current_annual_revenue_m: float
    current_ebitda_margin_pct: float
    items: list[PipelineItem]
    # ── Market-level metrics (before company win probability) ─────────
    # These answer: "Is the MARKET OPPORTUNITY real and committed?"
    total_market_opportunity_m: float      # Addressable × market existence probability
    market_to_revenue_ratio: float         # Market opportunity / current annual revenue
    market_certainty_score_pct: float      # Weighted avg market existence probability
    # ── Company-level metrics (after win probability) ─────────────────
    # These answer: "What share of that certain market will THIS company capture?"
    total_expected_revenue_m: float        # market opportunity × win probability × consortium share
    total_high_cert_revenue_m: float       # SIGNED/AWARDED items only (near-certain company revenue)
    company_capture_pct: float             # expected / market opportunity (company's implicit share)
    forward_revenue_years: float           # Weighted average start year
    total_npv_m: float                     # NPV using pipeline-appropriate discount rates
    total_npv_speculative_m: float         # NPV using standard speculative DCF
    certainty_premium_m: float             # Valuation uplift from using correct (lower) discount rate
    revenue_not_speculation_pct: float     # % of expected company revenue from high-certainty levels
    # ── Verdicts ──────────────────────────────────────────────────────
    market_verdict: str    # CERTAIN_MARKET | PROBABLE_MARKET | SPECULATIVE_MARKET
    company_verdict: str   # PIPELINE_BACKED | PIPELINE_SUPPORTED | CONVENTIONAL_FORECAST


def analyse_pipeline(
    company_name: str,
    current_annual_revenue_m: float,
    current_ebitda_margin_pct: float,
    items: list[PipelineItem],
) -> PipelineAnalysis:

    # ── Market-level ──────────────────────────────────────────────────
    # Market opportunity = addressable value × P(market exists), ignoring win probability
    total_market_opp = sum(
        i.addressable_value_m * MARKET_EXISTENCE_PROBABILITY[i.certainty]
        for i in items
    )
    market_ratio = total_market_opp / current_annual_revenue_m if current_annual_revenue_m > 0 else 0.0

    # Weighted average market existence probability (by addressable value)
    total_addressable = sum(i.addressable_value_m for i in items)
    if total_addressable > 0:
        market_cert_score = sum(
            MARKET_EXISTENCE_PROBABILITY[i.certainty] * i.addressable_value_m
            for i in items
        ) / total_addressable * 100
    else:
        market_cert_score = 0.0

    # ── Company-level ─────────────────────────────────────────────────
    total_expected  = sum(i.expected_revenue_m for i in items)
    total_npv       = sum(i.npv_m for i in items)
    total_npv_spec  = sum(i.npv_speculative_m for i in items)
    cert_premium    = total_npv - total_npv_spec

    high_certainty_levels = {
        CertaintyLevel.SIGNED, CertaintyLevel.AWARDED,
        CertaintyLevel.COMMITTED, CertaintyLevel.SCHEDULED,
    }
    high_cert_rev = sum(
        i.expected_revenue_m for i in items if i.certainty in high_certainty_levels
    )

    if total_expected > 0:
        fwd_years = sum(
            i.revenue_start_year * i.expected_revenue_m for i in items
        ) / total_expected
        company_capture = total_expected / total_market_opp * 100 if total_market_opp > 0 else 0.0
    else:
        fwd_years = 0.0
        company_capture = 0.0

    company_ratio = total_expected / current_annual_revenue_m if current_annual_revenue_m > 0 else 0.0

    # ── Market verdict: based on existence probability of the MARKET ──
    # Separate from company positioning — asks "is the money really there?"
    if market_cert_score >= 72 and market_ratio >= 3.0:
        market_verdict = "CERTAIN_MARKET"
    elif market_cert_score >= 60 and market_ratio >= 1.5:
        market_verdict = "PROBABLE_MARKET"
    else:
        market_verdict = "SPECULATIVE_MARKET"

    # ── Company verdict: based on company's EXPECTED capture ─────────
    if company_ratio >= 1.5 and (high_cert_rev / total_expected * 100 if total_expected else 0) >= 70:
        company_verdict = "PIPELINE_BACKED"
    elif company_ratio >= 0.5:
        company_verdict = "PIPELINE_SUPPORTED"
    else:
        company_verdict = "CONVENTIONAL_FORECAST"

    return PipelineAnalysis(
        company_name=company_name,
        current_annual_revenue_m=current_annual_revenue_m,
        current_ebitda_margin_pct=current_ebitda_margin_pct,
        items=items,
        total_market_opportunity_m=total_market_opp,
        market_to_revenue_ratio=market_ratio,
        market_certainty_score_pct=market_cert_score,
        total_expected_revenue_m=total_expected,
        total_high_cert_revenue_m=high_cert_rev,
        company_capture_pct=company_capture,
        forward_revenue_years=fwd_years,
        total_npv_m=total_npv,
        total_npv_speculative_m=total_npv_spec,
        certainty_premium_m=cert_premium,
        revenue_not_speculation_pct=(high_cert_rev / total_expected * 100) if total_expected else 0.0,
        market_verdict=market_verdict,
        company_verdict=company_verdict,
    )


def print_pipeline_report(analysis: PipelineAnalysis) -> None:
    sep  = "═" * 72
    thin = "─" * 72
    curr = analysis.current_annual_revenue_m

    print(f"\n{sep}")
    print(f"  PIPELINE CERTAINTY ANALYSIS — {analysis.company_name}")
    print(sep)
    mv_icon = {"CERTAIN_MARKET": "✓", "PROBABLE_MARKET": "~", "SPECULATIVE_MARKET": "✗"}
    cv_icon = {"PIPELINE_BACKED": "✓", "PIPELINE_SUPPORTED": "~", "CONVENTIONAL_FORECAST": "✗"}
    print(f"\n  Market verdict  : {mv_icon[analysis.market_verdict]} {analysis.market_verdict}  "
          f"(market certainty score {analysis.market_certainty_score_pct:.0f}%,  "
          f"market / revenue {analysis.market_to_revenue_ratio:.1f}x)")
    print(f"  Company verdict : {cv_icon[analysis.company_verdict]} {analysis.company_verdict}  "
          f"(expected share {analysis.company_capture_pct:.1f}% of addressable market)")
    print(f"  Current revenue : PLN {curr:.0f}m / year")

    print(f"\n{thin}")
    print("  PIPELINE ITEMS")
    print(thin)
    print(f"\n  {'Name':<35} {'Cert':<11} {'AddrMkt':>8}  {'WinP':>5}  {'ExpRev':>7}  {'ExpAnnRev':>9}")
    print(f"  {'-'*35} {'-'*11} {'-'*8}  {'-'*5}  {'-'*7}  {'-'*9}")
    for item in sorted(analysis.items, key=lambda x: x.certainty.value):
        print(
            f"  {item.name[:35]:<35} {item.certainty.value:<11} "
            f"{item.addressable_value_m:>7.0f}m  "
            f"{item.company_win_probability*100:>4.0f}%  "
            f"{item.expected_revenue_m:>6.0f}m  "
            f"{item.expected_annual_revenue_m:>8.0f}m"
        )

    print(f"\n{thin}")
    print("  MARKET vs COMPANY SPLIT")
    print(thin)
    print(f"\n  Market opportunity (addrssble × P(exists))  : PLN {analysis.total_market_opportunity_m:.0f}m  "
          f"({analysis.market_to_revenue_ratio:.1f}x current revenue)")
    print(f"  Market certainty score (weighted avg)       : {analysis.market_certainty_score_pct:.0f}%")
    print(f"\n  Company expected revenue (after win prob)   : PLN {analysis.total_expected_revenue_m:.0f}m  "
          f"({analysis.total_expected_revenue_m / max(analysis.current_annual_revenue_m, 1):.1f}x current revenue)")
    print(f"  Implicit market share                       : {analysis.company_capture_pct:.1f}%")
    print(f"  High-certainty company revenue (≥COMMITTED) : PLN {analysis.total_high_cert_revenue_m:.0f}m "
          f"({analysis.revenue_not_speculation_pct:.0f}% of expected)")
    print(f"\n  NPV (pipeline discount rates)  : PLN {analysis.total_npv_m:.0f}m")
    print(f"  NPV (standard speculative DCF) : PLN {analysis.total_npv_speculative_m:.0f}m")
    print(f"  Certainty premium              : +PLN {analysis.certainty_premium_m:.0f}m "
          f"({analysis.certainty_premium_m / max(analysis.total_npv_speculative_m, 1) * 100:.0f}% extra value)")

    print(f"\n{thin}")
    print("  WHY THIS IS NOT A REVENUE FORECAST")
    print(thin)
    print(f"""
  A revenue FORECAST asks: "Will customers buy our product?"
  → High uncertainty; requires assumptions about demand, competition, macro

  A pipeline ANALYSIS separates TWO different questions:
    Q1: Is the MARKET OPPORTUNITY real? → {analysis.market_verdict}
    Q2: What share does THIS company capture? → {analysis.company_verdict}

  For a CERTAIN_MARKET, Q1 is already answered — not a forecast, a fact.
  Q2 is the only remaining uncertainty (win probability / market share).

  The question shifts from "will the market exist?" to
  "what market share will this company capture?"

  Market share risk (win probability) ≠ demand risk (will anyone build this?)

  EU infrastructure contracts are backed by:
    1. Signed EU funding agreements (Poland cannot return funds without penalty)
    2. Legally binding procurement calendars (PKP PLK, GDDKiA publish 5-year plans)
    3. TEN-T (Trans-European Transport Network) compliance obligations
    4. KPO (National Recovery Plan) EU treaty commitments
    5. Political cost of NOT spending (unemployment, lost EU transfers)

  The appropriate DCF discount rate for SIGNED pipeline items is ~6%,
  not the 15% applied to speculative growth revenue.
  That difference alone creates {analysis.certainty_premium_m:.0f}m PLN of additional NPV.
""")
    print(sep)
