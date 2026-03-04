"""
Sum-of-Parts (SOTP) / NAV Discount Analysis
=============================================
For holding companies, conglomerates, and diversified businesses where
the whole trades at a discount to the sum of its parts.

The discount exists because:
  1. Complexity: analysts can't model 5 segments at once
  2. Index constraints: small-cap segments wouldn't pass thresholds
  3. Conglomerate discount: market assumes management destroys value
  4. One bad division poisons perception of the whole
  5. Liquidity: if you owned each part separately, you could sell them;
     in a conglomerate, you can't

The SOTP analysis answers:
  Q1: What would each division be worth as a standalone?
  Q2: What is the total NAV?
  Q3: What is the current discount to NAV?
  Q4: Which division dominates the value?
  Q5: Are there natural trade buyers for each division?
  Q6: What catalyst would crystallise the discount?

Comparable transaction approach:
  Most reliable approach is to look at recent M&A transactions in each
  sector — what do buyers actually pay? Not theoretical DCFs but signed deals.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SOTPSegment:
    """A single business segment in a SOTP analysis."""
    name:               str
    segment_type:       str          # "operations" | "financial_asset" | "real_estate" | "debt"

    # ── Revenue & earnings ──────────────────────────────────────────
    annual_revenue_m:   float        # In local currency millions
    ebitda_m:           float        # In local currency millions
    ebitda_margin_pct:  float        # Derived from above but can override

    # ── Multiple ranges (bear/base/bull) ───────────────────────────
    # For operating segments: EV/EBITDA multiples
    # For financial assets: carried value / market value
    # For real estate: cap rate or per-sqm market comps
    multiple_bear:      float        # e.g., 5.0 (distressed sale)
    multiple_base:      float        # e.g., 8.0 (fair market)
    multiple_bull:      float        # e.g., 12.0 (strategic premium)
    multiple_basis:     str = "EV/EBITDA"  # What the multiple applies to

    # ── Qualitative ─────────────────────────────────────────────────
    natural_buyers:     list = field(default_factory=list)
    recent_comps:       list = field(default_factory=list)  # (buyer, seller, multiple, year)
    trend:              str = "stable"     # "growing" / "stable" / "declining"
    carve_out_cost_m:   float = 0.0        # Cost to separate from parent (legal, IT, etc.)
    notes:              str = ""

    # ── Computed (filled by analyse_sotp) ──────────────────────────
    value_bear_m:       float = 0.0
    value_base_m:       float = 0.0
    value_bull_m:       float = 0.0
    value_pct_of_total: float = 0.0   # Share of total NAV (base case)

    def compute_values(self):
        """Compute segment values across scenarios."""
        if self.multiple_basis == "EV/EBITDA":
            basis = self.ebitda_m
        elif self.multiple_basis == "EV/Revenue":
            basis = self.annual_revenue_m
        elif self.multiple_basis == "Book":
            basis = self.ebitda_m  # Treat ebitda_m as book value if basis="Book"
        else:
            basis = self.ebitda_m

        self.value_bear_m = max(0.0, basis * self.multiple_bear - self.carve_out_cost_m)
        self.value_base_m = max(0.0, basis * self.multiple_base - self.carve_out_cost_m)
        self.value_bull_m = max(0.0, basis * self.multiple_bull - self.carve_out_cost_m)


@dataclass
class SOTPAnalysis:
    """Full SOTP analysis for a company."""
    company_name:           str
    ticker:                 str
    exchange:               str
    currency:               str
    current_market_cap_m:   float
    net_debt_m:             float = 0.0    # Positive = debt, Negative = net cash
    minority_interests_m:   float = 0.0    # Value of minorities to subtract
    central_costs_m:        float = 0.0    # Group central costs (capitalised as negative)
    central_cost_multiple:  float = 8.0    # EV/EBITDA multiple for central cost drag
    segments:               list = field(default_factory=list)

    # ── Computed by analyse_sotp ─────────────────────────────────
    nav_bear_m:             float = 0.0
    nav_base_m:             float = 0.0
    nav_bull_m:             float = 0.0
    discount_to_nav_pct:    float = 0.0    # (market cap / base NAV - 1): negative = trading at discount
    nav_to_market_cap_ratio: float = 0.0
    dominant_segment:       str = ""


def analyse_sotp(analysis: SOTPAnalysis) -> SOTPAnalysis:
    """
    Compute all segment values and derive the total NAV + discount.
    Mutates and returns the analysis object.
    """
    # Step 1: Compute segment values
    for seg in analysis.segments:
        seg.compute_values()

    # Step 2: Sum
    total_bear = sum(s.value_bear_m for s in analysis.segments)
    total_base = sum(s.value_base_m for s in analysis.segments)
    total_bull = sum(s.value_bull_m for s in analysis.segments)

    # Step 3: Central cost drag
    central_drag = analysis.central_costs_m * analysis.central_cost_multiple
    total_bear -= central_drag
    total_base -= central_drag
    total_bull -= central_drag

    # Step 4: Bridge from EV to equity (subtract net debt, minority interests)
    bridge = analysis.net_debt_m + analysis.minority_interests_m
    analysis.nav_bear_m = max(0.0, total_bear - bridge)
    analysis.nav_base_m = max(0.0, total_base - bridge)
    analysis.nav_bull_m = max(0.0, total_bull - bridge)

    # Step 5: Discount calculation
    if analysis.nav_base_m > 0:
        analysis.discount_to_nav_pct   = (analysis.current_market_cap_m / analysis.nav_base_m - 1) * 100
        analysis.nav_to_market_cap_ratio = analysis.nav_base_m / analysis.current_market_cap_m

    # Step 6: % of total NAV per segment (base case)
    for seg in analysis.segments:
        if analysis.nav_base_m > 0:
            seg.value_pct_of_total = seg.value_base_m / (analysis.nav_base_m + bridge) * 100

    # Step 7: Dominant segment
    if analysis.segments:
        dominant = max(analysis.segments, key=lambda s: s.value_base_m)
        analysis.dominant_segment = dominant.name

    return analysis


def print_sotp_report(analysis: SOTPAnalysis):
    """Print a formatted SOTP analysis report."""
    if analysis.nav_base_m == 0:
        analysis = analyse_sotp(analysis)

    sep  = "═" * 80
    thin = "─" * 80

    print(f"\n{sep}")
    print(f"  SUM-OF-PARTS (SOTP) / NAV ANALYSIS")
    print(f"  {analysis.company_name} ({analysis.ticker}:{analysis.exchange})")
    print(sep)

    # ── Summary box ──────────────────────────────────────────────────────
    discount_abs = abs(analysis.discount_to_nav_pct)
    direction    = "DISCOUNT" if analysis.discount_to_nav_pct < 0 else "PREMIUM"
    nav_ratio    = analysis.nav_to_market_cap_ratio

    print(f"\n  {'Current Market Cap':<30}: {analysis.currency} {analysis.current_market_cap_m:>10,.0f}m")
    print(f"  {'SOTP NAV (bear)':<30}: {analysis.currency} {analysis.nav_bear_m:>10,.0f}m")
    print(f"  {'SOTP NAV (base)':<30}: {analysis.currency} {analysis.nav_base_m:>10,.0f}m  ← key figure")
    print(f"  {'SOTP NAV (bull)':<30}: {analysis.currency} {analysis.nav_bull_m:>10,.0f}m")
    print(f"  {'NAV / Market Cap':<30}: {nav_ratio:>10.2f}x")
    print(f"  {'Trading at':<30}: {discount_abs:>9.1f}% {direction} to NAV (base)")
    print(f"  {'Dominant segment':<30}: {analysis.dominant_segment}")

    # ── Per-segment breakdown ──────────────────────────────────────────
    print(f"\n{thin}")
    print(f"  SEGMENT BREAKDOWN  (all values in {analysis.currency} millions)")
    print(thin)
    print(f"\n  {'Segment':<28} {'Revenue':>9} {'EBITDA':>9} "
          f"{'Multiple':<10} {'Bear':>9} {'Base':>9} {'Bull':>9} {'% NAV':>7}")
    print(f"  {'-'*28} {'-'*9} {'-'*9} {'-'*10} {'-'*9} {'-'*9} {'-'*9} {'-'*7}")

    for seg in sorted(analysis.segments, key=lambda s: s.value_base_m, reverse=True):
        mult_str = f"{seg.multiple_bear:.0f}-{seg.multiple_bull:.0f}x"
        pct_str = f"{seg.value_pct_of_total:.0f}%"
        print(f"  {seg.name[:28]:<28} {seg.annual_revenue_m:>9,.0f} {seg.ebitda_m:>9,.0f} "
              f"{mult_str:<10} {seg.value_bear_m:>9,.0f} {seg.value_base_m:>9,.0f} "
              f"{seg.value_bull_m:>9,.0f} {pct_str:>7}")

    # Subtotals
    print(f"  {'-'*28} {'-'*9} {'-'*9} {'-'*10} {'-'*9} {'-'*9} {'-'*9} {'-'*7}")
    gross_bear = sum(s.value_bear_m for s in analysis.segments)
    gross_base = sum(s.value_base_m for s in analysis.segments)
    gross_bull = sum(s.value_bull_m for s in analysis.segments)
    print(f"  {'GROSS EV (segments)':<28} {'':>9} {'':>9} {'':>10} "
          f"{gross_bear:>9,.0f} {gross_base:>9,.0f} {gross_bull:>9,.0f} {'':>7}")

    central = analysis.central_costs_m * analysis.central_cost_multiple
    if central > 0:
        print(f"  {'Group central costs':<28} {'':>9} {-analysis.central_costs_m:>9,.0f} "
              f"{'@ '+str(analysis.central_cost_multiple)+'x':<10} "
              f"{-central:>9,.0f} {-central:>9,.0f} {-central:>9,.0f} {'':>7}")

    bridge = analysis.net_debt_m + analysis.minority_interests_m
    if bridge != 0:
        label = "Net cash" if analysis.net_debt_m < 0 else "Net debt + minorities"
        print(f"  {label:<28} {'':>9} {'':>9} {'':>10} "
              f"{-bridge:>9,.0f} {-bridge:>9,.0f} {-bridge:>9,.0f} {'':>7}")

    print(f"  {'═'*28} {'':>9} {'':>9} {'':>10} "
          f"{'═'*9} {'═'*9} {'═'*9} {'═'*7}")
    print(f"  {'NET ASSET VALUE (equity)':<28} {'':>9} {'':>9} {'':>10} "
          f"{analysis.nav_bear_m:>9,.0f} {analysis.nav_base_m:>9,.0f} "
          f"{analysis.nav_bull_m:>9,.0f} {'100%':>7}")
    print(f"  {'Current Market Cap':<28} {'':>9} {'':>9} {'':>10} "
          f"{'':>9} {analysis.current_market_cap_m:>9,.0f} {'':>9} {'':>7}")

    # ── Natural buyers per segment ─────────────────────────────────────
    print(f"\n{thin}")
    print("  NATURAL BUYERS PER SEGMENT (Transaction Comparables)")
    print(thin)
    for seg in analysis.segments:
        if seg.natural_buyers:
            print(f"\n  {seg.name}:")
            for buyer in seg.natural_buyers:
                print(f"    → {buyer}")
        if seg.recent_comps:
            for comp in seg.recent_comps[:2]:
                print(f"      Comp: {comp}")

    # ── Discount context ────────────────────────────────────────────────
    print(f"\n{thin}")
    print("  DISCOUNT CONTEXT & CATALYST PATHS")
    print(thin)

    if nav_ratio >= 2.0:
        print(f"""
  EXTREME DISCOUNT ({nav_ratio:.1f}x NAV coverage):
  The market is valuing the company at less than half of the sum of its parts.
  This typically requires either:
    (a) No catalyst = discount persists indefinitely
    (b) Loss-making division that poisons the rest
    (c) Controlling shareholder with no financial need to act

  IF a catalyst emerges (sale of one division), the remaining parts
  re-rate because the market now sees the asset value is real.
  Partial sale = price discovery event for the whole.
