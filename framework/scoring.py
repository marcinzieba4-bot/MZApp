"""
Scoring Engine — translates raw company data + signals into a Pivot Score.

Architecture
────────────
The score has two independent layers:

  Layer 1 — Quantitative (from balance sheet / price data)
    Produces sub-scores for asset asymmetry and downside protection.

  Layer 2 — Qualitative (from signals and thesis)
    Produces sub-scores for smart money, catalyst clarity, business quality,
    and sentiment discount.

Final score = weighted average of all six dimensions (0–10 scale).

Conviction Tiers
  HIGH   ≥ 7.0  → Size position, monitor weekly
  MEDIUM 5.0–6.9 → Starter position, set price alerts
  WATCH  3.0–4.9 → On radar, revisit in 6 months
  PASS   < 3.0  → Not enough asymmetry today
"""

from dataclasses import dataclass
from typing import Optional
import math

from .models import Company, PriceScenario, PivotSignal, SignalStrength, ScoringWeights


# ──────────────────────────────────────────────
# Sub-score helpers
# ──────────────────────────────────────────────

def _score_asset_asymmetry(company: Company) -> tuple[float, str]:
    """
    Measures how much the market is undervaluing the asset base.

    Key ratios used:
      P/B  < 1.0  → you're buying assets cheaper than replacement cost
      (Net cash + hidden assets) / Market cap → safety cushion
      EBITDA margin trajectory → earnings lever
    """
    score = 5.0   # Start neutral
    notes = []

    # Price-to-book discount
    if company.book_value_per_share and company.book_value_per_share > 0:
        pb = company.current_price / company.book_value_per_share
        if pb < 0.5:
            score += 3.0
            notes.append(f"P/B={pb:.2f} — deep discount, strong asset backing")
        elif pb < 0.8:
            score += 2.0
            notes.append(f"P/B={pb:.2f} — trading below book")
        elif pb < 1.0:
            score += 1.0
            notes.append(f"P/B={pb:.2f} — slight discount to book")
        elif pb > 2.5:
            score -= 1.5
            notes.append(f"P/B={pb:.2f} — premium to book, limited asset cushion")

    # Hidden / off-balance-sheet asset value
    if company.hidden_asset_value_per_share:
        hidden_pct = company.hidden_asset_value_per_share / company.current_price
        if hidden_pct > 1.0:
            score += 2.5
            notes.append(f"Hidden assets >{hidden_pct*100:.0f}% of current price — major unrealised value")
        elif hidden_pct > 0.5:
            score += 1.5
            notes.append(f"Hidden assets ~{hidden_pct*100:.0f}% of current price")
        elif hidden_pct > 0.2:
            score += 0.5
            notes.append(f"Some off-book value ({hidden_pct*100:.0f}%)")

    # Net cash cushion
    if company.net_cash_per_share and company.net_cash_per_share > 0:
        cash_pct = company.net_cash_per_share / company.current_price
        if cash_pct > 0.5:
            score += 1.5
            notes.append(f"Net cash = {cash_pct*100:.0f}% of price — massive cushion")
        elif cash_pct > 0.2:
            score += 0.75
            notes.append(f"Meaningful net cash position")

    return min(max(score, 0), 10), "; ".join(notes)


def _score_downside_protection(company: Company) -> tuple[float, str]:
    """
    How much can you lose in the bear case?
    A good pivot candidate has an asymmetric floor — hard assets, cash,
    or a contractual floor (e.g. order book) limit the downside.
    """
    score = 5.0
    notes = []

    scenarios = {s.label: s for s in company.scenarios}
    bear = scenarios.get("bear")
    base = scenarios.get("base")

    if bear and base:
        downside_pct = (bear.price_target - company.current_price) / company.current_price
        upside_pct   = (base.price_target - company.current_price) / company.current_price

        if downside_pct > -0.15:
            score += 3.0
            notes.append(f"Bear downside only {downside_pct*100:.0f}% — floor is close")
        elif downside_pct > -0.30:
            score += 1.5
            notes.append(f"Bear downside {downside_pct*100:.0f}% — manageable")
        elif downside_pct < -0.50:
            score -= 2.0
            notes.append(f"Bear downside {downside_pct*100:.0f}% — significant capital risk")

        if upside_pct > 1.0:
            notes.append(f"Base upside +{upside_pct*100:.0f}% — strong base case return")

    if company.book_value_per_share:
        pb = company.current_price / company.book_value_per_share
        if pb < 0.7:
            score += 1.5
            notes.append("Trading below book → liquidation value provides floor")

    return min(max(score, 0), 10), "; ".join(notes)


