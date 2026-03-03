"""
Terminal report renderer for the Pivot Opportunity Framework.
Outputs a readable, structured analysis for a single company.
"""

from .models import Company, PivotType
from .scoring import ScoringResult
from .pivot_types import get_playbook


BAR_WIDTH = 20


def _bar(score: float, width: int = BAR_WIDTH) -> str:
    """ASCII progress bar for a 0–10 score."""
    filled = int(round(score / 10 * width))
    return "[" + "█" * filled + "░" * (width - filled) + f"] {score:.1f}/10"


def _tier_badge(tier: str) -> str:
    badges = {
        "HIGH":   "★★★ HIGH CONVICTION",
        "MEDIUM": "★★  MEDIUM",
        "WATCH":  "★   WATCH",
        "PASS":   "    PASS",
    }
    return badges.get(tier, tier)


def print_report(company: Company, result: ScoringResult,
                 suggested_pivot_types: list[PivotType]) -> None:
    sep  = "═" * 72
    thin = "─" * 72

    print(f"\n{sep}")
    print(f"  PIVOT OPPORTUNITY FRAMEWORK — COMPANY ANALYSIS")
    print(f"{sep}")

    print(f"\n  {company.name}  ({company.ticker or 'N/A'} : {company.exchange or '–'})")
    print(f"  {company.sector} | {company.country} | {company.currency}")
    print(f"  Current Price : {company.currency} {company.current_price:.2f}")
    print(f"  Market Cap    : {company.currency} {company.market_cap_m:.0f}M")

    print(f"\n{thin}")
    print(f"  PIVOT SCORE   {result.pivot_score:.1f} / 10     {_tier_badge(result.conviction_tier)}")
    print(thin)

    if result.asymmetry_ratio is not None:
        print(f"  Asymmetry Ratio (Bull / Bear)  : {result.asymmetry_ratio:.1f}x")
    if result.probability_weighted_return_pct is not None:
        print(f"  Probability-Weighted Return    : +{result.probability_weighted_return_pct:.1f}%")
    print(f"  Time Horizon                   : {company.time_horizon_years:.0f} years")

    # ── Dimension scores ──
    print(f"\n{thin}")
    print("  SCORING DIMENSIONS")
    print(thin)

    labels = {
        "asset_asymmetry":     "Asset Asymmetry      ",
        "smart_money_signals": "Smart Money Signals  ",
        "catalyst_clarity":    "Catalyst Clarity     ",
        "downside_protection": "Downside Protection  ",
        "business_quality":    "Business Quality     ",
        "sentiment_discount":  "Sentiment Discount   ",
    }
    for key, label in labels.items():
        score = result.dimension_scores[key]
        notes = result.dimension_notes[key]
        print(f"  {label} {_bar(score)}")
        if notes:
            # Wrap notes to 65 chars
            words, line, lines = notes.split("; "), "", []
            for w in words:
                if len(line) + len(w) + 2 > 60:
                    lines.append(line)
                    line = w
                else:
                    line = f"{line}; {w}" if line else w
            if line:
                lines.append(line)
            for l in lines:
                print(f"    {'':24s}→ {l}")
        print()

    # ── Price scenarios ──
    print(thin)
    print("  PRICE SCENARIOS")
    print(thin)
    for s in sorted(company.scenarios, key=lambda x: x.price_target, reverse=True):
        upside = (s.price_target / company.current_price - 1) * 100
        sign   = "+" if upside >= 0 else ""
        irr_str = f"  IRR ~{s.irr:.0f}%" if s.irr else ""
        print(f"  {s.label.upper():5s}  {company.currency} {s.price_target:.2f}  "
              f"({sign}{upside:.0f}%)  p={s.probability:.0%}{irr_str}")
        print(f"         {s.rationale[:66]}")
        print()

    # ── Pivot types ──
    print(thin)
    print("  PIVOT TYPE PLAYBOOKS (ranked by fit)")
    print(thin)
    types_to_show = suggested_pivot_types[:3] or company.pivot_types[:3]
    for i, pt in enumerate(types_to_show, 1):
        pb = get_playbook(pt)
        print(f"  {i}. [{pt.value.upper()}]")
        print(f"     {pb.one_liner}")
        print(f"     Return range : {pb.typical_return_range}  |  "
              f"Horizon : {pb.typical_horizon_years}y  |  "
              f"Base rate : {pb.base_rate_success}")
        print(f"     Top signals to verify:")
        for sig in pb.key_signals_to_find[:3]:
            print(f"       • {sig[:66]}")
        print()

    # ── Thesis ──
    print(thin)
    print("  THESIS")
    print(thin)
    words = company.thesis_summary.split()
    line = "  "
    for w in words:
        if len(line) + len(w) + 1 > 71:
            print(line)
            line = "  " + w
        else:
            line += (" " if line.strip() else "") + w
    if line.strip():
        print(line)

    # ── Risks ──
    print(f"\n{thin}")
    print("  KEY RISKS")
    print(thin)
    for r in company.key_risks:
        print(f"  ✗ {r}")

    print(f"\n{sep}\n")
