"""
Margin of Safety — Investment vs. Speculation Distinction
==========================================================
Benjamin Graham's definition of investment (Security Analysis, 1934):
  "An investment operation is one which, upon thorough analysis, promises
   safety of principal and an adequate return. Operations not meeting these
   requirements are speculative."

The practical test:
  SPECULATION — the upside requires something NEW to happen:
    growth accelerates, drug gets approved, management gets better,
    macro turns, a new product launches. You are paying for a FUTURE STATE
    that does not yet exist.

  INVESTMENT — the upside requires NOTHING to happen:
    the market price corrects to the value of things that ALREADY EXIST.
    You are paying below the value of the CURRENT STATE.

This module formalises the distinction and quantifies how "investmenty"
(vs. speculative) a pivot thesis is.

The key insight: a thesis can have a large upside AND be non-speculative,
if the upside is triggered by PRICE CORRECTION to existing reality —
not by future events materialising.
"""

from dataclasses import dataclass, field
from typing import Optional
from .models import Company


@dataclass
class SafetyComponent:
    """One verifiable, tangible floor for the stock price."""
    name: str
    value_per_share: float          # PLN (or relevant currency)
    confidence: float               # 0.0 (guess) → 1.0 (audited fact)
    description: str
    how_to_verify: str
    is_liquid: bool                 # Can this be converted to cash within 2 years?


@dataclass
class UpsideMechanism:
    """
    A specific path to value realisation.

    The key distinction:
      requires_future_growth: False → this is CORRECTION of mispricing (investment)
      requires_future_growth: True  → this depends on something new happening (speculative element)
    """
    name: str
    price_target: float
    requires_future_growth: bool
    growth_required_description: Optional[str]   # Only needed if requires_future_growth=True
    correction_logic: str                         # Why does the price move to this level?
    probability: float
    observable_trigger: str                       # What single observable event fires this path?
    months_to_trigger_estimate: int


@dataclass
class MarginOfSafetyAnalysis:
    company_name: str
    entry_price: float
    # The floor — assets you're buying below cost
    safety_components: list[SafetyComponent]
    # The upside mechanisms — correction vs. growth
    upside_mechanisms: list[UpsideMechanism]
    # Derived
    total_floor_value: float             # Sum of safety components × confidence
    speculation_ratio: float             # % of upside that requires future growth (0=pure investment)
    graham_verdict: str                  # "INVESTMENT" | "SPECULATIVE_ELEMENT" | "SPECULATION"
    summary: str


def analyse_margin_of_safety(
    company: Company,
    safety_components: list[SafetyComponent],
    upside_mechanisms: list[UpsideMechanism],
) -> MarginOfSafetyAnalysis:
    """
    Compute the investment vs. speculation ratio and margin of safety floor.
    """
    # ── Floor calculation ─────────────────────────────────────────────
    # Weighted by confidence — a PLN 3.50 asset with 50% confidence
    # contributes PLN 1.75 of real floor
    total_floor = sum(c.value_per_share * c.confidence for c in safety_components)

    # ── Speculation ratio ─────────────────────────────────────────────
    # What proportion of the EXPECTED VALUE comes from mechanisms
    # that require future growth vs. price correction?
    ev_correction = 0.0
    ev_growth     = 0.0

    for m in upside_mechanisms:  # local param — correct reference
        expected_gain = m.probability * (m.price_target - company.current_price)
        if m.requires_future_growth:
            ev_growth += max(expected_gain, 0)
        else:
            ev_correction += max(expected_gain, 0)

    total_ev = ev_correction + ev_growth
    speculation_ratio = (ev_growth / total_ev) if total_ev > 0 else 0.0

    # ── Graham verdict ────────────────────────────────────────────────
    downside_pct = (total_floor - company.current_price) / company.current_price
    if speculation_ratio < 0.20 and downside_pct > -0.30:
        verdict = "INVESTMENT"
    elif speculation_ratio < 0.50:
        verdict = "SPECULATIVE_ELEMENT"
    else:
        verdict = "SPECULATION"

    summary = (
        f"Floor: {total_floor:.2f} vs entry {company.current_price:.2f} "
        f"({downside_pct*100:+.1f}% downside to floor). "
        f"Speculation ratio: {speculation_ratio*100:.0f}% of expected value "
        f"requires future growth. "
        f"Graham verdict: {verdict}."
    )

    return MarginOfSafetyAnalysis(
        company_name=company.name,
        entry_price=company.current_price,
        safety_components=safety_components,
        upside_mechanisms=upside_mechanisms,
        total_floor_value=total_floor,
        speculation_ratio=speculation_ratio,
        graham_verdict=verdict,
        summary=summary,
    )