def _score_smart_money_signals(company: Company) -> tuple[float, str]:
    """
    Smart money creates pre-conditions for a pivot, validates the thesis,
    and often IS the catalyst (activist, PE buyout, strategic acquisition).
    """
    score = 0.0
    notes = []

    smart_money_signals = [s for s in company.signals if s.category == "smart_money"]

    for sig in smart_money_signals:
        weight = {
            SignalStrength.WEAK: 0.5,
            SignalStrength.MODERATE: 1.5,
            SignalStrength.STRONG: 2.5,
            SignalStrength.DEFINITIVE: 4.0,
        }[sig.strength]
        score += weight * sig.confidence
        notes.append(f"[{sig.strength.name}] {sig.name}")

    # Low float amplifies any activist's leverage
    if company.float_pct and company.float_pct < 30:
        score += 1.0
        notes.append(f"Low float ({company.float_pct:.0f}%) → small buyer moves needle")

    # Very high insider ownership can mean founder will NOT sell (risk) OR
    # single decision-maker makes deal faster (opportunity)
    if company.insider_ownership_pct:
        if company.insider_ownership_pct > 50:
            score += 0.5   # One call to the founder
            notes.append(f"Founder-controlled ({company.insider_ownership_pct:.0f}%) — single decision point")

    return min(max(score, 0), 10), "; ".join(notes)


def _score_catalyst_clarity(company: Company) -> tuple[float, str]:
    """
    A thesis without a catalyst is just hope.
    Score how concrete, near-term, and binary the trigger event is.
    """
    score = 0.0
    notes = []

    catalyst_signals = [s for s in company.signals if s.category == "catalyst"]

    for sig in catalyst_signals:
        weight = {
            SignalStrength.WEAK: 0.75,
            SignalStrength.MODERATE: 2.0,
            SignalStrength.STRONG: 3.0,
            SignalStrength.DEFINITIVE: 5.0,
        }[sig.strength]
        score += weight * sig.confidence
        notes.append(f"[{sig.strength.name}] {sig.name}")

    # Penalise very long waits — time kills IRR
    if company.time_horizon_years > 5:
        score -= 1.5
        notes.append(f"Long horizon ({company.time_horizon_years}y) compresses IRR")
    elif company.time_horizon_years <= 2:
        score += 1.0
        notes.append(f"Short horizon ({company.time_horizon_years}y) → fast IRR")

    return min(max(score, 0), 10), "; ".join(notes)


def _score_business_quality(company: Company) -> tuple[float, str]:
    """
    You need the core business to survive while waiting for the pivot.
    Not a growth stock analysis — just 'can it hold together for 3 years?'
    """
    score = 5.0
    notes = []

    if company.ebitda_margin_pct is not None:
        if company.ebitda_margin_pct > 15:
            score += 2.0
            notes.append(f"EBITDA margin {company.ebitda_margin_pct:.0f}% — self-funding")
        elif company.ebitda_margin_pct > 5:
            score += 0.5
            notes.append(f"EBITDA margin {company.ebitda_margin_pct:.0f}% — adequate")
        elif company.ebitda_margin_pct < 0:
            score -= 3.0
            notes.append(f"Negative EBITDA — burning cash, time pressure")

    if company.revenue_growth_yoy_pct is not None:
        if company.revenue_growth_yoy_pct > 10:
            score += 1.0
            notes.append("Revenue growing — organic momentum")
        elif company.revenue_growth_yoy_pct < -10:
            score -= 1.5
            notes.append("Revenue declining — business deteriorating")

    return min(max(score, 0), 10), "; ".join(notes)


def _score_sentiment_discount(company: Company) -> tuple[float, str]:
    """
    The more ignored/hated a stock, the bigger the re-rating potential.
    Contrarian premium: if everyone already knows it, the easy money is made.
    """
    score = 5.0
    notes = []

    sentiment_signals = [s for s in company.signals if s.category == "sentiment"]
    for sig in sentiment_signals:
        if sig.strength in (SignalStrength.STRONG, SignalStrength.DEFINITIVE):
            score += 2.0
        elif sig.strength == SignalStrength.MODERATE:
            score += 1.0
        notes.append(sig.name)

    # Low institutional ownership = under-discovered
    if company.institutional_ownership_pct is not None:
        if company.institutional_ownership_pct < 10:
            score += 2.0
            notes.append("Under-owned by institutions — re-rating potential is large")
        elif company.institutional_ownership_pct < 25:
            score += 1.0
            notes.append("Below-average institutional coverage")
        elif company.institutional_ownership_pct > 70:
            score -= 1.0
            notes.append("Well-owned — less room for discovery re-rating")

    return min(max(score, 0), 10), "; ".join(notes)


