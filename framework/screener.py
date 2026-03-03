"""
Screener — rank a list of companies by Pivot Score.
Use this to triage a watchlist from a raw data import.
"""

from typing import Optional
from .models import Company, ScoringWeights
from .scoring import score_company, ScoringResult


def screen(companies: list[Company],
           weights: Optional[ScoringWeights] = None,
           min_score: float = 5.0,
           min_asymmetry: float = 2.0) -> list[tuple[Company, ScoringResult]]:
    """
    Score all companies and return those passing minimum thresholds,
    sorted by pivot_score descending.

    Args:
        companies:      List of Company objects to evaluate
        weights:        Custom scoring weights (defaults to ScoringWeights())
        min_score:      Minimum pivot score to include in results
        min_asymmetry:  Minimum asymmetry ratio (bull / bear) to include

    Returns:
        List of (Company, ScoringResult) tuples, sorted by score descending
    """
    results = []
    for company in companies:
        result = score_company(company, weights)
        passes_score     = result.pivot_score >= min_score
        passes_asymmetry = (result.asymmetry_ratio is None or
                            result.asymmetry_ratio >= min_asymmetry)
        if passes_score and passes_asymmetry:
            results.append((company, result))

    results.sort(key=lambda x: x[1].pivot_score, reverse=True)
    return results


def print_screen_summary(results: list[tuple[Company, ScoringResult]]) -> None:
    """Print a compact ranked table of screener results."""
    if not results:
        print("No companies passed the screening criteria.")
        return

    header = (
        f"{'#':>2}  {'Company':<28} {'Score':>5}  {'Tier':<6}  "
        f"{'Asym':>5}  {'EV Ret':>7}  {'Pivot Types'}"
    )
    print("\n" + "═" * 80)
    print("  PIVOT OPPORTUNITY SCREENER — RESULTS")
    print("═" * 80)
    print(header)
    print("─" * 80)

    for i, (company, result) in enumerate(results, 1):
        asym_str = f"{result.asymmetry_ratio:.1f}x" if result.asymmetry_ratio else "  —"
        ev_str   = (f"+{result.probability_weighted_return_pct:.0f}%"
                    if result.probability_weighted_return_pct else "  —")
        types    = ", ".join(pt.replace("_", " ") for pt in result.recommended_pivot_types[:2])
        print(
            f"  {i:>2}  {company.name:<28} {result.pivot_score:>5.1f}  "
            f"{result.conviction_tier:<6}  {asym_str:>5}  {ev_str:>7}  {types}"
        )

    print("─" * 80)
    print(f"  {len(results)} companies passed screening.\n")