""")
    elif nav_ratio >= 1.5:
        print(f"""
  SIGNIFICANT DISCOUNT ({nav_ratio:.1f}x NAV coverage):
  Common for conglomerates. A 20-30% discount is "normal" complexity discount.
  A 50%+ discount ({nav_ratio:.0f}x coverage) implies the market actively
  expects value destruction OR believes the SOTP assumptions are wrong.
""")

    # ── Upside scenarios ────────────────────────────────────────────────
    print(f"\n  Upside scenarios to target price:")
    if analysis.nav_base_m > 0:
        per_share_nav  = analysis.nav_base_m / analysis.current_market_cap_m
        partial_50_pct = analysis.current_market_cap_m + 0.50 * (analysis.nav_base_m - analysis.current_market_cap_m)
        print(f"    Base (full NAV realised)  : {analysis.currency} {analysis.nav_base_m:,.0f}m  "
              f"= {nav_ratio:.1f}x current market cap")
        print(f"    Partial (50% discount close): {analysis.currency} {partial_50_pct:,.0f}m  "
              f"= {partial_50_pct/analysis.current_market_cap_m:.1f}x current")
        print(f"    Bull (premium NAV)        : {analysis.currency} {analysis.nav_bull_m:,.0f}m  "
              f"= {analysis.nav_bull_m/analysis.current_market_cap_m:.1f}x current")

    print(f"\n{sep}")