# ──────────────────────────────────────────────
# Asymmetry calculator
# ──────────────────────────────────────────────

def compute_asymmetry(company: Company) -> Optional[float]:
    """
    Asymmetry Ratio = (Bull upside) / (Bear downside)
    > 3x is attractive. > 5x is exceptional.
    Returns None if scenarios are missing.
    """
    scenarios = {s.label: s for s in company.scenarios}
    bull = scenarios.get("bull")
    bear = scenarios.get("bear")
    if not bull or not bear:
        return None

    upside   = bull.price_target - company.current_price
    downside = company.current_price - bear.price_target

    if downside <= 0:
        return float("inf")   # No downside scenario — rare but flag it
    if upside <= 0:
        return 0.0

    return round(upside / downside, 2)


def compute_probability_weighted_return(company: Company) -> Optional[float]:
    """
    EV of return = sum(probability_i * (price_i / current_price - 1))
    """
    if not company.scenarios:
        return None
    ev = sum(
        s.probability * (s.price_target / company.current_price - 1)
        for s in company.scenarios
    )
    return round(ev * 100, 1)   # as percentage


# ──────────────────────────────────────────────
# Main scoring function
# ──────────────────────────────────────────────

@dataclass
class ScoringResult:
    company_name: str
    pivot_score: float
    conviction_tier: str
    asymmetry_ratio: Optional[float]
    probability_weighted_return_pct: Optional[float]
    dimension_scores: dict[str, float]
    dimension_notes: dict[str, str]
    recommended_pivot_types: list[str]


def score_company(company: Company, weights: Optional[ScoringWeights] = None) -> ScoringResult:
    """
    Run the full scoring pipeline on a Company and return a ScoringResult.
    Also mutates the Company's pivot_score, asymmetry_ratio, conviction_tier fields.
    """
    if weights is None:
        weights = ScoringWeights()

    assert weights.validate(), "Weights must sum to 1.0"

    # Compute each dimension
    asset_score,     asset_notes     = _score_asset_asymmetry(company)
    smart_score,     smart_notes     = _score_smart_money_signals(company)
    catalyst_score,  catalyst_notes  = _score_catalyst_clarity(company)
    downside_score,  downside_notes  = _score_downside_protection(company)
    quality_score,   quality_notes   = _score_business_quality(company)
    sentiment_score, sentiment_notes = _score_sentiment_discount(company)

    # Weighted composite
    pivot_score = (
        asset_score     * weights.asset_asymmetry    +
        smart_score     * weights.smart_money_signals +
        catalyst_score  * weights.catalyst_clarity   +
        downside_score  * weights.downside_protection +
        quality_score   * weights.business_quality   +
        sentiment_score * weights.sentiment_discount
    )
    pivot_score = round(pivot_score, 2)

    # Asymmetry
    asymmetry = compute_asymmetry(company)
    pwr       = compute_probability_weighted_return(company)

    # Conviction tier
    if pivot_score >= 7.0 and (asymmetry is None or asymmetry >= 2.5):
        tier = "HIGH"
    elif pivot_score >= 5.0:
        tier = "MEDIUM"
    elif pivot_score >= 3.0:
        tier = "WATCH"
    else:
        tier = "PASS"

    # Write back to company
    company.pivot_score     = pivot_score
    company.asymmetry_ratio = asymmetry
    company.conviction_tier = tier

    return ScoringResult(
        company_name=company.name,
        pivot_score=pivot_score,
        conviction_tier=tier,
        asymmetry_ratio=asymmetry,
        probability_weighted_return_pct=pwr,
        dimension_scores={
            "asset_asymmetry":    round(asset_score, 2),
            "smart_money_signals": round(smart_score, 2),
            "catalyst_clarity":   round(catalyst_score, 2),
            "downside_protection": round(downside_score, 2),
            "business_quality":   round(quality_score, 2),
            "sentiment_discount": round(sentiment_score, 2),
        },
        dimension_notes={
            "asset_asymmetry":    asset_notes,
            "smart_money_signals": smart_notes,
            "catalyst_clarity":   catalyst_notes,
            "downside_protection": downside_notes,
            "business_quality":   quality_notes,
            "sentiment_discount": sentiment_notes,
        },
        recommended_pivot_types=[pt.value for pt in company.pivot_types],
    )