def print_margin_of_safety_report(analysis: MarginOfSafetyAnalysis) -> None:
    sep  = "═" * 72
    thin = "─" * 72

    print(f"\n{sep}")
    print(f"  MARGIN OF SAFETY — {analysis.company_name}")
    print(f"  Investment vs. Speculation Diagnosis")
    print(sep)

    # ── Floor ─────────────────────────────────────────────────────────
    print(f"\n  DOWNSIDE FLOOR (what you own that already exists)")
    print(thin)
    for c in analysis.safety_components:
        conf_bar = "█" * int(c.confidence * 10) + "░" * (10 - int(c.confidence * 10))
        liquid   = "liquid" if c.is_liquid else "illiquid"
        adj_val  = c.value_per_share * c.confidence
        print(f"\n  {c.name}")
        print(f"    Stated value : {c.value_per_share:.2f} PLN/share")
        print(f"    Confidence   : [{conf_bar}] {c.confidence*100:.0f}%  ({liquid})")
        print(f"    Adj. value   : {adj_val:.2f} PLN/share  (= {c.value_per_share:.2f} × {c.confidence*100:.0f}%)")
        print(f"    Verify via   : {c.how_to_verify}")
        print(f"    Logic        : {c.description}")

    downside_pct = (analysis.total_floor_value - analysis.entry_price) / analysis.entry_price
    print(f"\n  {thin}")
    print(f"  Total confidence-adjusted floor : {analysis.total_floor_value:.2f} PLN")
    print(f"  Entry price                     : {analysis.entry_price:.2f} PLN")
    print(f"  Downside to floor               : {downside_pct*100:+.1f}%")

    # ── Upside mechanisms ─────────────────────────────────────────────
    print(f"\n\n  UPSIDE MECHANISMS (how the price corrects)")
    print(thin)
    print(f"  Key: (C) = Correction of existing mispricing — NOT speculation")
    print(f"       (G) = Requires future Growth / new events — speculative element")
    print()

    total_correction_ev = 0.0
    total_growth_ev     = 0.0

    for m in analysis.upside_mechanisms:
        tag      = "(C)" if not m.requires_future_growth else "(G)"
        gain_pct = (m.price_target - analysis.entry_price) / analysis.entry_price * 100
        ev_gain  = m.probability * (m.price_target - analysis.entry_price)
        if not m.requires_future_growth:
            total_correction_ev += max(ev_gain, 0)
        else:
            total_growth_ev += max(ev_gain, 0)

        print(f"  {tag} {m.name}")
        print(f"     Target : {m.price_target:.2f} PLN  ({gain_pct:+.1f}%)   p={m.probability*100:.0f}%   ~{m.months_to_trigger_estimate}mo")
        print(f"     Trigger: {m.observable_trigger}")
        print(f"     Logic  : {m.correction_logic}")
        if m.requires_future_growth and m.growth_required_description:
            print(f"     ⚠ Requires: {m.growth_required_description}")
        print()

    total_ev = total_correction_ev + total_growth_ev
    spec_pct = (total_growth_ev / total_ev * 100) if total_ev > 0 else 0.0

    print(thin)
    print(f"  Expected value from CORRECTION  : +{total_correction_ev:.2f} PLN/share")
    print(f"  Expected value from GROWTH      : +{total_growth_ev:.2f} PLN/share")
    print(f"  Speculation ratio               : {spec_pct:.0f}% of upside EV requires new events")

    # ── Verdict ───────────────────────────────────────────────────────
    verdict_detail = {
        "INVESTMENT": (
            "The upside is primarily a CORRECTION of mispricing, not a bet on "
            "future events. You're buying existing assets below their verifiable value. "
            "Safety of principal is provided by the floor. This meets Graham's definition."
        ),
        "SPECULATIVE_ELEMENT": (
            "Most of the expected value comes from price correction, but some paths "
            "require future events (activist success, market re-rating). "
            "This is an investment with speculative seasoning — acceptable if sized correctly."
        ),
        "SPECULATION": (
            "The majority of expected value requires future growth or events "
            "that do not yet exist. Graham would call this speculation. "
            "Not inherently bad — but be honest about what you're doing."
        ),
    }[analysis.graham_verdict]

    print(f"\n\n  GRAHAM VERDICT: {analysis.graham_verdict}")
    print(thin)
    print(f"  {verdict_detail}")
    print(f"\n  Summary: {analysis.summary}")
    print(f"\n{sep}\n")
